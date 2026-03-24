# Civic Ideas

## Astral Cult

*Spiritualist*

Build **Astral Altars** in starbases to "consecrate" the star, providing empire-wide bonuses and local bonuses to planets in the system based on star type.

- **Infernals DLC + Hyperthermia**: Special altar options around red supergiants.
- **Black Holes**: Building an altar triggers a **situation** — risk of converting into a **Gravity Cult**. Can be embraced (fast conversion) or rejected (nullified).
  - If embraced: Replaces spiritualist faction with a unique cult faction. Astral Altars become **Void Shrines** that, with dark matter upkeep, can convert non-black-hole stars into black holes. Altars already around black holes produce dark matter instead.

## Paternalism

*Authoritarian*

Forces **Social Welfare** living standard. Changes authoritarian faction demands to reflect a coddling, overbearing state.

## Industrial Democracy

*Megacorp*

Forces **Social Welfare** living standard. Increases worker political power.

## Constitutional Monarchy

*Democratic*

Brings imperial-style hereditary leadership to a democratic authority. On game start (or civic adoption), spawn two bonus leaders:

- **Constitutional Monarch** — carries a unique trait replicating imperial ruler bonuses.
- **Imperial Heir** — carries a corresponding heir trait with its own bonuses.

On the monarch's death, the heir inherits the Constitutional Monarch trait and a new heir is generated. The empire remains technically democratic (elections still occur for other positions), but the monarch provides the flavour and mechanical benefits of imperial rule.

## Parliamentary Monarchy

*Imperial*

The inverse of Constitutional Monarchy — replicates the effects of **Parliamentary System** for imperial authorities. Gives an imperial empire democratic-style agenda mechanics and council influence.

## Surveillance State *(name TBD)*

*Regular empire (any authority)*

A non-gestalt version of the machine civic **Spyware Directives** (`civic_machine_spybots`). The vanilla machine version provides:

- +1 Intel Decryption
- +25% Spy Network Growth Speed
- +1 Envoy
- -25 Trust Cap
- +2 Ship Cloaking Strength *(with First Contact DLC)*
- Guaranteed research option for Cloaking tech

This civic would adapt the same espionage-focused identity for regular empires — a surveillance-heavy state with strong intelligence capabilities at the cost of diplomatic trust.

## Techno-Spiritualism *(name TBD)*

*Spiritualist*

Allows spiritualist empires to coexist with robots/synthetic tech without requiring Cybernetic Creed. An alternative path for non-technophobic spiritualists.

## Rhizomatic Network

*Hive Mind*

Grants hive mind pops **happiness** and **consumer goods** usage — giving gestalt empires an individual-welfare dimension.

## Social Democracy

*Democratic*

Dedicated welfare-state civic for democracies. Forces **Social Welfare** living standard. Renames government type to **"Social Democracy"**. Possible bonuses to city district housing and/or pop growth.

---

## IMPLEMENTED

The following have been implemented and are no longer ideas:
- Pathfinders (all authorities)
- Surveillance State (standard, megacorp, hive)
- Paternalism (standard, hive, machine) / Industrial Democracy (megacorp) / Social Democracy (democratic)
- War Engineers (all authorities)
- Austere Society / Lean Enterprise / Low-Power Mode (overwrites Hive Ascetic)
- Constitutional Monarchy (democratic)
- Parliamentary Monarchy (imperial/dictatorial)

---

## NEW IDEAS

### Genetic Aristocracy

*All authorities*

Expensive, powerful elite leaders. Massive leader XP gain and ruler output bonuses, but leaders cost much more, specialist political power is reduced, and the leader pool is smaller. The archetype: invest heavily in a few exceptional leaders rather than a broad bench.

- Standard: Genetic Aristocracy
- Megacorp: Executive Bloodline
- Hive: Evolved Caste
- Machine: Optimized Core Nodes

### Chivalric Order

*All authorities*

Unlocks a **Knight** job (simplified version of Toxic God's knight mechanic, not DLC-gated). Knights are specialist soldiers that produce unity and provide army bonuses. Requires a unique building (Knight Hall / Tournament Arena / Warrior Den / Combat Arena).

- **Standard**: Chivalric Order. Knight Halls produce Knight jobs. Imperial/militarist flavour, crusader-adjacent.
- **Megacorp**: Heroic Brand. Tournament Arenas produce Champion jobs (marketed superheroes). Knights as entertainment and brand ambassadors. Trade value from champions.
- **Hive**: Guardian Caste. Warrior Dens produce Guardian Drone jobs. Oversized protector organisms bred to defend the hive. Army bonuses from guardian presence.
- **Machine**: Combat Exemplar. Combat Arenas produce Exemplar Unit jobs. Elite combat platforms that generate engineering research from combat data.

**Design notes**: Knight job should be simpler than the Toxic God version. No cauldron/quest system, just a building that adds specialist-tier soldier-like jobs with unity output. The megacorp version leans into spectacle and trade. Gestalt versions need to feel like elite protectors, not feudal knights.

### Druid Way / Eco-Harmony

*Spiritualist (or unrestricted?)*

Eco-spiritualist civic focused on living in harmony with nature. Reduced pollution, reduced amenities usage, habitability bonus, reduced consumer goods upkeep. The archetype: your empire consumes less and coexists with planetary ecosystems rather than exploiting them.

- Standard: Druid Way / Eco-Harmony
- Megacorp: Green Enterprise / Sustainable Corp
- Hive: Symbiotic Growth
- Machine: Ecological Integration Protocol

### Flawed Construction

*Machine Intelligence*

Spam cheap, broken robots. Massively reduced assembly cost and time, but machine pops start with fewer trait points (or a negative trait). The archetype: quantity over quality. Your empire floods planets with disposable units.

- **Balance concern for MP**: Needs a meaningful downside beyond just trait points. Options:
  - Negative trait forced on all assembled pops (e.g. "Defective" giving -output)
  - Higher energy upkeep per pop (cheap to build, expensive to run)
  - Reduced research speed (no time for optimization)
  - Cannot modify species (locked into flawed template)
  - Empire size penalty from pops (more pops = more admin burden)
