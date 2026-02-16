# PostBridge API Reference (for agents)

## Auth
- Bearer token: read from `spoiled-pets/config.json` → `postbridge.api_key`
- Header: `Authorization: Bearer <API_KEY>`

## Base URL
`https://api.post-bridge.com`

## Spoiled Pets Accounts
- TikTok: ID `44681`, username `shopspoiledpets`

## Endpoints

### Upload Media
**POST** `/v1/media/create-upload-url`
```json
{
  "name": "slide-1.jpg",
  "mime_type": "image/jpeg",  // image/png, image/jpeg, video/mp4, video/quicktime
  "size_bytes": 123456
}
```
Response: `{ "media_id": "...", "upload_url": "...", "name": "..." }`

Then **PUT** the file to `upload_url`:
```
PUT <upload_url>
Content-Type: image/jpeg
Body: <raw file bytes>
```

### Create Post
**POST** `/v1/posts`
```json
{
  "caption": "Your caption here #hashtags",
  "social_accounts": [44681],
  "media": ["media_id_1", "media_id_2"],
  "platform_configurations": {
    "tiktok": {
      "draft": true,
      "is_aigc": false
    }
  }
}
```

Key fields:
- `caption` (required): Post caption
- `social_accounts` (required): Array of account IDs
- `media`: Array of uploaded media IDs (in order)
- `media_urls`: Alternative — array of publicly accessible URLs (ignored if `media` provided)
- `scheduled_at`: ISO datetime string. Null = post instantly
- `is_draft`: If true, post won't process until updated
- `platform_configurations.tiktok.draft`: If true, saves as TikTok draft
- `platform_configurations.tiktok.is_aigc`: If true, labels as AI-generated

### Get Posts
**GET** `/v1/posts?platform=tiktok&status=scheduled&offset=0&limit=10`

### Get Post by ID
**GET** `/v1/posts/{id}`

### Get Post Results
**GET** `/v1/post-results?post_id={id}`

## Python Example (urllib only)
```python
import json, os, urllib.request

API_KEY = "..."  # from config.json
BASE = "https://api.post-bridge.com"

def api_request(method, path, data=None):
    url = f"{BASE}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

# Upload image
def upload_image(filepath):
    size = os.path.getsize(filepath)
    name = os.path.basename(filepath)
    mime = "image/jpeg" if name.endswith(".jpg") else "image/png"
    
    result = api_request("POST", "/v1/media/create-upload-url", {
        "name": name, "mime_type": mime, "size_bytes": size
    })
    
    with open(filepath, "rb") as f:
        file_data = f.read()
    
    upload_req = urllib.request.Request(result["upload_url"], data=file_data, method="PUT")
    upload_req.add_header("Content-Type", mime)
    urllib.request.urlopen(upload_req)
    
    return result["media_id"]

# Create TikTok draft
media_ids = [upload_image(f) for f in image_files]
post = api_request("POST", "/v1/posts", {
    "caption": "Your caption #spoiledpets",
    "social_accounts": [44681],
    "media": media_ids,
    "platform_configurations": {"tiktok": {"draft": True}}
})
```
