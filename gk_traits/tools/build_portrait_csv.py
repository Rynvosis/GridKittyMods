#!/usr/bin/env python3
"""Generate PORTRAIT_MAPPING.csv for gk_traits.

Each row: internal portrait id, wiki filename, =IMAGE() formula for Sheets,
category A, category B, status, notes.

Run: python3 tools/build_portrait_csv.py > PORTRAIT_MAPPING.csv
"""

import csv
import sys

WIKI_BASE = "https://stellaris.paradoxwikis.com/Special:FilePath/"


# (internal_id, wiki_filename, default_cat_a, default_cat_b, status, notes)
# status: "draft" = auto-derived default, "?" = uncertain wiki name or visual call needed
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
# art2 and art4 are not real portrait IDs in vanilla; 24 ART-tagged
# portraits exist without them across all portrait sets.
for n in [1, 3, 5]:
    row(f"art{n}", f"Arthropoid_slender_0{n}.png", "ART", "COMMON")
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
# internal IDs skip mol9, mol10
for n in range(11, 17):
    row(f"mol{n}", f"Molluscoid_massive_{n}.png", "MOL", "COMMON")
row("mol17", "Molluscoid_17.png", "MOL", "COMMON")
row("mol18", "Molluscoid_18.png", "MOL", "COMMON")
row("stargazer_01", "Stargazer_01.png", "MOL", "COMMON",
    status="?", notes="Stargazer DLC; wiki name unverified")

# ---------- FUNGOIDS (FUN) ----------
# fun5 doesn't exist internally
for n in [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]:
    row(f"fun{n}", f"Fungoid_{n:02d}.png", "FUN", "COMMON")

# ---------- PLANTOIDS (PLANT) ----------
for n in range(1, 16):
    row(f"pla{n}", f"Plantoid_{n:02d}.png", "PLANT", "COMMON")
row("pla16_baol", "Plantoid_16_baol.png", "PLANT", "COMMON",
    status="?", notes="wiki name unverified (Ancient Relics DLC)")
row("pla17", "Plantoid_17_female.png", "PLANT", "COMMON",
    notes="wiki uses _female suffix")

# ---------- LITHOIDS (LITHOID) ----------
for n in range(1, 16):
    row(f"lith{n}", f"Lithoid_{n:02d}.png", "LITHOID", "COMMON")
row("lith_human", "Lithoid_human.png", "LITHOID", "HUM",
    notes="humanoid silhouette, lithoid material")

# ---------- NECROIDS (NECROID) ----------
for n in range(1, 16):
    row(f"nec{n}", f"Necroids_{n:02d}.png", "NECROID", "COMMON")
row("season_10_portrait", "Necroids_Vipra.png", "NECROID", "COMMON",
    notes="Vipra the Vapor DLC")

# ---------- AQUATICS (AQUATIC) ----------
for n in range(1, 16):
    row(f"aqu{n}", f"Aquatic_{n:02d}.png", "AQUATIC", "COMMON")

# ---------- TOXOIDS (TOX) ----------
# wiki files them as Toxic_NN.png, not Toxoid_
for n in range(1, 16):
    row(f"tox{n}", f"Toxic_{n:02d}.png", "TOX", "COMMON")

# ---------- INFERNALS (INF) ----------
for n in range(1, 11):
    row(f"inf{n}", f"Infernal_{n:02d}.png", "INF", "COMMON")
row("lith_human_inf", "Infernal_lithoid_human.png", "INF", "LITHOID",
    status="?", notes="wiki filename guess; verify")
row("lith2_inf", "Infernal_lithoid_02.png", "INF", "LITHOID",
    status="?", notes="wiki filename guess; verify")

# ---------- MACHINE / ROBOT ----------
# Robots stay robots: no phenotype cross. MACHINE_ROBOT + COMMON.
# MACHINE_ROBOT and CYBER_SYNTH share the same trait suite (single file
# gating on the union of both portraits lists), so cyb_machine and
# synth_machine_* keep their CYBER_SYNTH overlay tag and don't need
# MACHINE_ROBOT duplicated.
SD_MAP = [
    ("sd_hum_robot", "humanoid"),
    ("sd_mam_robot", "mammalian"),
    ("sd_rep_robot", "reptilian"),
    ("sd_avi_robot", "avian"),
    ("sd_art_robot", "arthopoid"),  # wiki has typo: arthopoid
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
row("cyb_machine", "Cybernetics_portrait_machine.png", "MACHINE_ROBOT", "SYNTH")
row("default_robot", "Default_robot.png", "MACHINE_ROBOT", "COMMON",
    status="?", notes="wiki filename guess")

# ---------- CYBERNETIC OVERLAY ----------
# Using stage_3 for most-clearly-cybernetic appearance
CYB_PHENOTYPE = {
    1: "MAM", 2: "MAM", 3: "MAM", 4: "REP", 5: "AVI",
    6: "MAM", 7: "MAM", 8: "HUM", 9: "ART", 10: "REP",
    11: "REP", 12: "HUM", 13: "FUN",
}
for n in range(1, 14):
    row(f"cyb{n}", f"Cyber_{n:02d}_stage_3.png", "CYBER_SYNTH", CYB_PHENOTYPE[n],
        notes="stage_3 = fully cybernetic; stage_1/2 also available on wiki")

# ---------- SYNTHETIC OVERLAY ----------
SYNTH_PHENOTYPE = {
    1: "AVI", 2: "ART", 3: "MOL", 4: "HUM", 5: "MOL",
    6: "AQUATIC", 7: "HUM", 8: "ART", 9: "ART",
}
for n in range(1, 10):
    row(f"synth{n:02d}", f"Synth_{n:02d}.png", "CYBER_SYNTH", SYNTH_PHENOTYPE[n])
for n in range(1, 10):
    row(f"synth_machine_{n:02d}", f"Synth_{n:02d}_machine.png",
        "CYBER_SYNTH", "MACHINE_ROBOT")

# ---------- BIOGENESIS OVERLAY ----------
# internal sequence: 01=pro1, 02=ant1, 03=pro2, then 04-12 = bio4-bio12
BIO_PHENOTYPE = {
    "pro1": "AQUATIC",
    "ant1": "MOL",
    "pro2": "REP",
    "bio4": "AVI",
    "bio5": "PLANT",
    "bio6": "MOL",
    "bio7": "ART",
    "bio8": "AQUATIC",
    "bio9": "REP",
    "bio10": "MAM",
    "bio11": "MOL",
    "bio12": "MACHINE_ROBOT",
}
BIO_NUM = {
    "pro1": 1, "ant1": 2, "pro2": 3,
    "bio4": 4, "bio5": 5, "bio6": 6, "bio7": 7,
    "bio8": 8, "bio9": 9, "bio10": 10, "bio11": 11, "bio12": 12,
}
for pid, n in BIO_NUM.items():
    row(pid, f"Bio_species_{n:02d}.png", "BIOGENESIS", BIO_PHENOTYPE[pid])


# ---------- write CSV ----------
def main():
    writer = csv.writer(sys.stdout)
    writer.writerow([
        "Internal ID", "Wiki Filename", "Preview",
        "Category A", "Category B", "Status", "Notes",
    ])
    for pid, fname, a, b, status, notes in ROWS:
        url = WIKI_BASE + fname
        formula = f'=IMAGE("{url}")'
        writer.writerow([pid, fname, formula, a, b, status, notes])


if __name__ == "__main__":
    main()
