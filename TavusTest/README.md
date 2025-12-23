# Tavus Avatar Lip-Sync Test

This folder contains a **simple, standalone test** to verify Tavus AI avatar lip-sync using a mock paragraph, **before** integrating it into the main FastAPI backend.

## Files

- `tavus_test.py`  
  Python script that:
  - reads your Tavus API credentials from environment variables or a local `.env` file,
  - sends a mock paragraph to the Tavus avatar API,
  - prints the JSON response, and
  - attempts to download the generated video (if a direct URL is present) as `tavus_output.mp4`.

- `requirements.txt`  
  Minimal Python dependencies required to run the test.

## Setup

1. **Create a virtual environment (recommended)**

```bash
python -m venv .venv
./.venv/Scripts/activate  # on Windows PowerShell
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set environment variables**

You need at least:

- `TAVUS_API_KEY` – your Tavus API key
- `TAVUS_AVATAR_ID` – the ID of the avatar/template you want to test

You can either export them in your shell, or create a `.env` file next to `tavus_test.py`:

```env
TAVUS_API_KEY=your_real_tavus_api_key_here
TAVUS_AVATAR_ID=your_avatar_id_here
```

> **Important:** The exact Tavus API endpoint and payload structure in `tavus_test.py` are **placeholders**. You must adjust them according to the official Tavus documentation for your account and avatar type.

## Running the Test

From this folder:

```bash
python tavus_test.py
```

The script will:

1. Load `TAVUS_API_KEY` and `TAVUS_AVATAR_ID`.
2. Send a mock interview-style paragraph to Tavus.
3. Print the JSON response from Tavus.
4. If the response includes a direct video URL (e.g., `video_url`, `output_url`, or `url`), it will download the video as:

```text
TavusTest/tavus_output.mp4
```

Open this video in any video player (e.g., VLC, default Windows player) and visually check whether the avatar lip movements are synchronized with the spoken text.

## Next Step

Once you confirm the lip-sync looks good with your actual Tavus endpoint and parameters:

- we can extract this logic into a reusable `AvatarService` in the main FastAPI backend,
- and connect it to the interview flow so the avatar speaks all AI-generated questions and feedback.
