# autopost
Automated daily pipeline: fetches data from Firestore, edits Canva video template, generates captions with Gemini AI, and posts to social media automatically via GitHub Actions.

## Enginnering Challenge: The "UI GHOST" Problem
During the deployment phase, a significant bottleneck was identified: TikTok's Creator Center frequently injects asynchronous "Feature Announcement" modals ("New editing features added") immediately after a video playload is dropped.

### The Impact
* **DOM Occlusion:** The modal creates a transparent but not-permeable layer over the description and "Post" elements.
* **Automation Stalls:** Standard Playwright selectors fail or trigger `TimeoutErrors` because the target elements are technically "unclickable" while hidden under the overlay.

### The Solution: Asynchronous UI Interception
I engineered a **Zero-Footprint Hotfix** integrated directly into the `tiktok_uploader/upload.py` lifecycle. This logic acts as a **"UI Janitor,"** proactively scanning for and dismissing blocking elements before the business logic proceeds.

#### Implementation Detail:
```python
# --- TIKTOK UI HOTFIX: ASYNCHRONOUS MODAL DISMISSAL ---
# Purpose: TikTok intermittently triggers 'New Feature' overlays post-upload 
# which prevents interaction with the 'Description' and 'Post' selectors.

try:
    logger.debug("Probing for 'New editing features' overlay...")
    
    # Wait for the specific 'Got it' dismissal trigger.
    # A 5000ms timeout is used to account for asynchronous JS rendering.
    page.get_by_text("Got it").click(timeout=5000)
    
    logger.info("UI Hotfix: Blocking modal successfully dismissed.")
    
    # Essential 1s buffer to allow the DOM to settle and 
    # elements to become 'pointer-interactive' again.
    page.wait_for_timeout(1000) 
    
except Exception:
    # Fail-safe: If the modal is not present, the pipeline continues without delay.
    logger.debug("UI Hotfix: No blocking elements detected. Proceeding...")
