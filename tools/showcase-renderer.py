#!/home/ryn/pyflex/bin/python3
"""Showcase page renderer for GK Stellaris mods.

Uses Facebook Yoga (via poga) for flexbox layout and ImageMagick for compositing.
Flow: measure → layout → render at computed sizes → composite.

Theme cascade: item > page theme > global theme > hardcoded default.

Usage: tools/showcase-renderer <page.yaml> [--output <path>]
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from poga.libpoga_capi import *


def magick(*args):
    cmd = ["magick"] + [str(a) for a in args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"magick error: {result.stderr}", file=sys.stderr)
    return result.stdout.strip()


def img_identify(path):
    out = magick("identify", "-format", "%w %h", path)
    parts = out.split()
    return int(parts[0]), int(parts[1])


def resolve_path(src, base_dir):
    return str(base_dir / src)


def apply_crop_to_dims(sw, sh, crop):
    """Apply crop to source dimensions."""
    if "gravity" in crop:
        sh = int(sh * crop["percent"] / 100)
    elif "top" in crop:
        sh -= crop["top"]
    elif "bottom" in crop:
        sh -= crop["bottom"]
    return sw, sh


DIRECTION_MAP = {"horizontal": Row, "vertical": Column}

JUSTIFY_MAP = {
    "start": YGJustify(0), "center": YGJustify(1), "end": YGJustify(2),
    "space-between": YGJustify(3), "space-around": YGJustify(4),
    "space-evenly": YGJustify(5),
}
ALIGN_MAP = {
    "start": YGAlign(1), "center": YGAlign(2), "end": YGAlign(3),
    "stretch": YGAlign(4),
}



class Renderer:
    def __init__(self, globals_cfg, page_cfg, base_dir):
        self.g = globals_cfg
        self.page = page_cfg
        self.base_dir = base_dir
        self.tmp = Path(tempfile.mkdtemp(prefix="showcase_"))
        self.counter = 0

        font_path = self.g["font"]["path"]
        if font_path.startswith("~"):
            font_path = os.path.expanduser(font_path)
        else:
            font_path = resolve_path(font_path, base_dir)
        self.font_path = font_path

        L = self.g["layout"]
        self.margin = L["margin"]
        self.top_y = L["top_y"]
        self.canvas_w, self.canvas_h = self.g["canvas"]
        self.full_w = self.canvas_w - 2 * self.margin
        self.full_h = self.canvas_h - self.margin - self.top_y

        self.beige = self.g["colors"]["beige"]
        self.red = self.g["colors"]["red"]
        self.black = self.g["colors"]["black"]

        # Theme: global < page
        self.global_theme = self.g.get("theme", {})
        self.page_theme = self.page.get("theme", {})

    def tmp_path(self):
        self.counter += 1
        return str(self.tmp / f"tmp_{self.counter}.png")

    def theme(self, item_type, prop, item_cfg=None):
        """Resolve a theme property: item > page theme > global theme > default."""
        if item_cfg and prop in item_cfg:
            return item_cfg[prop]
        page = self.page_theme.get(item_type, {})
        if prop in page:
            return page[prop]
        glob = self.global_theme.get(item_type, {})
        if prop in glob:
            return glob[prop]
        return None

    def resolve_decorator(self, dec_cfg):
        """Resolve a decorator: name → theme.decorator.name, dict → use directly."""
        if dec_cfg is None:
            return None
        if isinstance(dec_cfg, str):
            decorators = self.global_theme.get("decorator", {})
            return decorators.get(dec_cfg)
        if isinstance(dec_cfg, dict):
            return dec_cfg
        return None

    # ── Text ──

    def make_text(self, text, style_name):
        style = self.g["font"]["sizes"][style_name]
        pt, pad, kern = style["pt"], style["pad"], style.get("kern", 0)
        r_path, b_path = self.tmp_path(), self.tmp_path()
        for fill, path in [(self.red, r_path), (self.beige, b_path)]:
            magick("-background", "none", "-fill", fill,
                   "-font", self.font_path, "-pointsize", pt,
                   "-kerning", kern, f"label:{text}", path)
        w, h = img_identify(r_path)
        cw, ch = w + 1 + pad * 2, h + 1 + pad * 2
        combined = self.tmp_path()
        magick("-size", f"{cw}x{ch}", "xc:none",
               "(", r_path, ")", "-gravity", "NorthWest",
               "-geometry", f"+{pad+1}+{pad+1}", "-composite",
               "(", b_path, ")", "-gravity", "NorthWest",
               "-geometry", f"+{pad}+{pad}", "-composite", combined)
        return self._outline(self._outline(combined, cw, ch), cw, ch)

    def _outline(self, src, w, h):
        alpha = self.tmp_path()
        magick(src, "-alpha", "extract", alpha)
        outline = self.tmp_path()
        args = ["-size", f"{w}x{h}", "xc:none"]
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
            args += ["(", alpha, "-background", self.black,
                     "-alpha", "shape", "-geometry", f"{dx:+d}{dy:+d}", ")", "-composite"]
        magick(*args, outline)
        result = self.tmp_path()
        magick(outline, "(", src, ")", "-composite", result)
        return result

    def make_inline(self, big, small):
        bw, bh = img_identify(big)
        sw, sh = img_identify(small)
        out = self.tmp_path()
        magick("-size", f"{bw+12+sw}x{bh}", "xc:none",
               "(", big, ")", "-gravity", "NorthWest", "-geometry", "+0+0", "-composite",
               "(", small, ")", "-gravity", "NorthWest",
               "-geometry", f"+{bw+12}+{(bh-sh)//2}", "-composite", out)
        return out

    # ── Image processing ──

    def _clip_round(self, src, radius, stroke, stroke_width):
        """Apply rounded corner clipping + border stroke to an image."""
        w, h = img_identify(src)
        r = radius
        mask = self.tmp_path()
        magick("-size", f"{w}x{h}", "xc:black", "+antialias",
               "-fill", "white", "-draw", f"roundrectangle 0,0 {w-1},{h-1} {r},{r}", mask)
        clipped = self.tmp_path()
        magick(src, mask, "-alpha", "off", "-compose", "CopyOpacity", "-composite", clipped)
        border = self.tmp_path()
        magick("-size", f"{w}x{h}", "xc:none", "+antialias",
               "-fill", "none", "-stroke", stroke, "-strokewidth", str(stroke_width),
               "-draw", f"roundrectangle 0,0 {w-1},{h-1} {r},{r}", border)
        out = self.tmp_path()
        magick(clipped, border, "-compose", "Over", "-composite", out)
        return out

    def _apply_crop(self, src, crop):
        """Crop a source image. Matches apply_crop_to_dims."""
        cropped = self.tmp_path()
        if "gravity" in crop:
            magick(src, "-gravity", crop["gravity"],
                   "-crop", f"100%x{crop['percent']}%+0+0", "+repage", cropped)
        elif "top" in crop:
            sw, sh = img_identify(src)
            magick(src, "-crop", f"{sw}x{sh - crop['top']}+0+{crop['top']}",
                   "+repage", cropped)
        elif "bottom" in crop:
            sw, sh = img_identify(src)
            magick(src, "-crop", f"{sw}x{sh - crop['bottom']}+0+0",
                   "+repage", cropped)
        else:
            return src
        return cropped

    def _make_box(self, w, h, dec):
        """Create a filled rounded box (decorator background)."""
        out = self.tmp_path()
        r = dec.get("radius", 6)
        magick("-size", f"{w}x{h}", "xc:none", "+antialias",
               "-fill", dec.get("fill", "rgba(60,56,54,0.45)"),
               "-stroke", dec.get("stroke", "rgba(160,150,140,0.6)"),
               "-strokewidth", str(dec.get("stroke_width", 1)),
               "-draw", f"roundrectangle 0,0 {w-1},{h-1} {r},{r}", out)
        return out

    def render_image(self, item, tw):
        """Crop, resize to width, optionally round corners based on theme."""
        src = resolve_path(item["src"], self.base_dir)
        if "crop" in item:
            src = self._apply_crop(src, item["crop"])
        resized = self.tmp_path()
        magick(src, "-resize", f"{tw}x", resized)

        if self.theme("image", "border", item):
            radius = self.theme("image", "radius", item)
            stroke = self.theme("image", "stroke", item)
            stroke_w = self.theme("image", "stroke_width", item)
            return self._clip_round(resized, radius, stroke, stroke_w)
        return resized

    # ── Measure (Phase 1) ──

    def measure_leaf(self, cfg):
        """Get natural dimensions. Returns (w, h, pre_rendered_path_or_None)."""
        t = cfg.get("type")

        if t == "image":
            src = resolve_path(cfg["src"], self.base_dir)
            sw, sh = img_identify(src)
            if "crop" in cfg:
                sw, sh = apply_crop_to_dims(sw, sh, cfg["crop"])
            return sw, sh, None

        if t == "label":
            path = self.make_text(cfg["text"], cfg.get("style", "label"))
            w, h = img_identify(path)
            return w, h, path

        return 100, 100, None

    # ── Build Yoga tree (Phase 1) ──

    def build_yoga_tree(self, cfg, leaves):
        """Build Yoga node tree. Leaves gets (cfg, pre_path) for each leaf."""
        node = YGNodeNew()

        # Defaults
        YGNodeStyleSetFlexDirection(node, Column)
        YGNodeStyleSetJustifyContent(node, JUSTIFY_MAP["start"])
        YGNodeStyleSetAlignItems(node, ALIGN_MAP["stretch"])

        direction = "vertical"
        gap = self.theme("group", "gap") or 0
        align = "stretch"
        children = []

        for key, val in cfg.items():
            match key:
                case "type" | "decorator":
                    pass  # handled elsewhere
                case "items":
                    children = val
                case "direction":
                    direction = val
                    if val not in DIRECTION_MAP:
                        print(f"WARNING: unknown direction '{val}'", file=sys.stderr)
                    else:
                        YGNodeStyleSetFlexDirection(node, DIRECTION_MAP[val])
                case "gap":
                    gap = val
                case "justify":
                    if val not in JUSTIFY_MAP:
                        print(f"WARNING: unknown justify '{val}'", file=sys.stderr)
                    else:
                        YGNodeStyleSetJustifyContent(node, JUSTIFY_MAP[val])
                case "align":
                    align = val
                    if val not in ALIGN_MAP:
                        print(f"WARNING: unknown align '{val}'", file=sys.stderr)
                    else:
                        YGNodeStyleSetAlignItems(node, ALIGN_MAP[val])
                case "size":
                    YGNodeStyleSetWidth(node, val[0])
                    YGNodeStyleSetHeight(node, val[1])
                    YGNodeStyleSetOverflow(node, Hidden)
                case "width":
                    YGNodeStyleSetWidth(node, val)
                case "height":
                    YGNodeStyleSetHeight(node, val)
                case "flex":
                    YGNodeStyleSetFlexGrow(node, val)
                    YGNodeStyleSetFlexShrink(node, 1)
                    YGNodeStyleSetFlexBasis(node, 0)
                case "padding":
                    if val:
                        YGNodeStyleSetPadding(node, All, val)
                case _:
                    print(f"WARNING: unknown group property '{key}'", file=sys.stderr)

        # Pass 1: measure leaves, find reference cross-axis for non-stretch
        child_measures = []
        ref_cross = 0
        for child_cfg in children:
            child_type = child_cfg.get("type", "group")
            if child_type != "group":
                for lk in child_cfg:
                    match child_type, lk:
                        case _, "type":
                            pass
                        case "image", ("src" | "crop" | "width" | "height" | "flex"):
                            pass
                        case "image", ("border" | "radius" | "stroke" | "stroke_width"):
                            pass
                        case "label", ("text" | "style" | "flex"):
                            pass
                        case _:
                            src = child_cfg.get("src", child_cfg.get("text", "?"))
                            print(f"WARNING: '{lk}' not supported on "
                                  f"{child_type} ({src})", file=sys.stderr)
                w, h, pre_path = self.measure_leaf(child_cfg)
                child_measures.append((w, h, pre_path))
                if align != "stretch" and child_type == "image":
                    ref_cross = max(ref_cross, h if direction == "horizontal" else w)
            else:
                child_measures.append(None)

        # Pass 2: build yoga nodes
        parent_cross = cfg.get("height") if direction == "horizontal" else cfg.get("width")
        for i, child_cfg in enumerate(children):
            child_type = child_cfg.get("type", "group")

            if child_type == "group":
                child_node = self.build_yoga_tree(child_cfg, leaves)
            else:
                w, h, pre_path = child_measures[i]
                leaves.append((child_cfg, pre_path))

                child_node = YGNodeNew()
                if "flex" in child_cfg:
                    YGNodeStyleSetFlexGrow(child_node, child_cfg["flex"])
                    YGNodeStyleSetFlexShrink(child_node, 1)
                    YGNodeStyleSetFlexBasis(child_node, 0)
                if child_type == "image" and w > 0 and h > 0:
                    ar = w / h
                    if parent_cross:
                        if direction == "horizontal":
                            YGNodeStyleSetHeight(child_node, parent_cross)
                            YGNodeStyleSetWidth(child_node, int(parent_cross * ar))
                        else:
                            YGNodeStyleSetWidth(child_node, parent_cross)
                            YGNodeStyleSetHeight(child_node, int(parent_cross / ar))
                    elif ref_cross > 0:
                        # Proportional: tallest sibling = 100%, others scale
                        natural_cross = h if direction == "horizontal" else w
                        pct = (natural_cross / ref_cross) * 100
                        if direction == "horizontal":
                            YGNodeStyleSetHeightPercent(child_node, pct)
                        else:
                            YGNodeStyleSetWidthPercent(child_node, pct)
                        YGNodeStyleSetAspectRatio(child_node, ar)
                    else:
                        if direction == "vertical":
                            YGNodeStyleSetWidthPercent(child_node, 100)
                        YGNodeStyleSetAspectRatio(child_node, ar)
                        YGNodeStyleSetFlexShrink(child_node, 1)
                elif child_type == "label" and "flex" not in child_cfg:
                    YGNodeStyleSetWidth(child_node, w)
                    YGNodeStyleSetHeight(child_node, h)

                if "width" in child_cfg:
                    YGNodeStyleSetWidth(child_node, child_cfg["width"])
                if "height" in child_cfg:
                    YGNodeStyleSetHeight(child_node, child_cfg["height"])

            if gap and i < len(children) - 1:
                edge = Bottom if direction == "vertical" else Right
                YGNodeStyleSetMargin(child_node, edge, gap)

            YGNodeInsertChild(node, child_node, i)

        return node

    # ── Composite (Phase 2) ──

    def composite_tree(self, node, cfg, leaf_iter, compose_args, ox=0, oy=0):
        x = ox + int(YGNodeLayoutGetLeft(node))
        y = oy + int(YGNodeLayoutGetTop(node))
        w = int(YGNodeLayoutGetWidth(node))
        h = int(YGNodeLayoutGetHeight(node))

        # Group decorator
        dec_cfg = cfg.get("decorator")
        if dec_cfg:
            is_clip = dec_cfg == "clip" or (isinstance(dec_cfg, dict) and dec_cfg.get("type") == "clip")
            if is_clip:
                # Clip: render children to scratch canvas, then round-clip the result
                child_args = ["-size", f"{w}x{h}", "xc:none"]
                for i, child_cfg in enumerate(cfg.get("items", [])):
                    child_node = YGNodeGetChild(node, i)
                    child_type = child_cfg.get("type", "group")
                    if child_type == "group":
                        self.composite_tree(child_node, child_cfg, leaf_iter, child_args, 0, 0)
                    else:
                        self._composite_leaf(child_node, child_cfg, leaf_iter, child_args, 0, 0)

                tmp_canvas = self.tmp_path()
                magick(*child_args, tmp_canvas)
                radius = self.theme("image", "radius") or 4
                stroke = self.theme("image", "stroke") or "rgba(160,150,140,0.6)"
                stroke_w = self.theme("image", "stroke_width") or 1
                clipped = self._clip_round(tmp_canvas, radius, stroke, stroke_w)
                compose_args += ["(", clipped, ")", "-gravity", "NorthWest",
                                 "-geometry", f"+{x}+{y}", "-composite"]
                return  # children already composited

            dec = self.resolve_decorator(dec_cfg)
            if dec:
                # Box decorator: draw filled box behind content
                box = self._make_box(w, h, dec)
                compose_args += ["(", box, ")", "-gravity", "NorthWest",
                                 "-geometry", f"+{x}+{y}", "-composite"]

        # Composite children
        for i, child_cfg in enumerate(cfg.get("items", [])):
            child_node = YGNodeGetChild(node, i)
            child_type = child_cfg.get("type", "group")

            if child_type == "group":
                self.composite_tree(child_node, child_cfg, leaf_iter, compose_args, x, y)
            else:
                self._composite_leaf(child_node, child_cfg, leaf_iter, compose_args, x, y)

    def _composite_leaf(self, child_node, child_cfg, leaf_iter, compose_args, px, py):
        """Render and composite a single leaf item."""
        leaf_cfg, pre_path = next(leaf_iter)
        cx = px + int(YGNodeLayoutGetLeft(child_node))
        cy = py + int(YGNodeLayoutGetTop(child_node))
        cw = int(YGNodeLayoutGetWidth(child_node))
        ch = int(YGNodeLayoutGetHeight(child_node))

        if cw <= 0 or ch <= 0:
            src = child_cfg.get("src", child_cfg.get("text", "?"))
            print(f"WARNING: zero-size item ({cw}x{ch}): {src}", file=sys.stderr)
            return

        child_type = child_cfg.get("type")

        if child_type == "image":
            path = self.render_image(leaf_cfg, cw)
        elif child_type == "label" and pre_path:
            path = pre_path
        else:
            return

        compose_args += ["(", path, ")", "-gravity", "NorthWest",
                         "-geometry", f"+{cx}+{cy}", "-composite"]

    # ── Page render ──

    def render(self, output_path):
        bg_path = resolve_path(self.g["background"], self.base_dir)
        border_path = resolve_path(self.g["border"], self.base_dir)

        bg = self.tmp_path()
        magick(bg_path, "-resize", f"{self.canvas_w}x{self.canvas_h}!", bg)
        compose_args = [bg]

        if "title" in self.page:
            title = self.make_text(self.page["title"], "title")
            if "subtitle" in self.page:
                subtitle = self.make_text(self.page["subtitle"], "flavour")
                header = self.make_inline(title, subtitle)
            else:
                header = title
            compose_args += ["(", header, ")", "-gravity", "NorthWest",
                             "-geometry", f"+{self.margin+4}+14", "-composite"]

        root_cfg = self.page.get("root", {})
        if root_cfg:
            if "size" not in root_cfg:
                root_cfg["size"] = [self.full_w, self.full_h]

            leaves = []
            root_node = self.build_yoga_tree(root_cfg, leaves)
            YGNodeCalculateLayout(root_node, self.full_w, self.full_h, LTR)
            self.composite_tree(root_node, root_cfg, iter(leaves), compose_args,
                                self.margin, self.top_y)
            YGNodeFreeRecursive(root_node)

        compose_args += ["(", border_path, ")", "-compose", "Over", "-composite",
                         output_path]
        magick(*compose_args)
        print(f"Rendered: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Render showcase page from YAML")
    parser.add_argument("page", help="Path to page YAML file")
    parser.add_argument("--output", "-o", help="Output path (default: same dir, .png)")
    args = parser.parse_args()

    page_path = Path(args.page).resolve()
    base_dir = page_path.parent

    globals_path = base_dir / "globals.yaml"
    if not globals_path.exists():
        print(f"Error: globals.yaml not found in {base_dir}", file=sys.stderr)
        sys.exit(1)

    with open(globals_path) as f:
        globals_cfg = yaml.safe_load(f)
    with open(page_path) as f:
        page_cfg = yaml.safe_load(f)

    output = args.output or str(page_path.with_suffix(".png"))
    Renderer(globals_cfg, page_cfg, base_dir).render(output)


if __name__ == "__main__":
    main()
