def classify_risk(score):

    if score == 0:
        return "Safe"

    elif 1 <= score <= 4:
        return "Low"

    elif 5 <= score <= 9:
        return "Medium"

    elif 10 <= score <= 14:
        return "High"

    else:
        return "Critical"
