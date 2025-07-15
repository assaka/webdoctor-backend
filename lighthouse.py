import subprocess
import json
import tempfile

def run_lighthouse(url):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        output_path = tmp.name

    command = [
        "lighthouse",
        url,
        "--output=json",
        f"--output-path={output_path}",
        "--chrome-flags=--headless"
    ]

    subprocess.run(command, check=True)

    with open(output_path, "r") as f:
        data = json.load(f)

    scores = {
        "performance": data["categories"]["performance"]["score"],
        "accessibility": data["categories"]["accessibility"]["score"],
        "best_practices": data["categories"]["best-practices"]["score"],
        "seo": data["categories"]["seo"]["score"],
    }

    return scores
