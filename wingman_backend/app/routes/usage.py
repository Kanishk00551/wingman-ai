from fastapi import APIRouter

from app.services.supabase import get_user_usage

router = APIRouter()

@router.get("/usage/{user_id}")
async def get_usage(user_id: str):
    try:
        data = get_user_usage(user_id)
        return {**data, "status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}