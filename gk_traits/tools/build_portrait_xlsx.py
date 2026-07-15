#!/usr/bin/env python3
"""Generate PORTRAIT_MAPPING.xlsx for gk_traits.

Stdlib-only xlsx writer (no openpyxl/xlsxwriter required). Builds the minimal
OPC zip structure with one sheet whose Preview column holds IMAGE() formulas
that Google Sheets evaluates on import.

Run: python3 tools/build_portrait_xlsx.py path/to/output.xlsx
"""

import sys
import zipfile
from xml.sax.saxutils import escape

WIKI_BASE = "https://stellaris.paradoxwikis.com/Special:FilePath/"

# (internal_id, wiki_filename, cat_a, cat_b, status, notes)
ROWS = []


def row(pid, fname, a, b, status="draft", notes=""):
    ROWS.append((pid, fname, a, b, status, notes))


# ---------- HUMANOIDS (HUM) ----------
row("human", "Human_updated_version.png", "HUM", "COMMON")
row("human_legacy", "Human_legacy_version.png", "HUM", "COMMON")
for n in [2, 3, 4, 5]:
    row(f"humanoid_0{n}", f"Humanoid_0{n}.png", "HUM", "COMMON")
for n in [1, 2] + list(range(6, 15)) + [16]:
    row(f"humanoid_hp_{n:02d}", f"Humanoid_hp_{n:02d}.png", "HUM", "COMMON",
        notes=("internal has hp_14 but wiki may use hp_15; verify" if n == 14 else ""))
row("humanoid_elf", "Humanoid_elf.png", "HUM", "COMMON")

# ---------- MAMMALIANS (MAM) ----------
for n in range(1, 6):
    row(f"mam{n}", f"Mammalian_slender_0{n}.png", "MAM", "COMMON")
for n in range(6, 11):
    row(f"mam{n}", f"Mammalian_normal_{n:02d}.png", "MAM", "COMMON")
for n in range(11, 18):
    row(f"mam{n}", f"Mammalian_massive_{n}.png", "MAM", "COMMON")
row("mam_rat", "Mammalian_ratling.png", "MAM", "COMMON", notes="rat-themed novelty")
for n in range(1, 11):
    row(f"mammalian_ar_{n:02d}", f"Mammalian_ar_{n:02d}.png", "MAM", "COMMON",
        notes="Astral Rifts variant")

# ---------- REPTILIANS (REP) ----------
for n in range(1, 6):
    row(f"rep{n}", f"Reptilian_slender_0{n}.png", "REP", "COMMON")
for n in range(6, 11):
    row(f"rep{n}", f"Reptilian_normal_{n:02d}.png", "REP", "COMMON")
for n in range(11, 16):
    row(f"rep{n}", f"Reptilian_massive_{n}.png", "REP", "COMMON")
row("rep16", "Reptilian_16.png", "REP", "COMMON", notes="Leviathans DLC")
row("rep17", "Reptilian_17.png", "REP", "COMMON")
row("pdx_signup_portrait_01", "Reptilian_Behemothkin.png", "REP", "BIOGENESIS",
    notes="PDX account login Behemothkin; Behemoth lore is biogenesis-themed")

# ---------- AVIANS (AVI) ----------
for n in range(1, 6):
    row(f"avi{n}", f"Avian_slender_0{n}.png", "AVI", "COMMON")
for n in range(6, 11):
    row(f"avi{n}", f"Avian_normal_{n:02d}.png", "AVI", "COMMON")
for n in range(11, 18):
    row(f"avi{n}", f"Avian_massive_{n}.png", "AVI", "COMMON")
row("avi18", "Avian_18.png", "AVI", "COMMON")

# ---------- ARTHROPOIDS (ART) ----------
for n in range(1, 6):
    row(f"art{n}", f"Arthropoid_slender_0{n}.png", "ART", "COMMON",
        status=("?" if n in (2, 4) else "draft"),
        notes=("wiki may not have this exact file; verify" if n in (2, 4) else ""))
for n in range(6, 11):
    row(f"art{n}", f"Arthropoid_normal_{n:02d}.png", "ART", "COMMON")
for n in range(11, 18):
    row(f"art{n}", f"Arthropoid_massive_{n}.png", "ART", "COMMON")
for n in [18, 19, 20]:
    row(f"art{n}", f"Arthropoid_{n}.png", "ART", "COMMON")

# ---------- MOLLUSCOIDS (MOL) ----------
for n in range(1, 6):
    row(f"mol{n}", f"Molluscoid_slender_0{n}.png", "MOL", "COMMON")
for n in range(6, 9):
    row(f"mol{n}", f"Molluscoid_normal_{n:02d}.png", "MOL", "COMMON")
for n in range(11, 17):
    row(f"mol{n}", f"Molluscoid_massive_{n}.png", "MOL", "COMMON")
row("mol17", "Molluscoid_17.png", "MOL", "COMMON")
row("mol18", "Molluscoid_18.png", "MOL", "COMMON")
row("stargazer_01", "Stargazer_01.png", "MOL", "COMMON",
    status="?", notes="Stargazer DLC; wiki name unverified")

# ---------- FUNGOIDS (FUN) ----------
for n in [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]:
    row(f"fun{n}", f"Fungoid_{n:02d}.png", "FUN", "COMMON")

# ---------- PLANTOIDS (PLANT) ----------
for n in range(1, 16):
    row(f"pla{n}", f"Plantoid_{n:02d}.png", "PLANT", "COMMON")
row("pla16_baol", "Plantoid_16_baol.png", "PLANT", "COMMON",
    status="?", notes="wiki name unverified (Ancient Relics DLC)")
row("pla17", "Plantoid_17_female.png", "PLANT", "COMMON",
    notes="wiki uses _female suffix")

# ---------- LITHOIDS ----------
for n in range(1, 16):
    row(f"lith{n}", f"Lithoid_{n:02d}.png", "LITHOID", "COMMON")
row("lith_human", "Lithoid_human.png", "LITHOID", "HUM",
    notes="humanoid silhouette, lithoid material")

# ---------- NECROIDS ----------
for n in range(1, 16):
    row(f"nec{n}", f"Necroids_{n:02d}.png", "NECROID", "COMMON")
row("season_10_portrait", "Necroids_Vipra.png", "NECROID", "COMMON",
    notes="Vipra the Vapor DLC")

# ---------- AQUATICS ----------
for n in range(1, 16):
    row(f"aqu{n}", f"Aquatic_{n:02d}.png", "AQUATIC", "COMMON")

# ---------- TOXOIDS ----------
for n in range(1, 16):
    row(f"tox{n}", f"Toxic_{n:02d}.png", "TOX", "COMMON")

# ---------- INFERNALS ----------
for n in range(1, 11):
    row(f"inf{n}", f"Infernal_{n:02d}.png", "INF", "COMMON")
row("lith_human_inf", "Infernal_lithoid_human.png", "INF", "LITHOID",
    status="?", notes="wiki filename guess; verify")
row("lith2_inf", "Infernal_lithoid_02.png", "INF", "LITHOID",
    status="?", notes="wiki filename guess; verify")

# ---------- MACHINE / ROBOT ----------
SD_MAP = [
    ("sd_hum_robot", "humanoid"),
    ("sd_mam_robot", "mammalian"),
    ("sd_rep_robot", "reptilian"),
    ("sd_avi_robot", "avian"),
    ("sd_art_robot", "arthopoid"),
    ("sd_mol_robot", "molluscoid"),
    ("sd_fun_robot", "fungoid"),
    ("sd_pla_robot", "plantoid"),
]
for pid, wikipart in SD_MAP:
    note = "wiki filename has typo (arthopoid)" if wikipart == "arthopoid" else ""
    row(pid, f"Synthetic_dawn_portrait_{wikipart}.png", "MACHINE_ROBOT", "COMMON",
        notes=note)
row("lith_machine", "Lithoid_machine.png", "MACHINE_ROBOT", "COMMON")
row("nec_machine", "Necroids_machine.png", "MACHINE_ROBOT", "COMMON")
row("aqu_machine", "Aquatic_machine.png", "MACHINE_ROBOT", "COMMON")
row("tox_machine", "Toxic_machine.png", "MACHINE_ROBOT", "COMMON")
row("cyb_machine", "Cybernetics_portrait_machine.png", "MACHINE_ROBOT", "CYBER_SYNTH")
row("default_robot", "Default_robot.png", "MACHINE_ROBOT", "COMMON",
    status="?", notes="wiki filename guess")

# ---------- CYBERNETIC ----------
CYB_PHENOTYPE = {
    1: "MAM", 2: "MAM", 3: "MAM", 4: "REP", 5: "AVI",
    6: "MAM", 7: "MAM", 8: "HUM", 9: "ART", 10: "REP",
    11: "REP", 12: "HUM", 13: "FUN",
}
for n in range(1, 14):
    row(f"cyb{n}", f"Cyber_{n:02d}_stage_3.png", "CYBER_SYNTH", CYB_PHENOTYPE[n],
        notes="stage_3 = fully cybernetic")

# ---------- SYNTHETIC ----------
SYNTH_PHENOTYPE = {
    1: "AVI", 2: "ART", 3: "MOL", 4: "HUM", 5: "MOL",
    6: "AQUATIC", 7: "HUM", 8: "ART", 9: "ART",
}
for n in range(1, 10):
    row(f"synth{n:02d}", f"Synth_{n:02d}.png", "CYBER_SYNTH", SYNTH_PHENOTYPE[n])
for n in range(1, 10):
    row(f"synth_machine_{n:02d}", f"Synth_{n:02d}_machine.png",
        "CYBER_SYNTH", "MACHINE_ROBOT")

# ---------- BIOGENESIS ----------
BIO_PHENOTYPE = {
    "pro1": "AQUATIC", "ant1": "MOL", "pro2": "REP",
    "bio4": "AVI", "bio5": "PLANT", "bio6": "MOL", "bio7": "ART",
    "bio8": "AQUATIC", "bio9": "REP", "bio10": "MAM", "bio11": "MOL",
    "bio12": "MACHINE_ROBOT",
}
BIO_NUM = {
    "pro1": 1, "ant1": 2, "pro2": 3,
    "bio4": 4, "bio5": 5, "bio6": 6, "bio7": 7,
    "bio8": 8, "bio9": 9, "bio10": 10, "bio11": 11, "bio12": 12,
}
for pid, n in BIO_NUM.items():
    row(pid, f"Bio_species_{n:02d}.png", "BIOGENESIS", BIO_PHENOTYPE[pid])


# ---------- XLSX assembly ----------
COL_LETTERS = ["A", "B", "C", "D", "E", "F"]


def col_ref(col_idx, row_num):
    return f"{COL_LETTERS[col_idx]}{row_num}"


def text_cell(ref, value):
    v = escape(str(value))
    return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{v}</t></is></c>'


def formula_cell(ref, formula):
    # formula passed WITHOUT leading "=" (xlsx convention)
    f = escape(formula)
    return f'<c r="{ref}"><f>{f}</f></c>'


def build_sheet_xml():
    rows_xml = []

    # Header row
    headers = ["Internal ID", "Preview", "Category A", "Category B", "Status", "Notes"]
    cells = [text_cell(col_ref(i, 1), h) for i, h in enumerate(headers)]
    rows_xml.append(f'<row r="1">{"".join(cells)}</row>')

    # Data rows
    for idx, (pid, fname, a, b, status, notes) in enumerate(ROWS, start=2):
        url = WIKI_BASE + fname
        # IMAGE() wraps the URL string. xlsx <f> tag stores formula without leading =
        formula = f'IMAGE("{url}")'

        cells = [
            text_cell(col_ref(0, idx), pid),
            formula_cell(col_ref(1, idx), formula),
            text_cell(col_ref(2, idx), a),
            text_cell(col_ref(3, idx), b),
            text_cell(col_ref(4, idx), status),
            text_cell(col_ref(5, idx), notes),
        ]
        rows_xml.append(f'<row r="{idx}">{"".join(cells)}</row>')

    body = "".join(rows_xml)

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <cols>
    <col min="1" max="1" width="22" customWidth="1"/>
    <col min="2" max="2" width="14" customWidth="1"/>
    <col min="3" max="4" width="16" customWidth="1"/>
    <col min="5" max="5" width="10" customWidth="1"/>
    <col min="6" max="6" width="60" customWidth="1"/>
  </cols>
  <sheetData>{body}</sheetData>
</worksheet>'''


CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>'''

ROOT_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''

WORKBOOK_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Portraits" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>'''

WORKBOOK_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>'''


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "PORTRAIT_MAPPING.xlsx"
    sheet_xml = build_sheet_xml()

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("xl/workbook.xml", WORKBOOK_XML)
        z.writestr("xl/_rels/workbook.xml.rels", WORKBOOK_RELS)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)

    print(f"wrote {out_path} ({len(ROWS)} rows)", file=sys.stderr)


if __name__ == "__main__":
    main()
