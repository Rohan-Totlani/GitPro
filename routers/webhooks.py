from fastapi import APIRouter, Request, Header, HTTPException, BackgroundTasks
import hmac, hashlib, json, os
from services.llm import summarize_text
from services.reviewers import ReviewerEngine
from services.comments import comment_issue
import settings

router = APIRouter()


def verify(sig: str, body: bytes, secret: str):
    mac = hmac.new(secret.encode(), msg=body, digestmod=hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, sig or "")


async def _process_issue_event(payload: dict):
    # Minimal processing: summarize issue body and post a comment
    owner_repo = payload.get("repository", {}).get("full_name", "").split("/")
    if len(owner_repo) != 2:
        return
    owner, repo = owner_repo
    issue = payload.get("issue") or payload.get("pull_request")
    if not issue:
        return
    body = issue.get("body") or ""
    title = issue.get("title") or ""
    summary = "(no LLM configured)"
    try:
        summary = await summarize_text(title + "\n\n" + body, fallback="(no summary)")
    except Exception:
        summary = "(llm error)"
    comment_body = f"Automated summary:\n\n{summary}"
    # Post comment using GitHub App token (handled in comments.comment_issue)
    try:
        comment_issue(None, owner, repo, issue.get("number"), comment_body)
    except Exception:
        # swallow to avoid background task crash
        pass


async def _process_push_event(payload: dict):
    # For each commit, produce a refined commit message and comment on the commit
    owner_repo = payload.get("repository", {}).get("full_name", "").split("/")
    if len(owner_repo) != 2:
        return
    owner, repo = owner_repo
    commits = payload.get("commits", [])
    if not commits:
        return
    from services.commit_refine import refine_commit_message
    from services.comments import comment_commit
    for c in commits:
        msg = c.get("message", "")
        sha = c.get("id")
        try:
            refined = await refine_commit_message(msg)
            body = f"Suggested refined commit message:\n\n{refined}"
            comment_commit(None, owner, repo, sha, body)
        except Exception:
            continue


@router.post("/webhook")
async def webhook(request: Request, x_hub_signature_256: str = Header(None), x_github_event: str = Header(None)):
    raw = await request.body()
    secret = settings.GITHUB_WEBHOOK_SECRET
    if not secret:
        raise HTTPException(status_code=500, detail="GITHUB_WEBHOOK_SECRET not configured")
    if not verify(x_hub_signature_256, raw, secret):
        raise HTTPException(status_code=401, detail="bad signature")
    payload = await request.json()
    # For issues and pull_request events, enqueue a background job
    import asyncio
    if x_github_event in ("issues", "pull_request", "pull_request_review"):
        asyncio.create_task(_process_issue_event(payload))
    if x_github_event == "push":
        asyncio.create_task(_process_push_event(payload))
    return {"ok": True, "event": x_github_event, "action": payload.get("action")}
