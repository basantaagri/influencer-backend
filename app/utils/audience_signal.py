def compute_audience_signal(influencer: dict):
    engagement = influencer.get("engagement_rate") or 0
    followers = influencer.get("followers") or 0
    price = influencer.get("price") or 0

    # ------------------------
    # DEFAULT
    # ------------------------
    status = "Uncertain"
    confidence = "Low"

    # ------------------------
    # RULE 1: ENGAGEMENT
    # ------------------------
    if engagement >= 2.5:
        status = "Likely Genuine"
        confidence = "High"

    elif 1.0 <= engagement < 2.5:
        status = "Uncertain"
        confidence = "Medium"

    else:  # < 1%
        status = "Needs Review"
        confidence = "High"

    # ------------------------
    # RULE 2: PRICE SANITY (soft modifier)
    # ------------------------
    if followers > 100_000 and price < 2000:
        status = "Needs Review"
        confidence = "High"

    if engagement < 1.5 and price > 50_000:
        status = "Needs Review"
        confidence = "Medium"

    return {
        "status": status,
        "confidence": confidence
    }
