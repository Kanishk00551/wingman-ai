from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import anthropic
import base64
import os
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are Wingman — a brutally honest, culturally intelligent 
dating coach. You generate conversation openers based on 
what you actually see in the photo.

STRICT RULES:
- Never be generic. No "she looks fun" or "ask about travels"
- Always reference something SPECIFIC visible in the image
- Detect cultural context from visual cues (Indian city landmarks,
  Western locations, food, clothing, signage etc.)
- Give exactly 3 openers labeled: Safe / Flirty / Bold
- Each opener is max 2 sentences
- Sound like a witty friend, not an AI assistant
- No emojis inside the opener text itself
- After the 3 openers, add one line starting with
  "Why these work:" and briefly explain the strategy
"""

@app.get("/")
def root():
    return {"status": "Wingman AI backend is running"}

@app.post("/analyze-photo")
async def analyze_photo(
    file: UploadFile = File(...),
    user_city: str = Form(default="Mumbai"),
    user_style: str = Form(default="witty")
):
    try:
        # Read image
        contents = await file.read()

        # Resize to keep API cost low
        img = Image.open(io.BytesIO(contents))
        img.thumbnail((800, 800))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        img_base64 = base64.standard_b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        # Call Claude Vision
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": img_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": f"""
Analyze this dating profile photo and generate openers.

About the person sending these messages:
- Their city: {user_city}
- Their style preference: {user_style}

Generate 3 openers they can send to this match.
Make them specific to what you actually see in the photo.
"""
                        }
                    ],
                }
            ],
        )

        return {
            "openers": response.content[0].text,
            "status": "success"
        }

    except Exception as e:
        return {
            "openers": "",
            "status": "error",
            "message": str(e)
        }
    

## Analyze the entire dating profile (photos, bio, prompts) and return a structured audit

@app.post("/analyze-profile")
async def analyze_profile(
    files: list[UploadFile] = File(...),
    bio: str = Form(default=""),
    prompts: str = Form(default=""),
    user_city: str = Form(default="Mumbai"),
    target_app: str = Form(default="Hinge")
):
    try:
        # Process all uploaded photos
        image_contents = []
        for file in files:
            contents = await file.read()
            img = Image.open(io.BytesIO(contents))
            img.thumbnail((800, 800))
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            img_base64 = base64.standard_b64encode(
                buffer.getvalue()
            ).decode("utf-8")
            image_contents.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": img_base64,
                }
            })

        # Build the message content
        # First add all images
        message_content = image_contents

        # Then add the text prompt
        message_content.append({
            "type": "text",
            "text": f"""
Audit this dating profile completely and honestly.

Profile details:
- App: {target_app}
- City: {user_city}
- Bio: {bio if bio else "No bio provided"}
- Prompts/Answers: {prompts if prompts else "No prompts provided"}

Analyze everything and return your audit in exactly
this format:

PHOTO SCORE: [X/10]
[2-3 sentences on photo quality, variety, and what
works or doesn't. Be specific about each photo.]

BIO SCORE: [X/10]
[2-3 sentences on the bio. Is it interesting?
Generic? What's missing? Rewrite it if it's bad.]

PROMPTS SCORE: [X/10]
[2-3 sentences on the prompts. Are they revealing
personality? Are they boring? Rewrite the weakest one.]

OVERALL SCORE: [X/10]

BIGGEST PROBLEM:
[One sentence. The single thing killing their matches.]

TOP 3 FIXES:
1. [Specific fix]
2. [Specific fix]  
3. [Specific fix]

REWRITTEN BIO:
[Write an improved version of their bio. If no bio
was provided, write one based on their photos and prompts.]

{f'APP-SPECIFIC TIP FOR {target_app.upper()}:' if target_app else ''}
[One specific tip for how {target_app} algorithm works
and how this profile can take advantage of it.]

Be brutally honest. Sugarcoating helps nobody.
"""
        })

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            system="""
You are a brutally honest dating profile coach with deep
knowledge of how dating app algorithms work, what attracts
matches, and what cultural context matters in different cities.

You have reviewed thousands of profiles. You do not sugarcoat.
You give specific, actionable feedback — never generic advice
like "smile more" or "be yourself."

You understand the difference between how Hinge, Tinder,
and Bumble algorithms work and give platform-specific advice.

For Indian users: you understand Indian dating culture,
what works in metros vs tier 2 cities, and cultural nuances
around how people present themselves on dating apps.
""",
            messages=[
                {
                    "role": "user",
                    "content": message_content
                }
            ],
        )

        # Parse the response into structured sections
        raw = response.content[0].text
        sections = parse_profile_audit(raw)

        return {
            "audit": raw,
            "sections": sections,
            "status": "success"
        }

    except Exception as e:
        return {
            "audit": "",
            "sections": {},
            "status": "error",
            "message": str(e)
        }


def parse_profile_audit(raw_text: str) -> dict:
    """
    Parses the raw audit text into structured sections
    so the frontend can display each section separately
    """
    sections = {
        "photo_score": "",
        "bio_score": "",
        "prompts_score": "",
        "overall_score": "",
        "biggest_problem": "",
        "top_fixes": [],
        "rewritten_bio": "",
        "app_tip": ""
    }

    lines = raw_text.split('\n')
    current_section = None
    current_content = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("PHOTO SCORE:"):
            current_section = "photo_score"
            current_content = [line]
        elif line.startswith("BIO SCORE:"):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = "bio_score"
            current_content = [line]
        elif line.startswith("PROMPTS SCORE:"):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = "prompts_score"
            current_content = [line]
        elif line.startswith("OVERALL SCORE:"):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = "overall_score"
            current_content = [line]
        elif line.startswith("BIGGEST PROBLEM:"):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = "biggest_problem"
            current_content = []
        elif line.startswith("TOP 3 FIXES:"):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = "top_fixes"
            current_content = []
        elif line.startswith("REWRITTEN BIO:"):
            if current_section == "top_fixes":
                sections["top_fixes"] = current_content
            elif current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = "rewritten_bio"
            current_content = []
        elif line.startswith("APP-SPECIFIC TIP"):
            if current_section:
                if current_section == "top_fixes":
                    sections["top_fixes"] = current_content
                else:
                    sections[current_section] = '\n'.join(current_content)
            current_section = "app_tip"
            current_content = []
        else:
            current_content.append(line)

    # Save the last section
    if current_section and current_content:
        if current_section == "top_fixes":
            sections["top_fixes"] = current_content
        else:
            sections[current_section] = '\n'.join(current_content)

    return sections