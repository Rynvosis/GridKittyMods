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


def _split_food_clause(clause: Block, kind: str) -> List[Assign]:
    """Split a cost/upkeep clause containing `food = X` into up to three clauses:

    1. Non-food resources (alloys, sr_living_metal, etc.) with original mults,
       no trigger. Unconditional — always applies when the component is visible.
       Omitted if the clause had only food.
    2. Food clause: food, original mults, trigger = { NOT graphical_culture = litho }.
    3. Minerals mirror: minerals = food_value, original mults, mult = 0.8,
       trigger = { graphical_culture = litho }.

    `kind` is "cost" or "upkeep" (used for each new Assign's key).

    Rationale: the original `mult = X` in a clause applies to every resource
    in that clause. Duplicating non-food siblings into the minerals branch
    would apply the 0.8 lithogenesis scaling to them too, which is wrong.
    """
    food_value = None
    mults: List[Node] = []
    other_resources: List[Node] = []
    for child in clause.children:
        if isinstance(child, Assign):
            if child.key == "food":
                food_value = copy.deepcopy(child.value)
            elif child.key == "mult":
                mults.append(copy.deepcopy(child))
            elif child.key == "trigger":
                # Drop existing triggers. Vanilla's per-clause dispatch pattern
                # (e.g. cloaking) wraps food in trigger = { country_uses_bio_ships = yes };
                # our generated NOT-litho and litho triggers both already assert bio = yes,
                # so preserving the original would be redundant at best and conflicting at worst.
                pass
            else:
                other_resources.append(copy.deepcopy(child))
        else:
            other_resources.append(copy.deepcopy(child))
    assert food_value is not None, "_split_food_clause called on non-food clause"

    out: List[Assign] = []

    if other_resources:
        # Unconditional clause carrying everything else + original mults.
        non_food_block = Block(other_resources + [copy.deepcopy(m) for m in mults])
        out.append(Assign(kind, non_food_block))

    # Food clause for non-lithogenesis bio empires.
    food_block = Block(
        [Assign("food", copy.deepcopy(food_value))]
        + [copy.deepcopy(m) for m in mults]
        + [_trigger_block(include_litho=False)]
    )
    out.append(Assign(kind, food_block))

    # Minerals mirror for lithogenesis empires. Original mults + 0.8 litho scaling.
    minerals_block = Block(
        [Assign("minerals", copy.deepcopy(food_value))]
        + [copy.deepcopy(m) for m in mults]
        + [Assign("mult", Scalar("0.8"))]
        + [_trigger_block(include_litho=True)]
    )
    out.append(Assign(kind, minerals_block))

    return out


def _rebase_resources_block(resources: Block) -> None:
    """Walk resources children: for each cost/upkeep clause containing food,
    split into (non-food, food-non-litho, minerals-litho) clauses in place."""
    new_children: List[Node] = []
    for child in resources.children:
        if (
            isinstance(child, Assign)
            and child.key in ("cost", "upkeep")
            and isinstance(child.value, Block)
            and _is_food_clause(child.value)
            and not _clause_already_rebased(child.value)
        ):
            new_children.extend(_split_food_clause(child.value, child.key))
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
    # Canonical bio-ship marker — most bio components carry this in potential
    # or show_tech_unlock_if.
    "country_uses_bio_ships",
    # Weaver-specific gating. The underlying scripted_trigger only matches
    # weaver_stage_* ship sizes (all from Biogenesis DLC), so this implies
    # bio-ship context. Some components (e.g. WEAVER_BOOSTER_1) only gate on
    # this trigger without country_uses_bio_ships, so we need it as a fallback.
    "ship_uses_weaver_components",
    # is_galvanic_empire is intentionally NOT here. Non-bio empires can be
    # galvanic, so the trigger alone doesn't imply bio-ship context. Galvanic
    # bio-ship components always pair it with country_uses_bio_ships = yes,
    # which catches them via the primary signal.
)


def _has_assign_yes(block: Block, key: str) -> bool:
    """Recursively: does the block contain `key = yes` anywhere?"""
    for child in block.children:
        if isinstance(child, Assign):
            if (
                child.key == key
                and isinstance(child.value, Scalar)
                and child.value.raw == "yes"
            ):
                return True
            if isinstance(child.value, Block):
                if _has_assign_yes(child.value, key):
                    return True
    return False


def _has_assign_no(block: Block, key: str) -> bool:
    """Recursively: does the block contain `key = no` anywhere?"""
    for child in block.children:
        if isinstance(child, Assign):
            if (
                child.key == key
                and isinstance(child.value, Scalar)
                and child.value.raw == "no"
            ):
                return True
            if isinstance(child.value, Block):
                if _has_assign_no(child.value, key):
                    return True
    return False


def _clause_has_bio_yes_food(clause: Block) -> bool:
    """Does this cost/upkeep clause have `food = X` AND a trigger asserting
    country_uses_bio_ships = yes? This is vanilla's per-clause bio-dispatch
    pattern (e.g. CORVETTE_CLOAKING_1: food branch gated by bio=yes trigger)."""
    has_food = False
    has_bio_trigger = False
    for child in clause.children:
        if isinstance(child, Assign):
            if child.key == "food":
                has_food = True
            elif child.key == "trigger" and isinstance(child.value, Block):
                if _has_assign_yes(child.value, "country_uses_bio_ships"):
                    has_bio_trigger = True
    return has_food and has_bio_trigger


def is_bio_ship_block(node: Assign) -> bool:
    """Structural check: is this component bio-ship-relevant?

    Two independent paths qualify:

    1. Component-level gating: `potential` or `show_tech_unlock_if` positively
       asserts one of the BIO_SIGNAL_KEYS = yes. `country_uses_bio_ships = no`
       in these scopes is an explicit exclusion that overrides everything.

    2. Clause-level dispatch: the `resources` block has at least one
       cost/upkeep clause containing `food = X` gated by a trigger that
       asserts `country_uses_bio_ships = yes`. This is the pattern vanilla
       uses for components available to all empires but with food upkeep
       for bio empires only (e.g. CORVETTE_CLOAKING_1).
    """
    if not isinstance(node.value, Block):
        return False
    potential = None
    tech_unlock = None
    resources = None
    for child in node.value.children:
        if isinstance(child, Assign):
            if child.key == "potential" and isinstance(child.value, Block):
                potential = child.value
            elif child.key == "show_tech_unlock_if" and isinstance(child.value, Block):
                tech_unlock = child.value
            elif child.key == "resources" and isinstance(child.value, Block):
                resources = child.value
    # Explicit exclusion wins over everything else.
    if potential and _has_assign_no(potential, "country_uses_bio_ships"):
        return False
    if tech_unlock and _has_assign_no(tech_unlock, "country_uses_bio_ships"):
        return False
    # Path 1: positive signal in potential / show_tech_unlock_if.
    for scope in (potential, tech_unlock):
        if scope is None:
            continue
        for signal in BIO_SIGNAL_KEYS:
            if _has_assign_yes(scope, signal):
                return True
    # Path 2: clause-level bio-yes food dispatch inside resources.
    if resources is not None:
        for child in resources.children:
            if (
                isinstance(child, Assign)
                and child.key in ("cost", "upkeep")
                and isinstance(child.value, Block)
                and _clause_has_bio_yes_food(child.value)
            ):
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
