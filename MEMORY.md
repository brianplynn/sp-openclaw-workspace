# MEMORY.md — Long-Term Memory

## Daedrien
- Owns Spoiled Pets (ShopSpoiledPets.com) — freeze-dried pet food & treats
- Based in Denver metro, CO
- New small business owner, actively growing retail partnerships
- Pronouns: she/her

## Spoiled Pets — Key Facts
- Products: freeze-dried meals (cat & dog), single-ingredient treats, hydration enhancers
- Wild-caught Alaskan salmon, cage-free Wisconsin chicken, made in USA
- HTST pasteurized, AAFCO approved, human-grade
- Not on Amazon or big-box — retailer-exclusive
- Black/Latina woman-owned, Gen Z brand
- Wholesale margins: 40-47%
- Full product/pricing reference: spoiled-pets/wholesale-pricing.md

## Active Systems
- **Retailer Agent** — cron daily 8:30am MST, reads Google Sheet, produces action report
- **Daily Brief** — cron 9:00am MST, I compile and send to Telegram
- Google Sheet webhook (Apps Script): spoiled-pets/config.json
- Email templates (5-email sequence): spoiled-pets/email-templates.md
- Agent architecture doc: spoiled-pets/agent-architecture.md
- Outreach email: daedrien@shopspoiledpets.com

## Content Creation System (In Progress — Feb 16)
- **TikTok** personal account (not business — keeps trending sounds)
- **PostBridge** ($14/mo) for scheduling
- **Seedance** for AI video generation
- 1 post/day, educational focus (nutritional benefits of freeze-dried)
- UGC Image Generator: 5 AI images/day, Daedrien approves
- UGC Video Generator: Seedance, 2-3/week, Daedrien approves
- Photo library: ~115 (PhotoCircle) + ~100 (Google Drive) + AI-generated
- Content strategy doc: spoiled-pets/content-strategy.md
- Architecture doc: spoiled-pets/content-agent-architecture.md

## Future Agents (Not Yet Built)
- Affiliate/UGC — review applications, manage Shopify orders

## Preferences & Decisions
- Daedrien approves emails before sending (autonomous later)
- Email cadence: 7 days after visit → first email, then every 14 days, max 5
- IRL revisit reminders: day before
- Sub-agents report to Chat only, not directly to Daedrien
