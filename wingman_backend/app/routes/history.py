from fastapi import APIRouter
from app.services.supabase import get_user_history

router = APIRouter()

@router.get("/history/{user_id}")
async def get_history(user_id: str, limit: int = 20):
    try:
        history = get_user_history(user_id, limit)
        return {
            "history": history,
            "count": len(history),
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}