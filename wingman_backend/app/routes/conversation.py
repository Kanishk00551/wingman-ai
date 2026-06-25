from fastapi import APIRouter
from app.models.requests import ConversationRequest
from app.services.claude import generate_conversation_suggestions
from app.services.supabase import save_analysis, check_and_increment_usage

router = APIRouter()

@router.post("/conversation-suggest")
async def conversation_suggest(req: ConversationRequest):
    try:
        usage = await check_and_increment_usage(
            req.user_id, "conversation"
        )
        if not usage["allowed"]:
            return {"status": "limit_reached", "message": usage["message"]}

        suggestions = generate_conversation_suggestions(
            req.conversation,
            req.match_name,
            req.user_city,
            req.user_style
        )

        if req.user_id:
            await save_analysis(
                user_id=req.user_id,
                analysis_type="conversation",
                input_text=req.conversation,
                output_text=suggestions
            )

        return {"suggestions": suggestions, "status": "success"}

    except Exception as e:
        return {"suggestions": "", "status": "error", "message": str(e)}