"""Transforms applied to Paradox-script ASTs for gk_lithogenesis generation.

Only one transform so far: `rebase_food_to_minerals` wraps every `food = X` clause
inside `cost { }` / `upkeep { }` blocks with a trigger that excludes lithogenesis
empires, and emits a mirror `minerals = X * 0.8` clause gated to include them.

The transform is idempotent: if a cost/upkeep clause already mentions
`graphical_culture = lithogenesis_01`, it's skipped.
"""

from __future__ import annotations

import copy
from typing import List

from pdxscript import (
    Assign, Block, Comment, Node, Scalar, _BareWord, contains_text, parse,
)


LITHO_CULTURE = "lithogenesis_01"


def _trigger_block(include_litho: bool) -> Assign:
    """Build a trigger = { from = { country_uses_bio_ships = yes [NOT =] graphical_culture = litho } } assign."""
    inner = Block([
        Assign("country_uses_bio_ships", Scalar("yes")),
    ])
    if include_litho:
        inner.children.append(Assign("graphical_culture", Scalar(LITHO_CULTURE)))
    else:
        inner.children.append(
            Assign(
                "NOT",
                Block([Assign("graphical_culture", Scalar(LITHO_CULTURE))]),
            )
        )
    outer = Block([Assign("from", inner)])
    return Assign("trigger", outer)


def _has_trigger_clause(block: Block) -> bool:
    for a in block.children:
        if isinstance(a, Assign) and a.key == "trigger":
            return True
    return False


def _clause_already_rebased(clause: Block) -> bool:
    """A clause is 'already rebased' if it has a trigger mentioning graphical_culture."""
    for child in clause.children:
        if isinstance(child, Assign) and child.key == "trigger":
            if contains_text(child.value, LITHO_CULTURE):
                return True
    return False


def _is_food_clause(clause: Block) -> bool:
    for child in clause.children:
        if isinstance(child, Assign) and child.key == "food":
            return True
    return False


def _make_minerals_mirror(food_clause: Block) -> Block:
    """Given a cost/upkeep clause containing food = X, produce the minerals mirror.

    Copies all non-food / non-trigger children verbatim, replaces `food` with
    `minerals`, adds `mult = 0.8`, and swaps trigger to include lithogenesis.
    """
    mirror = Block([])
    for child in food_clause.children:
        if isinstance(child, Assign):
            if child.key == "food":
                mirror.children.append(Assign("minerals", copy.deepcopy(child.value)))
            elif child.key == "trigger":
                pass  # added below
            else:
                mirror.children.append(copy.deepcopy(child))
        else:
            mirror.children.append(copy.deepcopy(child))
    # scaling; append last so it multiplies the base
    mirror.children.append(Assign("mult", Scalar("0.8")))
    # lithogenesis trigger
    mirror.children.append(_trigger_block(include_litho=True))
    return mirror


def _wrap_food_clause_with_non_litho_trigger(clause: Block) -> None:
    """Add a NOT graphical_culture trigger to the food clause (mutating)."""
    clause.children.append(_trigger_block(include_litho=False))


def _rebase_resources_block(resources: Block) -> None:
    """Walk resources children: for each cost/upkeep clause containing food,
    rewrite it in-place and insert a minerals mirror immediately after."""
    new_children: List[Node] = []
    for child in resources.children:
        if (
            isinstance(child, Assign)
            and child.key in ("cost", "upkeep")
            and isinstance(child.value, Block)
            and _is_food_clause(child.value)
            and not _clause_already_rebased(child.value)
        ):
            _wrap_food_clause_with_non_litho_trigger(child.value)
            new_children.append(child)
            mirror_clause = Assign(child.key, _make_minerals_mirror(child.value))
            new_children.append(mirror_clause)
        else:
            new_children.append(child)
    resources.children = new_children


def rebase_food_to_minerals(root: Block) -> None:
    """Recursively find `resources = { ... }` blocks and rebase food->minerals.

    Also applies to top-level cost/upkeep clauses (for inline_script files that
    have them at the root rather than nested inside `resources`).
    """
    # Top-level cost/upkeep (inline_script style)
    _rebase_resources_block(root)
    # Recurse into all blocks
    for child in root.children:
        if isinstance(child, Assign) and isinstance(child.value, Block):
            # If this is a 'resources' assign, its children are the cost/upkeep clauses
            if child.key == "resources":
                _rebase_resources_block(child.value)
            else:
                rebase_food_to_minerals(child.value)


# -----------------------------------------------------------------------------
# Detection
# -----------------------------------------------------------------------------


BIO_SIGNAL_KEYS = (
    "country_uses_bio_ships",
    "is_galvanic_empire",
    "ship_uses_weaver_components",
)


def is_bio_ship_block(node: Assign) -> bool:
    """Heuristic: does this top-level block look like a bio-ship component?

    Checks potential / show_tech_unlock_if (component_template) and direct
    trigger text (inline_script) for any of the bio-ship signal triggers.
    """
    if not isinstance(node.value, Block):
        return False
    for signal in BIO_SIGNAL_KEYS:
        if contains_text(node.value, signal):
            return True
    return False


def has_food_resource(node: Assign) -> bool:
    """Does this block's resources (or top-level cost/upkeep) mention food?"""
    if not isinstance(node.value, Block):
        return False
    res = None
    for child in node.value.children:
        if isinstance(child, Assign) and child.key == "resources":
            res = child.value
            break
    if res is None:
        # top-level? check the block itself
        res = node.value
    # is there any cost/upkeep with food = X?
    for child in res.children:
        if (
            isinstance(child, Assign)
            and child.key in ("cost", "upkeep")
            and isinstance(child.value, Block)
            and _is_food_clause(child.value)
        ):
            return True
    return False
