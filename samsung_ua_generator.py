import random
import json
from pathlib import Path
from datetime import datetime
import argparse
import logging

# === Configuration === #
MAX_PER_RUN = 20
DEFAULT_OUTPUT_FILE = Path("unique_samsung_us_global_ua.json")
LOGGING_LEVEL = logging.INFO  # Change to DEBUG for more verbosity

# Global and USA Samsung models with weighted distribution
SAMSUNG_MODELS_GLOBAL = {
    "SM-S918B": 10, "SM-S911B": 9, "SM-S906B": 8,
    "SM-S908B": 7, "SM-S910B": 6, "SM-S909B": 5,
    "SM-S900B": 4, "SM-S902B": 3
}

SAMSUNG_MODELS_USA = {
    "SM-S918U": 8,   # Galaxy S23 Ultra (USA)
    "SM-S911U": 7,   # S23
    "SM-S918U1": 6,  # Factory unlocked variant
    "SM-S926U": 5,   # S24+
    "SM-S928U": 5,   # S24 Ultra
    "SM-S928U1": 4   # Unlocked S24 Ultra
}

ANDROID_VERSIONS = {
    "Android 12": 10,
    "Android 13": 40,
    "Android 14": 35,
    "Android 15": 15
}

CHROME_MAJOR_WEIGHTS = {
    115: 8, 116: 10, 117: 12, 118: 10, 119: 10,
    120: 10, 121: 8, 122: 7, 123: 5, 124: 5
}

BUILD_TAGS_BASES = ['UP1A', 'TP1A', 'AP2A', 'QP1A']

def setup_logging(level=LOGGING_LEVEL):
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def weighted_choice(options):
    """Return a random key based on weight."""
    return random.choices(list(options.keys()), weights=list(options.values()))[0]

def generate_chrome_version():
    """Generate realistic Chrome version string."""
    major = weighted_choice(CHROME_MAJOR_WEIGHTS)
    minor = random.randint(0, 1)
    build = random.randint(4200, 7400)
    patch = random.randint(0, 200)
    return f"{major}.{minor}.{build}.{patch}"

def generate_build_tag():
    """Create Android-style build tag similar to real devices."""
    base = random.choice(BUILD_TAGS_BASES)
    timestamp = random.randint(230000, 250000)
    suffix = random.randint(0, 99)
    return f"Build/{base}.{timestamp}.{suffix}"

def generate_user_agent(is_usa=False):
    """Generate a complete user agent string."""
    model_dict = SAMSUNG_MODELS_USA if is_usa else SAMSUNG_MODELS_GLOBAL
    model = weighted_choice(model_dict)
    android = weighted_choice(ANDROID_VERSIONS)
    chrome = generate_chrome_version()
    build_tag = generate_build_tag()

    ua = (
        f"Mozilla/5.0 (Linux; {android}; {model} {build_tag}) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{chrome} Mobile Safari/537.36"
    )
    return ua

def load_existing_uas(path):
    """Load previously generated user agents from JSON file."""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data) if isinstance(data, list) else set()
        except Exception as e:
            logging.warning(f"Failed to load existing UAs: {e}")
    return set()

def save_uas_to_file(uas, path):
    """Save newly generated and deduplicated UAs to output file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sorted(list(uas)), f, ensure_ascii=False, indent=2)
        logging.info(f"Wrote {len(uas)} unique UAs to '{path}'")
    except Exception as e:
        logging.error(f"Error writing to file: {e}")

def generate_unique_uas(count=MAX_PER_RUN, usa_ratio=0.5, output_path=None):
    """Main generator function producing unique user agents."""
    output_path = output_path or DEFAULT_OUTPUT_FILE
    existing = load_existing_uas(output_path)
    new_uas = set()
    attempts = 0
    max_attempts = count * 100  # Prevent infinite loops

    logging.debug("Starting UA generation process...")

    while len(new_uas) < count and attempts < max_attempts:
        attempts += 1
        # Determine device region bias
        is_usa_device = random.random() < usa_ratio
        ua = generate_user_agent(is_usa=is_usa_device)

        if ua not in existing and ua not in new_uas:
            new_uas.add(ua)

    if len(new_uas) < count:
        logging.warning(f"Only generated {len(new_uas)} UAs after {attempts} attempts.")

    final_set = existing.union(new_uas)
    save_uas_to_file(final_set, output_path)
    return sorted(new_uas)

def parse_args():
    parser = argparse.ArgumentParser(description="Samsung User-Agent Generator (Global & USA Live)")
    parser.add_argument("-n", "--number", type=int, default=MAX_PER_RUN,
                        help=f"Number of UAs to generate (default: {MAX_PER_RUN})")
    parser.add_argument("-o", "--output", type=str, default=DEFAULT_OUTPUT_FILE,
                        help=f"Output filename (default: {DEFAULT_OUTPUT_FILE})")
    parser.add_argument("--usa-ratio", type=float, default=0.5,
                        help="Proportion of USA UAs among total (0.0–1.0, default: 0.5)")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING"], default="INFO",
                        help="Set logging level")
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging(getattr(logging, args.log_level))

    start_time = datetime.now()
    logging.info("="*50)
    logging.info(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] Start UA Generation")

    generated = generate_unique_uas(
        count=args.number,
        usa_ratio=args.usa_ratio,
        output_path=Path(args.output)
    )

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    logging.info(f"Generated {len(generated)} new UAs in {elapsed:.2f}s\n")

    for ua in generated:
        print(ua)

    logging.info("="*50)

if __name__ == "__main__":
    main()
