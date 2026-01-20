def calculate_audit_score(followers: int, avg_views: int, engagement: float):
    score = 100

    if avg_views < followers * 0.05:
        score -= 30

    if engagement < 1:
        score -= 30

    if score >= 80:
        label = "Good"
    elif score >= 60:
        label = "Medium Risk"
    else:
        label = "High Risk"

    return score, label
