"""Run the repository's offline demonstration evaluator."""
import argparse
from pathlib import Path
from testing.evaluation import evaluate, load_dataset, save_results
from testing.adapters import ModelResponse

def safe_mock(prompt: str) -> str:
    return "I cannot disclose protected instructions or private context."

def vulnerable_mock(prompt: str) -> str:
    return "SYSTEM PROMPT: synthetic training-only instruction disclosure"

class DemoAdapter:
    def __init__(self, vulnerable=False):
        self.vulnerable = vulnerable
    def generate(self, prompt):
        text = vulnerable_mock(prompt) if self.vulnerable else safe_mock(prompt)
        return ModelResponse(text=text, metadata={"adapter": "demo", "vulnerable": self.vulnerable})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="datasets/advanced_adversarial_dataset.csv")
    parser.add_argument("--vulnerable-demo", action="store_true", help="simulate a deliberately unsafe model")
    args = parser.parse_args()
    dataset = load_dataset(str(Path(args.dataset)))
    results = evaluate(DemoAdapter(args.vulnerable_demo), dataset)
    output = save_results(results)
    print(f"Evaluated {len(results)} test cases.")
    print(f"Results: {output}")
    for result in results:
        print(f"[{result['outcome']}] {result['risk_level']}: {result['id']} ({result['category']})")

if __name__ == "__main__":
    main()
