import argparse
import asyncio
import json
from scanner import scan_user
from utils import log_results, save_to_file

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Username scanner across social media.")
    parser.add_argument("username", nargs="+", help="Username(s) to scan")
    parser.add_argument("--export", choices=["json", "csv"], help="Export results")
    args = parser.parse_args()

    config = load_config()

    for user in args.username:
        results = asyncio.run(scan_user(user, config))
        log_results(user, results)
        if args.export:
            save_to_file(user, results, args.export)

if __name__ == "__main__":
    main()
