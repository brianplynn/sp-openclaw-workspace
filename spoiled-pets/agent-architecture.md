# Spoiled Pets — Agent Architecture

## Overview
Three specialist agents + Chat (main agent) as the daily briefing layer.

```
Daedrien (Telegram)
    ↕
Chat (Main Agent) — daily 9am MST brief
    ↕
┌─────────────────┬──────────────────┬────────────────────┐
│ Retailer Agent   │ Content Agent    │ Affiliate Agent    │
│ (active)         │ (future)         │ (future)           │
└─────────────────┴──────────────────┴────────────────────┘
```

## Communication Flow
- Sub-agents report to Chat ONLY (not directly to Daedrien)
- Chat queries all active agents at ~8:45am MST
- Chat sends Daedrien a consolidated daily brief at 9:00am MST on Telegram
- Urgent items (like "you told X store you'd visit tomorrow") get flagged prominently

---

## Agent 1: Retailer Management Agent

### Schedule
- **Daily check:** 8:30am MST via cron (isolated session)
- Reports findings to Chat's session

### Data Source
- Google Sheet: "Denver Metro Area Visits" tab
- URL: https://docs.google.com/spreadsheets/d/1lKT1vGE2qWrISCla9l-phFKjh_toIrDbF65xxqLqLuE/
- Read via CSV export, write via Google Sheets API (requires setup)

### Daily Logic
For each store in the sheet:

1. **Check "Field Selections" + "Status" + notes**
2. **Determine action needed:**

   **→ Email Follow-Up Needed?**
   - Has email address? ✓
   - Last email sent > threshold? (1 week for first, 2 weeks for subsequent)
   - Follow-up count < 5?
   - Not marked "Not interested" or "Customer"?
   - **Action:** Draft full personalized email using the appropriate template, report to Chat

   **→ IRL Revisit Needed?**
   - Field Selections contains "Circle Back IRL"?
   - Any notes about "come back [day]" or "call back"?
   - **Action:** Send reminder to Chat (day before if date known, otherwise flag as "needs scheduling")

   **→ Status Update Needed?**
   - 5 follow-ups sent with no response → mark as "Cold / No Response"
   - Response received → flag for Daedrien's attention
   - **Action:** Update sheet, report to Chat

3. **After processing, update sheet:**
   - Set "Last Email Sent" date
   - Increment "Follow-up Count"
   - Set "Next Follow-up" date
   - Update "Status" field

### Email Templates
Located at: `spoiled-pets/email-templates.md`
- Template 1: Post-Visit Introduction (1 week after visit)
- Template 2: Gentle Check-In (2 weeks after T1)
- Template 3: Value Proposition (2 weeks after T2)
- Template 4: Social Proof + Soft Ask (2 weeks after T3)
- Template 5: Final Follow-Up (2 weeks after T4)

### Email Approval Flow (Current)
1. Agent drafts full email with all personalization filled in
2. Chat includes drafted email in daily brief
3. Daedrien reviews on Telegram, says "send" or requests changes
4. Daedrien sends email manually (or Chat sends once email integration is set up)

### Email Approval Flow (Future / Autonomous)
1. Agent drafts and sends email directly via SMTP
2. Agent updates sheet with sent date
3. Chat reports what was sent in daily brief (informational only)

---

## Agent 2: Content Creation System (IN PROGRESS)
**Full architecture:** `spoiled-pets/content-agent-architecture.md`
**Content strategy:** `spoiled-pets/content-strategy.md`

### Components
- **Content Agent** — 1 TikTok post/day (educational focus), 7am MST
- **UGC Image Generator** — 5 AI-generated images/day, 6am MST
- **UGC Video Generator** — 2-3 Seedance videos/week

### Tools & Platforms
- **TikTok** (personal account — access to trending sounds)
- **PostBridge** ($14/mo) — TikTok scheduling
- **Seedance** — AI video generation
- **Image gen tool** — TBD (DALL-E 3 / Flux / etc.)

### Content Library
- ~115 photos (PhotoCircle) + ~100 photos (Google Drive) + AI-generated
- 5 pillars: Why Freeze-Dried, Ingredient Spotlights, Pet Health, Brand Story, UGC/Social Proof

---

## Agent 3: Affiliate / UGC Agent (FUTURE)
- Review affiliate applications
- Judge whether to send free product
- Create Shopify orders for affiliate sends
- Review UGC submissions for ad copy selection

---

## Chat (Main Agent) — Daily Brief

### Schedule
- 9:00am MST via cron → Telegram message to Daedrien

### Brief Format
```
☀️ Good morning, Daedrien! Here's your daily Spoiled Pets brief:

📬 RETAILER OUTREACH
- X emails ready for your approval (see below)
- X stores need IRL follow-up
- X stores marked as cold (5 follow-ups, no response)

🔔 REMINDERS
- Tomorrow: Visit [Store Name] (you said you'd come back [day])

✉️ EMAILS TO APPROVE
1. [Store Name] — Follow-up #X to [Contact Name]
   [Full draft email below or in thread]

📊 PIPELINE SNAPSHOT
- Active outreach: X stores
- Awaiting response: X stores
- Customers: X stores
- Cold/Dead: X stores
```

---

## Setup Requirements

### Google Sheets Write Access
**Option A: Google Sheets API (Recommended)**
1. Create Google Cloud project
2. Enable Google Sheets API
3. Create service account
4. Share sheet with service account email (editor access)
5. Download credentials JSON to workspace

**Option B: Google Apps Script Webhook**
1. Create Apps Script attached to the sheet
2. Deploy as web app with POST endpoint
3. Agent POSTs updates to the webhook URL

### Email Sending (Future)
- SMTP access to daedrien@shopspoiledpets.com
- Or integration with email provider (Gmail API, SendGrid, etc.)

### Cron Jobs Needed
1. Retailer Agent: daily 8:30am MST (`0 30 8 * * *` America/Denver)
2. Chat Daily Brief: daily 9:00am MST (`0 0 9 * * *` America/Denver)
