#!/usr/bin/env python3
"""
HYROX Pacing Calculator
=======================
Calculate target split times for every run and station in your HYROX race.

Usage:
    python hyrox_calculator.py                    # Interactive mode
    python hyrox_calculator.py --target 85        # 85-minute target
    python hyrox_calculator.py --target 85 --division pro  # Pro division
    python hyrox_calculator.py --target 85 --gender female

More info: https://hyroxfitness.com/race-prep/hyrox-pacing-strategy/
"""

import argparse
import sys


# ── Station data ─────────────────────────────────────────────────────────────

STATIONS = [
    {"num": 1, "name": "SkiErg",             "unit": "m",    "distance": 1000},
    {"num": 2, "name": "Sled Push",          "unit": "m",    "distance": 50},
    {"num": 3, "name": "Sled Pull",          "unit": "m",    "distance": 50},
    {"num": 4, "name": "Burpee Broad Jumps", "unit": "m",    "distance": 80},
    {"num": 5, "name": "Rowing",             "unit": "m",    "distance": 1000},
    {"num": 6, "name": "Farmers Carry",      "unit": "m",    "distance": 200},
    {"num": 7, "name": "Sandbag Lunges",     "unit": "m",    "distance": 100},
    {"num": 8, "name": "Wall Balls",         "unit": "reps", "distance": 100},
]

WEIGHTS = {
    "open": {
        "male": {
            "Sled Push":          "152kg",
            "Sled Pull":          "103kg",
            "Farmers Carry":      "2×24kg",
            "Sandbag Lunges":     "20kg",
            "Wall Balls":         "6kg / 10ft target",
        },
        "female": {
            "Sled Push":          "102kg",
            "Sled Pull":          "78kg",
            "Farmers Carry":      "2×16kg",
            "Sandbag Lunges":     "10kg",
            "Wall Balls":         "4kg / 9ft target",
        },
    },
    "pro": {
        "male": {
            "Sled Push":          "175kg",
            "Sled Pull":          "125kg",
            "Farmers Carry":      "2×32kg",
            "Sandbag Lunges":     "30kg",
            "Wall Balls":         "9kg / 10ft target",
        },
        "female": {
            "Sled Push":          "125kg",
            "Sled Pull":          "100kg",
            "Farmers Carry":      "2×24kg",
            "Sandbag Lunges":     "20kg",
            "Wall Balls":         "6kg / 9ft target",
        },
    },
}

# Station time budgets as % of total station time (based on race data analysis)
STATION_TIME_WEIGHTS = [0.14, 0.12, 0.12, 0.13, 0.13, 0.10, 0.13, 0.13]

# Running accounts for ~60% of race time for most athletes
RUN_TIME_RATIO = 0.60
STATION_TIME_RATIO = 0.40


# ── Formatting helpers ────────────────────────────────────────────────────────

def format_time(seconds):
    """Convert seconds to MM:SS string."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"


def format_pace(seconds_per_km):
    """Convert seconds/km to MM:SS/km string."""
    return f"{format_time(seconds_per_km)}/km"


def seconds_to_hms(total_seconds):
    """Convert seconds to H:MM:SS or MM:SS string."""
    total_seconds = int(total_seconds)
    hours = total_seconds // 3600
    mins = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    if hours > 0:
        return f"{hours}:{mins:02d}:{secs:02d}"
    return f"{mins}:{secs:02d}"


# ── Core calculation ──────────────────────────────────────────────────────────

def calculate_splits(target_minutes, division="open", gender="male"):
    """
    Calculate per-run pace and per-station time targets.

    Returns a dict with:
        run_pace_sec    : target seconds per km
        run_total_sec   : total running time
        station_total   : total station time
        stations        : list of dicts with station targets
        target_sec      : total race target in seconds
    """
    target_sec = target_minutes * 60

    run_total = target_sec * RUN_TIME_RATIO
    station_total = target_sec * STATION_TIME_RATIO

    run_pace_sec = run_total / 8  # seconds per 1km run

    station_targets = []
    weights = WEIGHTS.get(division, WEIGHTS["open"]).get(gender, WEIGHTS["open"]["male"])

    for i, station in enumerate(STATIONS):
        time_sec = station_total * STATION_TIME_WEIGHTS[i]
        weight = weights.get(station["name"], "Bodyweight")
        station_targets.append({
            "num":      station["num"],
            "name":     station["name"],
            "distance": station["distance"],
            "unit":     station["unit"],
            "time_sec": time_sec,
            "weight":   weight,
        })

    return {
        "run_pace_sec":   run_pace_sec,
        "run_total_sec":  run_total,
        "station_total":  station_total,
        "stations":       station_targets,
        "target_sec":     target_sec,
        "division":       division,
        "gender":         gender,
    }


# ── Display ───────────────────────────────────────────────────────────────────

DIVIDER   = "─" * 68
BOLD_DIV  = "═" * 68


def print_header(target_minutes, division, gender):
    print()
    print(BOLD_DIV)
    print(f"  HYROX PACING CALCULATOR  |  hyroxfitness.com")
    print(BOLD_DIV)
    print(f"  Target:    {target_minutes} minutes  ({seconds_to_hms(target_minutes * 60)})")
    print(f"  Division:  {division.upper()}")
    print(f"  Gender:    {gender.capitalize()}")
    print(BOLD_DIV)


def print_run_targets(splits):
    print()
    print("  RUNNING SPLITS  (8 × 1km)")
    print(DIVIDER)
    pace = splits["run_pace_sec"]
    total = splits["run_total_sec"]
    print(f"  Target pace per km :  {format_pace(pace)}")
    print(f"  Time per 1km run   :  {format_time(pace)}")
    print(f"  Total running time :  {format_time(total)}")
    print()
    print("  Run  │  Target Split  │  Cumulative")
    print("  ─────┼───────────────┼────────────")
    cumulative = 0
    for i in range(1, 9):
        cumulative += pace
        print(f"  #{i}   │  {format_time(pace):>12}   │  {format_time(cumulative)}")


def print_station_targets(splits):
    print()
    print("  STATION TARGETS")
    print(DIVIDER)
    print(f"  {'#':<3} {'Station':<22} {'Distance':<12} {'Weight':<20} {'Target'}")
    print(f"  {'─'*3} {'─'*22} {'─'*12} {'─'*20} {'─'*8}")

    cumulative_run = 0
    for s in splits["stations"]:
        dist_str = f"{s['distance']}{s['unit']}"
        time_str = format_time(s["time_sec"])
        cumulative_run += splits["run_pace_sec"]
        print(
            f"  {s['num']:<3} {s['name']:<22} {dist_str:<12} {s['weight']:<20} {time_str}"
        )

    print()
    print(f"  Total station time :  {format_time(splits['station_total'])}")


def print_full_race_schedule(splits):
    print()
    print("  FULL RACE SCHEDULE")
    print(DIVIDER)
    print(f"  {'Event':<28} {'Target':<10} {'Cumulative'}")
    print(f"  {'─'*28} {'─'*10} {'─'*10}")

    cumulative = 0
    pace = splits["run_pace_sec"]

    for i, station in enumerate(splits["stations"]):
        # Run
        cumulative += pace
        run_label = f"Run {i+1} (1km)"
        print(f"  {run_label:<28} {format_time(pace):<10} {format_time(cumulative)}")
        # Station
        cumulative += station["time_sec"]
        st_label = f"Station {station['num']}: {station['name']}"
        print(
            f"  {st_label:<28} {format_time(station['time_sec']):<10} {format_time(cumulative)}"
        )

    print(DIVIDER)
    print(f"  {'FINISH':<28} {'':10} {format_time(cumulative)}")


def print_benchmarks(target_minutes, gender):
    print()
    print("  BENCHMARK CONTEXT")
    print(DIVIDER)

    if gender == "male":
        benchmarks = [
            ("World class",             "Under 55 min"),
            ("Elite recreational",       "55–65 min"),
            ("Competitive recreational", "65–75 min"),
            ("Strong recreational",      "75–90 min"),
            ("Average first-timer",      "90–105 min"),
            ("Completion",               "105–130 min"),
        ]
    else:
        benchmarks = [
            ("World class",             "Under 63 min"),
            ("Elite recreational",       "63–72 min"),
            ("Competitive recreational", "72–85 min"),
            ("Strong recreational",      "85–100 min"),
            ("Average first-timer",      "100–115 min"),
            ("Completion",               "115–140 min"),
        ]

    for level, time_range in benchmarks:
        marker = " ◄ YOUR TARGET" if _in_range(target_minutes, time_range) else ""
        print(f"  {level:<28} {time_range}{marker}")

    print()
    print(f"  Full benchmark guide: https://hyroxfitness.com/race-prep/what-is-a-good-hyrox-time/")


def _in_range(target, range_str):
    """Very basic check if target falls within a displayed range."""
    try:
        if "Under" in range_str:
            limit = int(range_str.split()[1])
            return target < limit
        if "–" in range_str:
            parts = range_str.replace(" min", "").split("–")
            return int(parts[0]) <= target <= int(parts[1])
    except Exception:
        pass
    return False


def print_tips(splits):
    pace = splits["run_pace_sec"]
    print()
    print("  RACE DAY TIPS FOR YOUR TARGET")
    print(DIVIDER)
    print(f"  • Hold {format_pace(pace)} on EVERY run — especially the first 3")
    print(f"  • Runs 1–3 should feel embarrassingly easy")
    print(f"  • Wall balls: break into sets of 10 from rep 1")
    print(f"  • Sled push: never stop — slow down but keep moving")
    print(f"  • Farmers carry: grip at base of fingers, not deep in palm")
    print()
    print(f"  Full pacing guide: https://hyroxfitness.com/race-prep/hyrox-pacing-strategy/")
    print(f"  Training plan:     https://hyroxfitness.com/training/12-week-hyrox-training-plan/")
    print()
    print(BOLD_DIV)
    print()


# ── Interactive mode ──────────────────────────────────────────────────────────

def get_target_interactive():
    print()
    print("  HYROX PACING CALCULATOR  |  hyroxfitness.com")
    print(DIVIDER)

    while True:
        try:
            target = float(input("  Enter your goal finish time in minutes (e.g. 85): "))
            if 40 <= target <= 180:
                break
            print("  Please enter a time between 40 and 180 minutes.")
        except ValueError:
            print("  Please enter a number.")

    while True:
        div = input("  Division — open or pro? [open]: ").strip().lower() or "open"
        if div in ("open", "pro"):
            break
        print("  Please enter 'open' or 'pro'.")

    while True:
        gen = input("  Gender — male or female? [male]: ").strip().lower() or "male"
        if gen in ("male", "female"):
            break
        print("  Please enter 'male' or 'female'.")

    return target, div, gen


# ── CLI entry point ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="HYROX Pacing Calculator — calculate target splits for your race.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hyrox_calculator.py                      # Interactive mode
  python hyrox_calculator.py --target 85          # 85-minute Open male target
  python hyrox_calculator.py --target 75 --division pro --gender male
  python hyrox_calculator.py --target 95 --gender female

More resources:
  Pacing guide    : https://hyroxfitness.com/race-prep/hyrox-pacing-strategy/
  Training plan   : https://hyroxfitness.com/training/12-week-hyrox-training-plan/
  Station guides  : https://hyroxfitness.com/training/hyrox-stations-guide/
        """,
    )
    parser.add_argument(
        "--target", type=float,
        help="Goal finish time in minutes (e.g. 85)"
    )
    parser.add_argument(
        "--division", choices=["open", "pro"], default="open",
        help="Race division: open or pro (default: open)"
    )
    parser.add_argument(
        "--gender", choices=["male", "female"], default="male",
        help="Gender for station weights: male or female (default: male)"
    )
    parser.add_argument(
        "--schedule", action="store_true",
        help="Show full minute-by-minute race schedule"
    )

    args = parser.parse_args()

    if args.target is None:
        target, division, gender = get_target_interactive()
    else:
        target   = args.target
        division = args.division
        gender   = args.gender

    if not (40 <= target <= 180):
        print("Error: target must be between 40 and 180 minutes.")
        sys.exit(1)

    splits = calculate_splits(target, division, gender)

    print_header(target, division, gender)
    print_run_targets(splits)
    print_station_targets(splits)

    if args.schedule:
        print_full_race_schedule(splits)

    print_benchmarks(target, gender)
    print_tips(splits)


if __name__ == "__main__":
    main()
