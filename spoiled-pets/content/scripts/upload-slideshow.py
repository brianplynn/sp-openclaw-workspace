#!/usr/bin/env python3
import json, os, urllib.request, urllib.error

BASE_DIR = "/Users/daedrien-lynn/.openclaw/workspace"
CONFIG = json.load(open(f"{BASE_DIR}/spoiled-pets/config.json"))
PB = CONFIG["postbridge"]
API_KEY = PB["api_key"]
BASE_URL = PB["base_url"]
TIKTOK_ID = PB["tiktok_account_id"]
SLIDES_DIR = f"{BASE_DIR}/spoiled-pets/content/pending-approval/slideshows/2026-03-06"

CAPTION = """Cooking destroys up to 60% of your pet's nutrients. 🔥

Most kibble is extruded at 300-400°F — that heat breaks down proteins, vitamins, and enzymes your pet actually needs. Freeze-drying? It just removes water. That's it. No extreme heat, no nutrient loss.

The result: 97% of original nutrients preserved in every bite. Plus, Spoiled Pets is HTST pasteurized — so it's safe AND nutritious. Real ingredients you can see, smell, and recognize.

Your pet deserves food that works as hard as their body does. 🐾

ShopSpoiledPets.com | Link in bio

#freezedriedpetfood #freezedried #petnutrition #dogfood #catfood #healthypets #rawfeeding #petfoodtransparency #spoiledpets #humangradeingredients #petparents #dogmom #catmom #pettok #nutrientdense"""

media_ids = []
for i in range(1, 8):
    slide_path = f"{SLIDES_DIR}/slide-{i}.jpeg"
    size = os.path.getsize(slide_path)
    
    # Step 1: Get upload URL
    req = urllib.request.Request(
        f"{BASE_URL}/v1/media/create-upload-url",
        data=json.dumps({"name": f"slide-{i}.jpeg", "mime_type": "image/jpeg", "size_bytes": size}).encode(),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method="POST"
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    media_id = resp["media_id"]
    upload_url = resp["upload_url"]
    
    # Step 2: Upload file
    with open(slide_path, "rb") as f:
        put_req = urllib.request.Request(upload_url, data=f.read(), headers={"Content-Type": "image/jpeg"}, method="PUT")
        urllib.request.urlopen(put_req)
    
    media_ids.append(media_id)
    print(f"Uploaded slide-{i}: {media_id}")

# Step 3: Create post
post_data = {
    "caption": CAPTION,
    "social_accounts": [TIKTOK_ID],
    "media": media_ids,
    "platform_configurations": {"tiktok": {"draft": True}}
}
req = urllib.request.Request(
    f"{BASE_URL}/v1/posts",
    data=json.dumps(post_data).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST"
)
resp = json.loads(urllib.request.urlopen(req).read())
print(f"\nPOST CREATED: {json.dumps(resp, indent=2)}")
