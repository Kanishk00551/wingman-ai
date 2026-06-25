from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from app.services.claude import (
    compress_image,
    generate_profile_audit,
    parse_profile_audit
)
from app.services.supabase import save_analysis, check_and_increment_usage

router = APIRouter()

@router.post("/analyze-profile")
async def analyze_profile(
    files: List[UploadFile] = File(...),
    user_id: str = Form(default=""),
    bio: str = Form(default=""),
    prompts: str = Form(default=""),
    user_city: str = Form(default="Mumbai"),
    target_app: str = Form(default="Hinge")
):
    try:
        # Check usage limit
        usage = await check_and_increment_usage(user_id, "profile_audit")
        if not usage["allowed"]:
            return {"status": "limit_reached", "message": usage["message"]}

        # Process all photos
        image_contents = []
        for file in files:
            contents = await file.read()
            img_base64 = compress_image(contents)
            image_contents.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": img_base64,
                }
            })

        # Generate audit
        raw = generate_profile_audit(
            image_contents, bio, prompts, user_city, target_app
        )
        sections = parse_profile_audit(raw)

        # Save to history
        if user_id:
            await save_analysis(
                user_id=user_id,
                analysis_type="profile_audit",
                input_text=f"bio:{bio} prompts:{prompts}",
                output_text=raw,
                output_sections=sections
            )

        return {"audit": raw, "sections": sections, "status": "success"}

    except Exception as e:
        return {"audit": "", "sections": {}, "status": "error", "message": str(e)}