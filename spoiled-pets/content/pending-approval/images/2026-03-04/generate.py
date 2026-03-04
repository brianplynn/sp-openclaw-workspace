import os, json, base64, urllib.request, ssl

API_KEY = os.environ["OPENAI_API_KEY"]
URL = "https://api.openai.com/v1/images/generations"

prompts = [
    ("D", "Ingredient Close-Up — Raw salmon filet",
     "Close-up overhead smartphone photo of a raw wild-caught Alaskan salmon filet on a weathered wooden cutting board, shot on iPhone 14, slightly off-center framing, natural window lighting with soft shadows, a few scattered peppercorns and a crumpled paper towel in background, shallow depth of field with slight blur on edges, UGC aesthetic not professional photography, the salmon has vivid pink-orange flesh with visible marbling and skin still on one side"),
    ("A", "Product Flat Lay — Spoiled Pup bag on counter",
     "Smartphone photo of a stand-up pet food pouch with a bright yellow lower half and black upper half featuring a cartoon dog face illustration with round white eyes and a drool drop, matte finish pouch sitting on a granite kitchen counter next to a coffee mug and car keys, shot on iPhone 14, slightly messy background with mail and a banana, natural morning light from a window, slightly off-center composition, casual UGC feel"),
    ("C", "Bowl Shot — Freeze-dried food in ceramic bowl",
     "Close-up overhead smartphone photo of small irregular porous tan and golden-brown freeze-dried food chunks in a white ceramic bowl with ridged texture, some chunks scattered on the dark countertop around the bowl, a small jar with a black lid and gold label visible in the blurry background, shot on iPhone 14, slightly warm natural lighting, shallow depth of field, a few crumbs on the counter, UGC aesthetic with slight motion blur"),
    ("E", "Lifestyle — Kitchen counter with both products",
     "Smartphone photo of a kitchen counter scene with two stand-up pet food pouches casually placed among everyday items - one pouch hot pink and black with a cat face illustration and white eyes, the other yellow and black with a dog face and drool drop illustration, surrounded by a cutting board with lemon slices, a plant pot, dish soap, and a folded towel, natural afternoon lighting with shadows, shot on iPhone 14, slightly cluttered and authentic, UGC aesthetic"),
    ("B", "Pet + Product — Cat sniffing treat pouch",
     "Smartphone photo from slightly above of a tabby cat paw and nose sniffing a small black stand-up treat pouch with pink salmon-colored accent borders on a wooden table, only partial view of the cat visible, the pouch is small 1-2oz size, there is a small ceramic bowl with tan porous freeze-dried chunks nearby, shot on iPhone 14, warm indoor lighting, slight blur on the cat, background shows a cozy living room out of focus, UGC aesthetic not professional"),
]

ctx = ssl.create_default_context()

for i, (cat, desc, prompt) in enumerate(prompts, 1):
    print(f"Generating image {i}/5: {desc}...")
    data = json.dumps({
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "medium"
    }).encode()
    
    req = urllib.request.Request(URL, data=data, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    })
    
    try:
        resp = urllib.request.urlopen(req, timeout=120, context=ctx)
        result = json.loads(resp.read())
        b64 = result["data"][0].get("b64_json", "")
        if b64:
            with open(f"image-{i}.png", "wb") as f:
                f.write(base64.b64decode(b64))
            print(f"  Saved image-{i}.png")
        else:
            url = result["data"][0].get("url", "")
            if url:
                urllib.request.urlretrieve(url, f"image-{i}.png")
                print(f"  Saved image-{i}.png (from URL)")
    except Exception as e:
        print(f"  ERROR: {e}")

print("Done!")
