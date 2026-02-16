# Lessons Learned
*Every mistake documented once, never repeated.*

## Technical
- Google Apps Script webhook: use plain `urllib.request.urlopen()` — do NOT use custom redirect handlers. curl also fails; use Python.
- Google Sheets key parameter is `sheetName` (not `sheet` or `tab`)
- Google Cloud org policy may block service account keys by default — Apps Script webhook is the easier path
- PDF downloads from Canva may be incomplete (.pdf.download bundle) — verify file size before processing

## Process
- When spawning sub-agents, include exact working code snippets for API calls — don't assume they'll figure out quirks
- Test cron jobs with sessions_spawn before relying on cron triggers (faster feedback)
