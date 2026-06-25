import base64
from PIL import Image
import io
from app.config import claude_client

OPENER_SYSTEM_PROMPT = """
You are Wingman — a brutally honest, culturally intelligent 
dating coach. You generate conversation openers based on 
what you actually see in the photo.

STRICT RULES:
- Never be generic. No "she looks fun" or "ask about travels"
- Always reference something SPECIFIC visible in the image
- Detect cultural context from visual cues (Indian city 
  landmarks, Western locations, food, clothing, signage)
- Give exactly 3 openers labeled: Safe / Flirty / Bold
- Each opener max 2 sentences
- Sound like a witty friend, not an AI
- No emojis inside the opener text
- After openers add one line: "Why these work:" with strategy
"""

PROFILE_SYSTEM_PROMPT = """
You are a brutally honest dating profile coach with deep
knowledge of dating app algorithms, what attracts matches,
and cultural context across different cities.

You do not sugarcoat. You give specific actionable feedback.
You understand Hinge, Tinder, and Bumble algorithm differences.
For Indian users you understand metro vs tier 2 city dynamics.
"""

CONVERSATION_SYSTEM_PROMPT = """
You are Wingman — a brutally honest dating conversation coach.
You analyze conversations and suggest the perfect next reply.

STRICT RULES:
- Read the full conversation before suggesting anything
- Understand the energy and tone of the chat so far
- Never suggest anything generic or try-hard
- Give exactly 3 replies: Safe / Flirty / Bold
- Each reply max 2 sentences
- After replies add: "Read the room:" with one line
  explaining what's happening in this conversation
  and what strategy to follow
"""


def compress_image(file_bytes: bytes) -> str:
    """Compress image and return base64 string"""
    img = Image.open(io.BytesIO(file_bytes))
    img.thumbnail((800, 800))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")


def generate_openers(
    img_base64: str,
    user_city: str,
    user_style: str
) -> str:
    response = claude_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=OPENER_SYSTEM_PROMPT,
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

Generate 3 openers specific to what you see in the photo.
"""
                    }
                ],
            }
        ],
    )
    return response.content[0].text


def generate_profile_audit(
    image_contents: list,
    bio: str,
    prompts: str,
    user_city: str,
    target_app: str
) -> str:
    message_content = image_contents + [
        {
            "type": "text",
            "text": f"""
Audit this dating profile completely and honestly.

Profile details:
- App: {target_app}
- City: {user_city}
- Bio: {bio if bio else "No bio provided"}
- Prompts/Answers: {prompts if prompts else "No prompts provided"}

Return audit in exactly this format:

PHOTO SCORE: [X/10]
[2-3 sentences on photos]

BIO SCORE: [X/10]
[2-3 sentences on bio. Rewrite if bad.]

PROMPTS SCORE: [X/10]
[2-3 sentences on prompts. Rewrite weakest one.]

OVERALL SCORE: [X/10]

BIGGEST PROBLEM:
[One sentence.]

TOP 3 FIXES:
1. [fix]
2. [fix]
3. [fix]

REWRITTEN BIO:
[Improved version]

APP-SPECIFIC TIP FOR {target_app.upper()}:
[One tip for this app's algorithm]

Be brutally honest.
"""
        }
    ]

    response = claude_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=PROFILE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": message_content}],
    )
    return response.content[0].text


def generate_conversation_suggestions(
    conversation: str,
    match_name: str,
    user_city: str,
    user_style: str
) -> str:
    response = claude_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=CONVERSATION_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"""
Here is the conversation so far:

{conversation}

About the person replying:
- Match name: {match_name if match_name else "Unknown"}
- Their city: {user_city}
- Their style: {user_style}

Generate 3 reply options for their next message.
"""
            }
        ],
    )
    return response.content[0].text

def parse_profile_audit(raw_text: str) -> dict:
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

    section_map = {
        "PHOTO SCORE:": "photo_score",
        "BIO SCORE:": "bio_score",
        "PROMPTS SCORE:": "prompts_score",
        "OVERALL SCORE:": "overall_score",
        "BIGGEST PROBLEM:": "biggest_problem",
        "TOP 3 FIXES:": "top_fixes",
        "REWRITTEN BIO:": "rewritten_bio",
        "APP-SPECIFIC TIP": "app_tip"
    }

    def save_current():
        if current_section and current_content:
            if current_section == "top_fixes":
                sections["top_fixes"] = current_content
            else:
                sections[current_section] = '\n'.join(current_content)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        matched = False
        for key, section_name in section_map.items():
            if line.startswith(key):
                save_current()
                current_section = section_name
                current_content = [] if section_name in [
                    "biggest_problem", "top_fixes",
                    "rewritten_bio", "app_tip"
                ] else [line]
                matched = True
                break

        if not matched and current_section:
            current_content.append(line)

    save_current()
    return sections