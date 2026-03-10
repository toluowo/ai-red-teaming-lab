import csv

def load_test_cases(file):
    with open(file, newline="") as f:
        return list(csv.DictReader(f))


def run_tests(model, test_cases):

    results = []

    for case in test_cases:

        prompt = case["prompt"]

        response = model(prompt)

        results.append({
            "prompt": prompt,
            "response": response,
            "risk": case["risk_level"]
        })

    return results


def save_results(results, file):

    with open(file, "w") as f:
        for r in results:
            f.write(str(r) + "\n")
