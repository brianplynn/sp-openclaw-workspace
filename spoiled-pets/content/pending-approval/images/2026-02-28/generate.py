#!/usr/bin/env python3
import base64, json, os, urllib.request, urllib.error, sys
from pathlib import Path

API_KEY = os.environ["OPENAI_API_KEY"]
OUT = Path(__file__).parent

prompts = [
    # 1 - Category E: Lifestyle/Kitchen Scene
    "Casual smartphone photo of a messy kitchen counter with a stand-up pet food pouch with bright yellow lower half and black upper half featuring a cartoon dog face with round white eyes and a drool drop, sitting between a half-empty coffee mug and a crumpled napkin, morning light from a window casting uneven shadows, slightly off-center composition, shot on iPhone 14, slight warm cast, a few crumbs on the marble surface, UGC aesthetic",

    # 2 - Category D: Ingredient Close-Up
    "Close-up smartphone photo of a beautiful raw wild-caught salmon filet on a wooden cutting board, glistening pink-orange flesh with visible fat marbling, slightly blurry background showing a kitchen, shot on iPhone 13, natural overhead lighting with slight shadows, one corner slightly out of focus, a lemon wedge and knife handle visible at edge of frame, UGC aesthetic not professional food photography",

    # 3 - Category C: Meal Prep/Bowl Shot
    "Overhead smartphone photo looking down at a white ceramic ridged bowl filled with small irregular porous tan golden-brown freeze-dried food chunks, airy lightweight texture with rough cratered surfaces, a small jar with a black lid and pink label sitting next to the bowl, dark granite countertop, shot on iPhone 14, slightly off-center framing, natural kitchen lighting, slight motion blur on one edge, UGC aesthetic",

    # 4 - Category B: Pet + Product (partial view)
    "Smartphone photo of a tabby cat's paw and partial face sniffing a small black stand-up treat pouch with pink salmon-colored accent border and a white cat face illustration, the pouch is on a wooden table, shallow depth of field with blurry background showing a cozy living room, shot on iPhone 14, slightly warm tones, natural window light, casual composition, UGC aesthetic not professional",

    # 5 - Category A: Product Flat Lay
    "Top-down smartphone photo flat lay on a light wood table showing three small square jars with black screw-top lids, one with a gold label one with a pink label one with a dark navy label, arranged casually not perfectly aligned, a dog leash and sunglasses nearby, natural daylight from above with soft shadows, slightly imperfect composition, shot on iPhone 14, UGC aesthetic, minor lens flare in corner"
]

for i, prompt in enumerate(prompts, 1):
    print(f"Generating image {i}/5...", flush=True)
    body = json.dumps({"model": "gpt-image-1", "prompt": prompt, "n": 1, "size": "1024x1024", "quality": "high"}).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        b64 = data["data"][0].get("b64_json")
        url = data["data"][0].get("url")
        fname = f"image-{i}.png"
        if b64:
            (OUT / fname).write_bytes(base64.b64decode(b64))
        elif url:
            urllib.request.urlretrieve(url, OUT / fname)
        print(f"  Saved {fname}", flush=True)
    except Exception as e:
        print(f"  ERROR on image {i}: {e}", file=sys.stderr, flush=True)

print("Done!", flush=True)
