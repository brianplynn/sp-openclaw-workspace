#!/usr/bin/env python3
"""Upload today's slideshow to TikTok drafts via PostBridge API."""

import json
import os
import urllib.request
import urllib.error

# --- Config ---
CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/spoiled-pets/config.json")
PHOTO_DIR = os.path.expanduser("~/.openclaw/workspace/spoiled-pets/content/photo-library")

with open(CONFIG_PATH) as f:
    config = json.load(f)

API_KEY = config["postbridge"]["api_key"]
BASE_URL = config["postbridge"]["base_url"]
TIKTOK_ACCOUNT_ID = config["postbridge"]["tiktok_account_id"]

# --- Slides (in order) ---
slides = [
    {
        "slide_num": 1,
        "text_overlay": "Your dog's kibble is cooked at 400°F.",
        "photo": "20250626_214937_ED6E99.jpeg",
        "source": "real",
        "role": "HOOK"
    },
    {
        "slide_num": 2,
        "text_overlay": "That heat destroys up to 60% of nutrients.",
        "photo": "20250615_125425_EADA31.jpeg",
        "source": "real",
        "role": "PROBLEM"
    },
    {
        "slide_num": 3,
        "text_overlay": "Freeze-drying locks in raw nutrition.",
        "photo": "20250529_183946_E30A0C.jpeg",
        "source": "real",
        "role": "SOLUTION"
    },
    {
        "slide_num": 4,
        "text_overlay": "HTST pasteurized. AAFCO approved. Human-grade.",
        "photo": "20250626_214937_E1B979.jpeg",
        "source": "real",
        "role": "PROOF"
    },
    {
        "slide_num": 5,
        "text_overlay": "Real ingredients you can see and identify.",
        "photo": "20250624_134016_E8C159.jpeg",
        "source": "real",
        "role": "RESULT"
    },
    {
        "slide_num": 6,
        "text_overlay": "Small-batch. Wisconsin-made. Never mass-produced.",
        "photo": "20250716_105411_E1A9A8.jpeg",
        "source": "real",
        "role": "BRAND"
    },
    {
        "slide_num": 7,
        "text_overlay": "Your pet deserves better. ShopSpoiledPets.com",
        "photo": "20250624_133101_E04919.jpeg",
        "source": "real",
        "role": "CTA"
    }
]

CAPTION = """Your dog's kibble is cooked at 400°F. Here's why that matters. 🔥

Most commercial pet food is heat-processed at extreme temperatures — destroying up to 60% of the natural vitamins, enzymes, and amino acids your pet needs to thrive. That's why you have to add synthetic nutrients back in.

Freeze-drying is different. It preserves raw nutrition without heat damage. Every bag of Spoiled Pets is HTST pasteurized, AAFCO approved, and made with human-grade ingredients you can actually see — wild-caught Alaskan salmon, cage-free Wisconsin chicken, real vegetables.

No fillers. No mystery "meat meal." Just real food, made in small batches.

🐾 ShopSpoiledPets.com | Link in bio

#pettok #petnutrition #freezedriedpetfood #spoiledpets #dogfood #catfood #petparent #freezedried #rawpetfood #healthypets #petfoodtiktok #dogsoftiktok #catsoftiktok #pethealth #knowyourpetfood"""

# --- Upload ---
def api_request(endpoint, data=None, method="POST"):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else "no body"
        print(f"HTTP {e.code} on {method} {endpoint}: {error_body}")
        raise

def upload_image(filepath):
    filename = os.path.basename(filepath)
    size = os.path.getsize(filepath)
    mime = "image/jpeg"

    # Step 1: Get upload URL
    resp = api_request("/v1/media/create-upload-url", {
        "name": filename,
        "mime_type": mime,
        "size_bytes": size
    })
    media_id = resp["media_id"]
    upload_url = resp["upload_url"]
    print(f"  Got media_id={media_id} for {filename}")

    # Step 2: PUT the file bytes
    with open(filepath, "rb") as f:
        file_bytes = f.read()
    put_req = urllib.request.Request(upload_url, data=file_bytes, method="PUT")
    put_req.add_header("Content-Type", mime)
    with urllib.request.urlopen(put_req) as resp:
        print(f"  Uploaded {filename} ({size} bytes) → {resp.status}")

    return media_id

def main():
    media_ids = []
    print("=== Uploading slideshow images ===")
    for slide in slides:
        filepath = os.path.join(PHOTO_DIR, slide["photo"])
        print(f"Slide {slide['slide_num']}: {slide['photo']}")
        mid = upload_image(filepath)
        media_ids.append(mid)
        slide["media_id"] = mid

    print(f"\n=== Creating TikTok draft post ===")
    post_data = {
        "caption": CAPTION,
        "social_accounts": [TIKTOK_ACCOUNT_ID],
        "media": media_ids,
        "platform_configurations": {
            "tiktok": {
                "draft": True
            }
        }
    }
    resp = api_request("/v1/posts", post_data)
    print(f"Post response: {json.dumps(resp, indent=2)}")

    # Extract post ID
    post_id = resp.get("id") or resp.get("post_id") or resp.get("data", {}).get("id")
    status = resp.get("status") or resp.get("data", {}).get("status", "unknown")
    is_draft = resp.get("is_draft") or resp.get("data", {}).get("is_draft", False)

    print(f"\n✅ PostBridge post ID: {post_id}")
    print(f"   Status: {status}")
    print(f"   Draft: {is_draft}")

    # Output for the report
    result = {
        "post_id": post_id,
        "status": status,
        "is_draft": is_draft,
        "media_ids": media_ids,
        "slides": slides
    }
    # Write result to temp file for the report
    result_path = os.path.expanduser("~/.openclaw/workspace/spoiled-pets/content/scripts/upload-result-2026-02-16.json")
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult saved to {result_path}")

if __name__ == "__main__":
    main()
