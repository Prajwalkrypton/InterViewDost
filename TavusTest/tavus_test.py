import os
import sys
import json
import pathlib

import requests
from dotenv import load_dotenv


def main() -> None:
    # Load environment variables from a local .env file if present
    # (TAVUS_API_KEY and TAVUS_AVATAR_ID should be defined).
    load_dotenv()

    api_key = os.getenv("TAVUS_API_KEY")
    avatar_id = os.getenv("TAVUS_AVATAR_ID")

    if not api_key or not avatar_id:
        print("ERROR: Please set TAVUS_API_KEY and TAVUS_AVATAR_ID in your environment or .env file.")
        sys.exit(1)

    # Mock paragraph to test lip-sync
    script_text = (
        "In this demo, we are testing a realistic AI avatar for interview simulations. "
        "The goal is to check whether the lip movements are synchronized with the spoken words. "
        "If this works correctly, we will integrate this avatar into a full AI-powered interview system."
    )

    # NOTE: The endpoint URL and payload structure below are PLACEHOLDERS.
    # You MUST adjust them according to the official Tavus API documentation
    # for your account and the specific avatar / template you are using.
    base_url = "https://api.tavus.io"  # Replace with the correct base URL if different

    # Example placeholder endpoint – adjust to actual Tavus endpoint
    endpoint = f"/v2/avatars/{avatar_id}/generate"
    url = base_url + endpoint

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        # Replace / extend these fields with whatever Tavus expects:
        "script": script_text,
        # e.g., you might need fields like "voice_id", "webhook_url", "format", etc.
    }

    print("Sending request to Tavus...")
    response = requests.post(url, headers=headers, json=payload, timeout=60)

    print("Status:", response.status_code)
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Raw response:")
        print(response.text)
        sys.exit(1)

    print("Response JSON:")
    print(json.dumps(data, indent=2))

    # Depending on Tavus, you might get:
    #  - a direct video URL,
    #  - a job / request ID to poll later,
    #  - or a signed URL to download the video.
    # The following is generic logic that tries to download a video if a URL is present.

    video_url = None
    # Try some common keys that Tavus might use – adjust based on real response
    for key in ("video_url", "output_url", "url"):
        if isinstance(data, dict) and key in data:
            video_url = data[key]
            break

    if not video_url:
        print("No video URL field found in response. Check Tavus docs and adjust parsing.")
        return

    print(f"Attempting to download video from: {video_url}")
    video_resp = requests.get(video_url, timeout=120)
    if video_resp.status_code != 200:
        print("Failed to download video, status:", video_resp.status_code)
        return

    output_path = pathlib.Path(__file__).parent / "tavus_output.mp4"
    with open(output_path, "wb") as f:
        f.write(video_resp.content)

    print(f"Video saved to: {output_path}")
    print("Open this file in a video player to visually inspect lip-sync.")


if __name__ == "__main__":
    main()
