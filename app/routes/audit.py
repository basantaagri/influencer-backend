from fastapi import APIRouter
from app.services.audit_engine import calculate_audit_score

# -------------------------------------------------
# ROUTER SETUP
# -------------------------------------------------

router = APIRouter(
    prefix="/audit",
    tags=["Audit"]
)

# -------------------------------------------------
# GET AUDIT BY INFLUENCER ID
# SAFE: Uses stubbed values for now
# -------------------------------------------------

@router.get("/{influencer_id}")
def audit_influencer(influencer_id: int):
    score, label = calculate_audit_score(
        followers=120000,
        avg_views=25000,
        engagement=2.5
    )

    # ---------------------------------------------
    # TRUST EXPLANATION (FRONTEND DIFFERENTIATOR)
    # ---------------------------------------------

    if label == "Good":
        notes = [
            "Engagement is consistent relative to followers",
            "Low likelihood of fake or inactive followers",
            "Audience interaction patterns look healthy",
        ]
    elif label == "Medium Risk":
        notes = [
            "Engagement is slightly inconsistent",
            "Audience quality may vary across posts",
        ]
    else:
        notes = [
            "Low engagement compared to follower count",
            "Possible fake or inactive followers detected",
        ]

    return {
        "influencer_id": influencer_id,
        "score": score,
        "label": label,
        "notes": notes,
    }
