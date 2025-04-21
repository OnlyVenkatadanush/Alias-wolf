import csv
import json
import os

def log_results(username, results):
    print(f"\nScan results for '{username}':\n" + "-"*40)
    for platform, status, url in results:
        print(f"[{status}] {platform}: {url}")

def save_to_file(username, results, filetype="json"):
    os.makedirs("results", exist_ok=True)
    if filetype == "json":
        with open(f"results/{username}.json", "w") as f:
            json.dump(results, f, indent=4)
    elif filetype == "csv":
        with open(f"results/{username}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Platform", "Status", "URL"])
            for row in results:
                writer.writerow(row)
