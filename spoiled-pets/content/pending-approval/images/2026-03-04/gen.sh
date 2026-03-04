#!/bin/bash
set -e

generate() {
  local num=$1
  local prompt=$2
  echo "Generating image $num..."
  
  response=$(curl -s -X POST https://api.openai.com/v1/images/generations \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"gpt-image-1\",
      \"prompt\": $(echo "$prompt" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))'),
      \"n\": 1,
      \"size\": \"1024x1024\",
      \"quality\": \"high\"
    }")
  
  # Extract b64 data or url
  url=$(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'][0].get('url',''))" 2>/dev/null || true)
  b64=$(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'][0].get('b64_json',''))" 2>/dev/null || true)
  
  if [ -n "$b64" ] && [ "$b64" != "" ]; then
    echo "$b64" | base64 -d > "image-${num}.png"
    echo "Saved image-${num}.png (b64)"
  elif [ -n "$url" ] && [ "$url" != "" ]; then
    curl -s -o "image-${num}.png" "$url"
    echo "Saved image-${num}.png (url)"
  else
    echo "ERROR on image $num: $response"
  fi
}

PROMPT1="Close-up overhead smartphone photo of a raw wild-caught Alaskan salmon filet on a weathered wooden cutting board, shot on iPhone 14, slightly off-center framing, natural window lighting with soft shadows, a few scattered peppercorns and a crumpled paper towel in background, shallow depth of field with slight blur on edges, UGC aesthetic not professional photography, the salmon has vivid pink-orange flesh with visible marbling and skin still on one side"

PROMPT2="Smartphone photo of a stand-up pet food pouch with a bright yellow lower half and black upper half featuring a cartoon dog face illustration with round white eyes and a drool drop, matte finish pouch sitting on a granite kitchen counter next to a coffee mug and car keys, shot on iPhone 14, slightly messy background with mail and a banana, natural morning light from a window, slightly off-center composition, casual UGC feel"

PROMPT3="Close-up overhead smartphone photo of small irregular porous tan and golden-brown freeze-dried food chunks in a white ceramic bowl with ridged texture, some chunks scattered on the dark countertop around the bowl, a small jar with a black lid and gold label visible in the blurry background, shot on iPhone 14, slightly warm natural lighting, shallow depth of field, a few crumbs on the counter, UGC aesthetic with slight motion blur"

PROMPT4="Smartphone photo of a kitchen counter scene with two stand-up pet food pouches casually placed among everyday items - one pouch hot pink and black with a cat face illustration and white eyes, the other yellow and black with a dog face and drool drop illustration, surrounded by a cutting board with lemon slices, a plant pot, dish soap, and a folded towel, natural afternoon lighting with shadows, shot on iPhone 14, slightly cluttered and authentic, UGC aesthetic"

PROMPT5="Smartphone photo from slightly above of a tabby cat's paw and nose sniffing a small black stand-up treat pouch with pink salmon-colored accent borders on a wooden table, only partial view of the cat visible, the pouch is small 1-2oz size, there is a small ceramic bowl with tan porous freeze-dried chunks nearby, shot on iPhone 14, warm indoor lighting, slight blur on the cat, background shows a cozy living room out of focus, UGC aesthetic not professional"

generate 1 "$PROMPT1"
generate 2 "$PROMPT2"
generate 3 "$PROMPT3"
generate 4 "$PROMPT4"
generate 5 "$PROMPT5"

echo "All done!"
