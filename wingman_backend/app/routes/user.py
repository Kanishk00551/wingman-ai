from fastapi import APIRouter

from app.models.requests import OnboardingRequest
from app.config import supabase_client

from datetime import datetime

router = APIRouter()

@router.post("/user/onboarding")
async def save_onboarding(req: OnboardingRequest):
    try:
        supabase_client.table("users").update({
            "city": req.city,
            "style": req.style,
            "personality": req.personality,
            "dating_goal": req.dating_goal,
            "target_app": req.target_app,
            "updated_at": datetime.now().isoformat()
        }).eq("id", req.user_id).execute()

        return {"status": "success", "message": "Profile saved"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/user/profile/{user_id}")
async def get_profile(user_id: str):
    try:
        res = supabase_client.table("users")\
            .select("*")\
            .eq("id", user_id)\
            .single()\
            .execute()

        return {"user": res.data, "status": "success"}

    except Exception as e:
        return {"status": "error", "message": str(e)}