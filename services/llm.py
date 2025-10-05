import os
from typing import Optional

import httpx

# Prefer Google Gemini 1.5 Flash via the Google Generative Language API if configured.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")
GOOGLE_LOCATION = os.environ.get("GOOGLE_LOCATION", "us-central1")

async def summarize_text(text: str, fallback: Optional[str] = None) -> str:
    """Summarize text using Google Gemini 1.5 Flash.

    Returns summarized text or fallback when not configured.
    """
    prompt = f"Summarize the following text in a concise way for a GitHub issue/PR reviewer:\n\n{text}\n\nSummary:"

    # Google Generative Language API via REST (minimal dependency)
    if GOOGLE_API_KEY and GOOGLE_PROJECT_ID:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta2/projects/{GOOGLE_PROJECT_ID}/locations/{GOOGLE_LOCATION}/models/chat-bison-001:generateMessage"
        )
        headers = {"Authorization": f"Bearer {GOOGLE_API_KEY}", "Content-Type": "application/json"}
        body = {
            "messages": [{"content": prompt, "author": "user"}],
            "temperature": 0.2,
            "candidate_count": 1,
            "max_output_tokens": 300,
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.post(url, json=body, headers=headers)
                r.raise_for_status()
                data = r.json()
            # Parse Google response
            if isinstance(data, dict):
                # response may contain candidates with output
                out = None
                if "candidates" in data and isinstance(data["candidates"], list):
                    out = data["candidates"][0].get("content")
                elif "output" in data:
                    out = data["output"]
                if out:
                    # content may be dict with text
                    if isinstance(out, dict):
                        return out.get("content", fallback or "(empty)").strip()
                    return str(out).strip()
        except Exception:
            # If Google call fails, return fallback below
            pass

    return fallback or "(no LLM configured)"
