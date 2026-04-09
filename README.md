# Autopost
Automated daily pipeline that fetches quotes from Firestore, renders them onto video templates, generates AI captions with Gemini, and posts to TikTok automatically via GitHub Actions.

---

## How It Works
Each run executes a single, ordered pipeline:
1. **Fetch:** pulls the next unused quote from Firestore (`used == false`).
2. **Render:** draws the quote text and current date onto (`assets/template.mp4`) using Pillow + MoviePy.
3. **Caption:** sends quote context to Gemini, parses a short caption and hashtags line from the response.
4. **Upload:** posts the rendered video and caption to TikTok via cookie-authenticated automation.
5. **Commit:** marks the quote as used in Firestore with a posted date, only after a confirmed successful upload.
6. **Cleanup:** deletes the local video file.

Upload success is a hard requirement before the state is updated. A failed upload stops the pipeline early, and no quote is ever marked used unless it was acutally posted.

---

## Project Structure
```
autopost/
├── assets/
│   ├── template.mp4          # Base video template
│   └── PALA.TTF              # Font for text overlays
├── output/                   # Temporary render output (gitignored)
├── src/
│   ├── main.py               # Pipeline orchestrator
│   ├── firestore_client.py   # Firestore read/write
│   ├── renderer.py           # Video rendering (MoviePy + Pillow)
│   ├── llm_client.py         # Gemini caption generation
│   └── tiktok_client.py      # TikTok upload automation
└── requirements.txt
```

---

## Tech Stack
- **Data:** Google Cloud Firestore
- **Rendering:** MoviePy, Pillow, NumpPy
- **AI Captions:** Google Gemini (`google-generativeai`)
- **Social Upload:** `tiktok-uploader`
- **Config:** `python-dotenv`


## Setup
 
### 1. Clone and create a virtual environment
 
```bash
git clone https://github.com/ayoamrit/autopost
cd autopost
python -m venv venv
```
 
**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```
 
**macOS/Linux:**
```bash
source venv/bin/activate
```
 
### 2. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 3. Configure environment variables
 
Create a `.env` file in the project root:
 
```env
GOOGLE_APPLICATION_CREDENTIALS=service_account.json
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_model_name
TIKTOK_CLIENT_KEY=your_tiktok_client_key
TIKTOK_CLIENT_SECRET=your_tiktok_client_secret
```
 
### 4. Add credential files
 
Place these files in the project root (do not commit them):
 
- `service_account.json` — Google Cloud service account for Firestore access
- `cookies.txt` — TikTok authenticated session cookies for upload automation
 
---
 
## Usage
 
```bash
python src/main.py
```
 
Each run processes exactly one quote, generates one video, and posts one time. Firestore tracks which quotes have been used, so re-running never produces duplicates.
 
---
 
## Engineering Notes
 
### The UI Ghost Problem
 
During deployment, a significant automation bottleneck was discovered: TikTok's Creator Center intermittently injects asynchronous "Feature Announcement" modals immediately after a video payload is dropped into the uploader. These modals create a transparent but impermeable DOM layer over the description field and the Post button, causing Playwright selectors to fail or hang with `TimeoutError`.
 
**Solution — Asynchronous UI Interception**
 
A zero-footprint hotfix was integrated directly into the `tiktok_uploader/upload.py` lifecycle. It acts as a UI janitor, proactively detecting and dismissing blocking overlays before the upload logic proceeds:
 
```python
# TIKTOK UI HOTFIX: ASYNCHRONOUS MODAL DISMISSAL
# TikTok intermittently triggers 'New Feature' overlays post-upload
# which block interaction with the 'Description' and 'Post' selectors.
 
try:
    logger.debug("Probing for 'New editing features' overlay...")
 
    # 5000ms timeout accounts for asynchronous JS rendering
    page.get_by_text("Got it").click(timeout=5000)
 
    logger.info("UI Hotfix: Blocking modal successfully dismissed.")
 
    # 1s buffer allows DOM to settle before proceeding
    page.wait_for_timeout(1000)
 
except Exception:
    # Fail-safe: modal not present, pipeline continues without interruption
    logger.debug("UI Hotfix: No blocking elements detected. Proceeding...")
```
 
If the modal is absent, the exception is swallowed silently, and the pipeline continues with zero delay.
 
---
