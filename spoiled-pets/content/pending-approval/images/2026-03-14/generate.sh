#!/bin/bash
set -e
DIR="spoiled-pets/content/pending-approval/images/2026-03-14"
cd /Users/daedrien-lynn/.openclaw/workspace

PROMPTS=(
"Overhead smartphone photo of a beautiful raw wild-caught salmon filet on a rustic wooden cutting board, slightly off-center composition, warm kitchen lighting with soft shadows, a few crumbs and a crumpled kitchen towel visible at edge of frame, shot on iPhone 14, shallow depth of field, slightly imperfect framing, UGC aesthetic not professional photography, natural and appetizing food photography"

"Casual smartphone photo of a stand-up matte pet food pouch with bright yellow lower half and black upper half featuring a cartoon dog face illustration with round white eyes and a white nose, placed on a granite kitchen counter next to a set of car keys and a half-empty coffee mug, slightly messy background with mail and a banana, natural window lighting with slight shadows, shot on iPhone 14, slightly off-center, UGC aesthetic, not professional photography"

"Close-up smartphone photo looking down into a white ceramic ridged pet bowl filled with small irregular porous tan and golden-brown freeze-dried food chunks, some orange sweet potato pieces mixed in, a light dusting of pinkish-mauve powder topper, bowl sitting on a dark wood floor, slight motion blur as if photographer was bending down quickly, natural indoor lighting, shot on iPhone 14, UGC aesthetic not professional photography"

"Casual smartphone photo of a modern kitchen counter scene with two small square jars with black screw-top lids and gold labels placed casually among everyday items - a fruit bowl, a water glass, and a folded dish towel, warm afternoon window light casting long shadows, slightly cluttered background, shot on iPhone 14, slightly off-center framing, UGC aesthetic not professional photography, cozy lived-in kitchen vibe"

"Smartphone photo from slightly above of a tabby cat's paw reaching toward a small black stand-up treat pouch with pink-salmon colored accent borders and a white cat face illustration, pouch laying on its side on a beige couch with a cozy knit blanket in background, soft natural light from nearby window, slightly blurry background, shot on iPhone 14, candid moment captured, UGC aesthetic not professional photography"
)

NAMES=("01-salmon-ingredient" "02-pup-bag-flatlays" "03-bowl-freezedried" "04-hydration-jars-lifestyle" "05-cat-paw-treats")

for i in 0 1 2 3 4; do
  echo "Generating image $((i+1))/5: ${NAMES[$i]}..."
  RESPONSE=$(curl -s https://api.openai.com/v1/images/generations \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d "$(jq -n --arg prompt "${PROMPTS[$i]}" '{model: "gpt-image-1", prompt: $prompt, n: 1, size: "1024x1024", quality: "high"}')")
  
  # Extract b64 or url
  URL=$(echo "$RESPONSE" | jq -r '.data[0].url // empty')
  B64=$(echo "$RESPONSE" | jq -r '.data[0].b64_json // empty')
  
  if [ -n "$URL" ]; then
    curl -s -o "$DIR/${NAMES[$i]}.png" "$URL"
    echo "  Saved ${NAMES[$i]}.png (from URL)"
  elif [ -n "$B64" ]; then
    echo "$B64" | base64 -d > "$DIR/${NAMES[$i]}.png"
    echo "  Saved ${NAMES[$i]}.png (from b64)"
  else
    echo "  ERROR: $RESPONSE"
  fi
done

echo "Done!"
