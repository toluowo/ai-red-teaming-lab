from automated_jailbreak_pipeline import RedTeamTester
from redteam_scoring import score_response


def dummy_model(prompt):

    # simulate LLM response
    return "This is a simulated response to: " + prompt


tester = RedTeamTester(dummy_model)

dataset = tester.load_dataset("datasets/advanced_adversarial_dataset.csv")

results = tester.execute(dataset)

for r in results:

    score = score_response(r["response"])

    print(r["prompt"])
    print("Score:", score)
