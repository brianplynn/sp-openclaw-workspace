# Content Creation Agent — Architecture

## System Overview

```
Daedrien (Telegram)
    ↕ approves images/videos/slideshows via Telegram
Chat (Main Agent) — processes approvals, moves to library
    ↕
┌─────────────────────┬──────────────────────┬───────────────────────┐
│ Slideshow Agent     │ UGC Image Generator  │ UGC Video Generator   │
│ 7:00am MST daily    │ 6:00am MST daily     │ 6:30am MST daily      │
│ (ACTIVE)            │ (ACTIVE)             │ (DISABLED — waiting   │
│                     │                      │  for Seedance API)    │
└─────────────────────┴──────────────────────┴───────────────────────┘
         ↓                    ↓                       ↓
  pending-approval/     pending-approval/      pending-approval/
  slideshows/           images/                videos/
         ↓                    ↓                       ↓
    PostBridge          ✅ → ai-approved/       ✅ → ai-approved/
    (TikTok)            ❌ → feedback log       ❌ → feedback log
```

## Cron Job IDs
- Image Generator: `d5e7be07-500e-448f-a489-c94390e1e467` (ACTIVE)
- Video Generator: `8a6958a2-e2c5-4112-8ae8-205bbbed9606` (DISABLED)
- Slideshow Creator: `8b036171-8d59-48df-ad04-4a3d179805d5` (ACTIVE)

## Feedback Loop
All agents read `spoiled-pets/content/prompt-feedback.md` before generating.
Daedrien's approvals/rejections + feedback are logged there.
Over time, prompts improve based on accumulated preferences.

## Approval Flow
1. Agent generates → saves to `pending-approval/`
2. Chat sends batch to Daedrien on Telegram
3. Daedrien responds: ✅ approve, ❌ reject, or feedback
4. Chat processes:
   - Approved → moves to `photo-library/ai-approved/`
   - Rejected → logs feedback in `prompt-feedback.md`
   - Updates `approved-library.json` with metadata

---

## Agent A: Content Agent (Daily Post Creator)

### Purpose
Generate 1 TikTok post per day — educational content about pet nutrition, freeze-dried food benefits, and Spoiled Pets products.

### Schedule
- **Daily 7:00am MST** — Generate today's post (caption + image/video selection + hashtags)
- Gives Daedrien ~2 hours to review before optimal posting window

### Daily Logic
1. Check content calendar (`content-strategy.md`) for today's topic/pillar
2. Select appropriate image(s) from content library:
   - Prefer real UGC when available and relevant
   - Use AI-generated images as supplement
   - Track which images have been used (avoid repeats)
3. Write caption:
   - Educational hook (first line = scroll stopper)
   - 2-3 key facts
   - Call to action
   - Hashtags
4. Format for PostBridge scheduling
5. Report to Chat with full post preview for daily brief

### Output Format (to Chat)
```
📱 TODAY'S TIKTOK POST
Topic: [Pillar] — [Specific topic]
Format: [Slideshow/Text overlay/etc.]

Caption:
[Full caption text]

Images: [List of selected images with preview]
Sound suggestion: [If applicable]

Status: Ready for scheduling via PostBridge
```

### Content Library Tracking
File: `spoiled-pets/content-library.json`
```json
{
  "images": [
    {
      "id": "ugc-001",
      "source": "photocircle|drive|ai-generated",
      "path": "path/to/image",
      "tags": ["dog", "salmon", "eating"],
      "usedInPosts": ["2026-02-17"],
      "approved": true
    }
  ],
  "posts": [
    {
      "date": "2026-02-17",
      "pillar": "why-freeze-dried",
      "topic": "kibble-vs-freeze-dried",
      "caption": "...",
      "images": ["ugc-001"],
      "status": "posted|scheduled|draft"
    }
  ]
}
```

---

## Agent B: UGC Image Generator (5/day)

### Purpose
Generate 5 AI-created UGC-style product/lifestyle images daily to build up the content library. All images go through Daedrien's approval before entering the library.

### Schedule
- **Daily 6:00am MST** — Generate 5 images
- Results sent to Daedrien via Telegram for approval
- Approved images added to content library

### Image Categories (rotate daily)
1. **Product flat-lays** — Spoiled Pets packaging on aesthetic backgrounds
2. **Pet + product** — Dogs/cats with Spoiled Pets food (UGC style)
3. **Before/after bowls** — Dry freeze-dried → rehydrated meal
4. **Lifestyle** — Kitchen counter, pet bowl area, lifestyle context
5. **Ingredient close-ups** — Raw salmon, chicken, whitefish (appetizing)

### Generation Prompts (Templates)
Each image type has a base prompt template:

**Product flat-lay:**
> "Aesthetic flat-lay photo of freeze-dried pet food in a modern matte black bag labeled 'Spoiled Pets', on a clean marble counter with a small bowl of rehydrated food, natural lighting, iPhone photo style, UGC aesthetic"

**Pet + product:**
> "Candid iPhone photo of a [breed] [dog/cat] eating from a ceramic bowl next to a Spoiled Pets freeze-dried food bag, kitchen setting, warm natural light, slightly imperfect composition like real UGC"

**Lifestyle:**
> "Aesthetic kitchen counter scene with Spoiled Pets freeze-dried pet treats, a coffee mug, and morning light, millennial/gen-z home aesthetic, shot on iPhone"

### Image Generation Tool
- **TBD** — Options: DALL-E 3, Flux, Stable Diffusion, Seedance image gen
- Need: API access, consistent brand representation
- Challenge: Generating accurate product packaging (may need image-to-image with real product photos as reference)

### Approval Flow
1. Agent generates 5 images
2. Sends to Chat → Chat sends batch to Daedrien on Telegram
3. Daedrien reacts: ✅ approve, ❌ reject, or replies with feedback
4. Approved images added to `content-library.json`
5. Rejected images logged with feedback for prompt improvement

---

## Agent C: UGC Video Generator (Seedance)

### Purpose
Generate short UGC-style video clips using Seedance AI for TikTok content.

### Schedule
- **2-3x per week** initially (video gen is more expensive/slower)
- Batch generate, approval queue

### Video Types
1. **Product reveals** — Unboxing / pouring freeze-dried food
2. **Rehydration clips** — Water being poured on freeze-dried food, transforming
3. **Pet eating** — AI-generated clips of pets eating
4. **Ingredient showcase** — Fresh salmon/chicken being freeze-dried

### Seedance Integration
- **Tool:** Seedance AI (seedance.ai)
- **Capabilities:** Text-to-video, image-to-video
- **Flow:** Generate → Download → Approval → Content Library

### Approval Flow
Same as image approval — batch sent to Daedrien via Telegram.

---

## Integration Points

### PostBridge
- **What:** TikTok scheduling tool ($14/mo)
- **How:** TBD — need to check if PostBridge has an API, or if we prepare content for manual scheduling
- **Ideal flow:** Agent prepares post (caption + media), Daedrien schedules in PostBridge with one click

### Photo Sources
| Source | Count | Access Method | Status |
|--------|-------|---------------|--------|
| PhotoCircle | ~115 | TBD (export? API?) | Need access |
| Google Drive | ~100 | Drive API or shared link | Need folder URL |
| AI Generated | 5/day | Image gen API | Need to set up |
| Seedance Video | 2-3/week | Seedance API | Need account |

---

## Setup Checklist

### Immediate (to start generating content)
- [ ] Get Google Drive folder URL for existing UGC photos
- [ ] Export PhotoCircle photos (or get access method)
- [ ] Choose image generation tool + get API access
- [ ] Create Seedance account + check API availability
- [ ] Daedrien sets up PostBridge account
- [ ] Get TikTok account handle for reference

### Once tools are ready
- [ ] Build content library index from existing photos
- [ ] Create image generation cron (daily 6am MST)
- [ ] Create content agent cron (daily 7am MST)
- [ ] Create video generation cron (Mon/Wed/Fri 6am MST)
- [ ] Set up approval flow in daily brief
- [ ] Test end-to-end: generate → approve → schedule → post

### Nice to have
- [ ] PostBridge API integration (if available)
- [ ] Auto-tagging of images (pet type, product, setting)
- [ ] Performance tracking (views, engagement per post)
- [ ] A/B test different content pillars
