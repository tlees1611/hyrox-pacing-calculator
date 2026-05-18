# HYROX Pacing Calculator 🏃

A command-line tool that calculates target split times for every run and station in your HYROX race. Works for Open and Pro divisions, male and female, any goal time from 40 to 180 minutes.

```
════════════════════════════════════════════════════════════════════
  HYROX PACING CALCULATOR  |  hyroxfitness.com
════════════════════════════════════════════════════════════════════
  Target:    85.0 minutes  (1:25:00)
  Division:  OPEN
  Gender:    Male
════════════════════════════════════════════════════════════════════

  RUNNING SPLITS  (8 × 1km)
────────────────────────────────────────────────────────────────────
  Target pace per km :  6:22/km
  Time per 1km run   :  6:22
  Total running time :  51:00

  Run  │  Target Split  │  Cumulative
  ─────┼───────────────┼────────────
  #1   │          6:22   │  6:22
  #2   │          6:22   │  12:45
  #3   │          6:22   │  19:07
  #4   │          6:22   │  25:30
  #5   │          6:22   │  31:52
  #6   │          6:22   │  38:15
  #7   │          6:22   │  44:37
  #8   │          6:22   │  51:00

  STATION TARGETS
────────────────────────────────────────────────────────────────────
  #   Station                Distance     Weight               Target
  1   SkiErg                 1000m        Bodyweight           4:45
  2   Sled Push              50m          152kg                4:04
  3   Sled Pull              50m          103kg                4:04
  4   Burpee Broad Jumps     80m          Bodyweight           4:25
  5   Rowing                 1000m        Bodyweight           4:25
  6   Farmers Carry          200m         2×24kg               3:24
  7   Sandbag Lunges         100m         20kg                 4:25
  8   Wall Balls             100reps      6kg / 10ft target    4:25

  Strong recreational    75–90 min ◄ YOUR TARGET
```

---

## Installation

No dependencies beyond Python 3.6+. No pip installs required.

```bash
git clone https://github.com/YOUR_USERNAME/hyrox-pacing-calculator.git
cd hyrox-pacing-calculator
python hyrox_calculator.py
```

---

## Usage

### Interactive mode
```bash
python hyrox_calculator.py
```
Prompts you for goal time, division, and gender.

### Command-line mode
```bash
# 85-minute Open male target
python hyrox_calculator.py --target 85

# 75-minute Pro male target with full race schedule
python hyrox_calculator.py --target 75 --division pro --gender male --schedule

# 95-minute Open female target
python hyrox_calculator.py --target 95 --gender female

# 72-minute Pro female — full schedule
python hyrox_calculator.py --target 72 --division pro --gender female --schedule
```

### All options
```
--target     Goal finish time in minutes (e.g. 85)
--division   open or pro (default: open)
--gender     male or female (default: male)
--schedule   Show full minute-by-minute race schedule
```

---

## How the Calculator Works

**Running time** accounts for ~60% of total race time for most HYROX athletes. The remaining 40% is distributed across the 8 stations using weightings derived from real race split data.

**Station time weights** (% of total station budget):

| Station | Weight |
|---|---|
| SkiErg | 14% |
| Sled Push | 12% |
| Sled Pull | 12% |
| Burpee Broad Jumps | 13% |
| Rowing | 13% |
| Farmers Carry | 10% |
| Sandbag Lunges | 13% |
| Wall Balls | 13% |

These weightings reflect average time distributions from Open division race data. Individual athlete profiles will vary — a strong runner might need more station budget, a CrossFit athlete more running budget. Use the outputs as a starting point and adjust based on your own training data.

---

## Station Weights Reference

### Open Division

| Station | Men | Women |
|---|---|---|
| Sled Push (50m) | 152kg | 102kg |
| Sled Pull (50m) | 103kg | 78kg |
| Farmers Carry (200m) | 2×24kg | 2×16kg |
| Sandbag Lunges (100m) | 20kg | 10kg |
| Wall Balls (100 reps) | 6kg / 10ft | 4kg / 9ft |

### Pro Division

| Station | Men | Women |
|---|---|---|
| Sled Push (50m) | 175kg | 125kg |
| Sled Pull (50m) | 125kg | 100kg |
| Farmers Carry (200m) | 2×32kg | 2×24kg |
| Sandbag Lunges (100m) | 30kg | 20kg |
| Wall Balls (100 reps) | 9kg / 10ft | 6kg / 9ft |

SkiErg, Burpee Broad Jumps, and Rowing are bodyweight across all divisions.

---

## Benchmark Times

### Open Division — Men

| Level | Time |
|---|---|
| World class | Under 55 min |
| Elite recreational | 55–65 min |
| Competitive recreational | 65–75 min |
| Strong recreational | 75–90 min |
| Average first-timer | 90–105 min |
| Completion | 105–130 min |

### Open Division — Women

| Level | Time |
|---|---|
| World class | Under 63 min |
| Elite recreational | 63–72 min |
| Competitive recreational | 72–85 min |
| Strong recreational | 85–100 min |
| Average first-timer | 100–115 min |
| Completion | 115–140 min |

Full benchmark guide: [What is a Good HYROX Time?](https://hyroxfitness.com/race-prep/what-is-a-good-hyrox-time/)

---

## Training Resources

- 📋 [Free 12-Week HYROX Training Plan](https://hyroxfitness.com/training/12-week-hyrox-training-plan/)
- ⏱ [HYROX Pacing Strategy Guide](https://hyroxfitness.com/race-prep/hyrox-pacing-strategy/)
- 🏋️ [Complete Guide to All 8 Stations](https://hyroxfitness.com/training/hyrox-stations-guide/)
- 👟 [Best Shoes for HYROX](https://hyroxfitness.com/gear/best-shoes-for-hyrox/)
- 💊 [Best Supplements for HYROX](https://hyroxfitness.com/nutrition/best-supplements-hyrox/)

---

## Also in This Repo

- `hyrox_training_log.csv` — 12-week training log template (import into Excel or Google Sheets)

---

## Contributing

Issues and PRs welcome. If you have real race split data that would improve the station time weightings, please open an issue.

---

## License

MIT — free to use, modify, and share.
