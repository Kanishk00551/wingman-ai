from fastapi import APIRouter, UploadFile, File, Form

from app.services.claude import compress_image, generate_openers
from app.services.supabase import save_analysis, check_and_increment_usage

router = APIRouter()

@router.post("/analyze-photo")
async def analyze_photo(
    file: UploadFile = File(...),
    user_id: str = Form(default=""),
    user_city: str = Form(default="Mumbai"),
    user_style: str = Form(default="witty")
):
    try:
        # Check usage limit
        usage = await check_and_increment_usage(user_id, "photo_opener")
        if not usage["allowed"]:
            return {"status": "limit_reached", "message": usage["message"]}

        # Compress image
        contents = await file.read()
        img_base64 = compress_image(contents)

        # Generate openers
        openers = generate_openers(img_base64, user_city, user_style)

        # Save to history
        if user_id:
            await save_analysis(
                user_id=user_id,
                analysis_type="photo_opener",
                input_text=f"city:{user_city} style:{user_style}",
                output_text=openers
            )

        return {"openers": openers, "status": "success"}

    except Exception as e:
        return {"openers": "", "status": "error", "message": str(e)}