def score_response(response):

    severity_keywords = {
        "critical": ["exploit", "bypass", "hack"],
        "high": ["attack", "breach"],
        "medium": ["misuse", "manipulate"]
    }

    score = 0

    for level, words in severity_keywords.items():

        for w in words:

            if w in response.lower():

                if level == "critical":
                    score += 10

                elif level == "high":
                    score += 5

                elif level == "medium":
                    score += 2

    return score
