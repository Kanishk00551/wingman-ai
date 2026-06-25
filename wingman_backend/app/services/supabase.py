from app.config import supabase_client
from datetime import datetime

FREE_LIMITS = {
    "photo_opener": 3,
    "profile_audit": 1,
    "conversation": 5
}

def get_current_month() -> str:
    return datetime.now().strftime("%Y-%m")

async def save_analysis(
    user_id: str,
    analysis_type: str,
    input_text: str,
    output_text: str,
    output_sections: dict = None
):
    try:
        supabase_client.table("analyses").insert({
            "user_id": user_id,
            "type": analysis_type,
            "input_text": input_text,
            "output_text": output_text,
            "output_sections": output_sections
        }).execute()
    except Exception as e:
        print(f"History save failed: {e}")

async def check_and_increment_usage(
    user_id: str,
    feature: str
) -> dict:
    if not user_id:
        return {"allowed": True, "message": ""}
    try:
        month = get_current_month()
        count_field = f"{feature}_count"

        user_res = supabase_client.table("users")\
            .select("plan")\
            .eq("id", user_id)\
            .single()\
            .execute()

        plan = user_res.data["plan"] if user_res.data else "free"

        if plan != "free":
            return {"allowed": True, "message": ""}

        usage_res = supabase_client.table("usage")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("month", month)\
            .execute()

        current = 0
        if usage_res.data:
            current = usage_res.data[0].get(count_field, 0)

        limit = FREE_LIMITS.get(feature, 3)

        if current >= limit:
            return {
                "allowed": False,
                "message": f"Free limit reached. Upgrade to Pro for unlimited access."
            }

        # Increment
        if usage_res.data:
            supabase_client.table("usage").update({
                count_field: current + 1,
                "total_count": usage_res.data[0]["total_count"] + 1,
                "updated_at": datetime.now().isoformat()
            }).eq("user_id", user_id).eq("month", month).execute()
        else:
            supabase_client.table("usage").insert({
                "user_id": user_id,
                "month": month,
                count_field: 1,
                "total_count": 1
            }).execute()

        return {"allowed": True, "message": ""}

    except Exception as e:
        print(f"Usage check failed: {e}")
        return {"allowed": True, "message": ""}

def get_user_history(user_id: str, limit: int = 20) -> list:
    try:
        res = supabase_client.table("analyses")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return res.data or []
    except Exception as e:
        print(f"History fetch failed: {e}")
        return []

def get_user_usage(user_id: str) -> dict:
    try:
        month = get_current_month()
        res = supabase_client.table("usage")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("month", month)\
            .execute()

        if res.data:
            usage_data = res.data[0]
        else:
            usage_data = {
                "photo_opener_count": 0,
                "profile_audit_count": 0,
                "conversation_count": 0,
                "total_count": 0
            }

        remaining = {
            "photo_opener": max(0, FREE_LIMITS["photo_opener"]
                - usage_data["photo_opener_count"]),
            "profile_audit": max(0, FREE_LIMITS["profile_audit"]
                - usage_data["profile_audit_count"]),
            "conversation": max(0, FREE_LIMITS["conversation"]
                - usage_data["conversation_count"]),
        }

        return {
            "usage": usage_data,
            "remaining": remaining,
            "limits": FREE_LIMITS,
            "month": month
        }
    except Exception as e:
        print(f"Usage fetch failed: {e}")
        return {}