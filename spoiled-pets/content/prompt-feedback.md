# Prompt Feedback Log
## How this works
Each entry records: the prompt used, whether it was approved/rejected, and Daedrien's feedback.
Agents MUST read this file before generating to learn from past results.

## Image Generation Feedback

### 2026-02-16 — Dry Run (GPT Image 1)
**Prompt:** "Close-up overhead photo of dry brown kibble dog food in a plain stainless steel bowl..."
**Result:** Approved (usable) — but noted as "a bit obvious" as AI
**Lesson:** Need more imperfection, natural messiness, realistic phone camera artifacts

**Prompt:** "Beautiful appetizing photo of rehydrated freeze-dried pet food in a ceramic bowl..."
**Result:** Approved (usable) — AI-obvious
**Lesson:** Same — too clean, too perfect. Real UGC has slight blur, uneven lighting, background clutter

**Prompt:** "Adorable golden retriever puppy happily eating from a bowl of fresh wholesome food..."
**Result:** Approved (usable) — AI-obvious
**Lesson:** Dogs are hardest — fur texture, eye reflections give it away. Try more environmental context, partial views, slightly off-center framing

### 2026-02-18 — Batch Feedback
**Overall:** Daedrien says images need more UGC feel. The bags described in prompts are too generic ("black pet food bag with yellow accents") — they don't match actual product packaging. Updated image-gen-prompt.md with detailed visual descriptions from real UGC photos.

**Key issues:**
- Bag descriptions too vague → AI generates generic pet food bags that don't look like Spoiled Pets
- Still too clean/polished — needs more authentic phone-camera messiness
- Need to reference actual product details: cartoon animal faces, specific color blocking, matte finish pouches
- Bowl shots should show the actual freeze-dried food texture: porous, airy, irregular tan/golden chunks — not smooth kibble

**Action taken:** Rewrote Brand Reference section in image-gen-prompt.md with detailed visual specs for every product type (bags, treats, jars, food in bowls), based on scanning ~15 real UGC photos from the photo library.

### General Lessons Learned
- Add "shot on iPhone 13" or "slightly blurry" to prompts for more realistic feel
- Include minor imperfections: crumbs on counter, slightly messy background, uneven lighting
- Avoid perfectly centered compositions — real UGC is often off-center
- Pet close-ups work better than full body (less AI-obvious fur)
- Product-focused shots (flat lays, counter scenes) are more convincing than pet portraits
- Dark/moody lighting hides AI artifacts better than bright even lighting

## Video Generation Feedback
(No entries yet — Seedance not yet set up)
