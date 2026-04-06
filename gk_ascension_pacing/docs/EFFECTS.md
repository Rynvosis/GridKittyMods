# GK Ascension Pacing — Effects Reference

## System 1: Ascension Speed Scaling

All ascension situations have their base progress rate dynamically scaled by game year.

**Formula:** `base_rate * (years_passed² / 5000 + 0.5)`, capped at 2.5x

| Year | Speed Multiplier |
|------|-----------------|
| 2200 | 0.50x |
| 2230 | 0.68x |
| 2250 | 1.00x (vanilla) |
| 2260 | 1.22x |
| 2280 | 1.78x |
| 2300 | 2.50x (cap) |

Uses `set` on the base rate — approach percentage bonuses (+20% overdrive etc.) scale off the modified base, not the vanilla base.

### Affected Situations

- `genetic_ascension_situation` / `_hive` (Bio)
- `situation_breach_shroud` (Psionic)
- `situation_cyberization` / `_hive` (Cybernetic)
- `situation_cybernetic_creed_cyberization` (Cybernetic Creed)
- `situation_digitization` (Synthetic)
- `situation_transformation` (Machine)

## System 2: Patience Bonus

Empires without an ascension path gain scaling bonuses from year 2240, ramping from zero.

**Base (at multiplier 1.0):** +10% job output, +20% founder species growth, +20% assembly

**Scaling:** `sqrt(years_since_2240) * 0.25`

| Year | Job Output | Growth/Assembly |
|------|-----------|-----------------|
| 2240 | 0% | 0% |
| 2250 | +7.9% | +15.8% |
| 2260 | +11.2% | +22.4% |
| 2275 | +14.8% | +29.6% |
| 2300 | +19.4% | +38.8% |

**On ascension:** Multiplier is halved and locked in permanently. Ascending before 2240 gives no patience bonus.
