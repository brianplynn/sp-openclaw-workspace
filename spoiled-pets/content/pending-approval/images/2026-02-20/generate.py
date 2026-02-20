#!/usr/bin/env python3
import base64, json, os, urllib.request, urllib.error, sys
from pathlib import Path

API_KEY = os.environ["OPENAI_API_KEY"]
OUT = Path(__file__).parent

prompts = [
    # 1. Category D — Ingredient Close-Up (salmon)
    (
        "img1-salmon-ingredient.png",
        "D — Raw salmon filet close-up",
        "Overhead smartphone photo of a beautiful raw wild-caught Alaskan salmon filet on a worn wooden cutting board, natural kitchen window light casting soft uneven shadows, slightly off-center composition, a lemon wedge and scattered peppercorns nearby, slight motion blur on one edge, shot on iPhone 14, UGC aesthetic not professional photography, warm golden tones, a crumb on the counter edge"
    ),
    # 2. Category A — Product Flat Lay
    (
        "img2-product-flatlay.png",
        "A — Dog meal pouch flat lay on kitchen counter",
        "Casual overhead smartphone photo of a stand-up pet food pouch with a bright yellow lower half and black upper half featuring a cartoon dog face illustration with round white eyes, sitting on a white marble kitchen counter, a coffee mug and car keys scattered nearby, morning sunlight streaming in from the left creating warm shadows, slightly messy composition, shot on iPhone 14, UGC aesthetic, natural imperfect lighting, a few crumbs visible on counter"
    ),
    # 3. Category C — Meal Prep / Bowl Shot
    (
        "img3-bowl-rehydrated.png",
        "C — Freeze-dried food being rehydrated in bowl",
        "Close-up smartphone photo of freeze-dried pet food chunks being rehydrated in a white ceramic ridged bowl, warm water being poured from a small measuring cup, the food is tan and golden-brown with porous airy irregular textures and some darker pieces, slightly off-center framing, kitchen counter background slightly blurred, natural window lighting with uneven shadows, shot on iPhone 14, UGC aesthetic, not professional, a paper towel visible at edge of frame"
    ),
    # 4. Category E — Lifestyle / Kitchen Scene
    (
        "img4-kitchen-lifestyle.png",
        "E — Kitchen counter lifestyle scene with treats",
        "Casual smartphone photo of a cozy kitchen counter scene, two small black stand-up treat pouches with pink salmon-colored accent borders and a white cat face graphic sitting among everyday items: a half-empty glass of water, a phone charger cable, and a folded dish towel, warm afternoon light from a window, slightly dark and moody tones, background slightly out of focus showing kitchen cabinets, shot on iPhone 14, slightly imperfect composition tilted slightly, authentic UGC feel"
    ),
    # 5. Category B — Pet + Product (partial view)
    (
        "img5-cat-sniffing.png",
        "B — Cat paw and nose near product jar",
        "Close-up smartphone photo of a tabby cat's nose and one paw reaching toward a small square jar with a black screw-top lid and a pink label, the jar sits on a wooden table, shallow depth of field with the cat slightly soft-focus and the jar sharp, natural indoor lighting slightly warm, a cozy blanket visible in the background, shot on iPhone 14, UGC aesthetic, slightly off-center, casual and authentic feeling, not staged"
    ),
]

for fname, desc, prompt in prompts:
    print(f"Generating: {desc}...", flush=True)
    body = json.dumps({
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "high"
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        b64 = data["data"][0].get("b64_json")
        url = data["data"][0].get("url")
        if b64:
            (OUT / fname).write_bytes(base64.b64decode(b64))
        elif url:
            urllib.request.urlretrieve(url, OUT / fname)
        print(f"  ✅ Saved {fname}", flush=True)
    except Exception as e:
        print(f"  ❌ Failed: {e}", flush=True)

print("Done!")
