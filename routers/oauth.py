from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from github_app import oauth_authorize_url
import os
import httpx

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    state = os.urandom(8).hex()
    url = oauth_authorize_url(state, redirect_uri=os.environ.get("OAUTH_REDIRECT_URI"))
    return RedirectResponse(url)


@router.get("/callback")
async def callback(code: str = None, state: str = None):
    # Exchange code for token - requires GITHUB_OAUTH_CLIENT_ID and GITHUB_OAUTH_CLIENT_SECRET
    client_id = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
    if not code:
        raise HTTPException(status_code=400, detail="missing code")
    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="oauth client not configured")
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    payload = {"client_id": client_id, "client_secret": client_secret, "code": code, "state": state}
    async with httpx.AsyncClient() as client:
        r = await client.post(token_url, data=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
    # data contains access_token, scope, token_type
    return {"ok": True, "token": data}
