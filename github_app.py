import os
from typing import Optional

from github import GithubIntegration, Github


def _load_private_key() -> str:
    # Support passing private key content directly or via a file path
    key = os.environ.get("GITHUB_APP_PRIVATE_KEY")
    if key:
        return key
    path = os.environ.get("GITHUB_APP_PRIVATE_KEY_PATH")
    if path and os.path.exists(path):
        return open(path).read()
    raise RuntimeError("GitHub app private key not configured")


def app_integration() -> GithubIntegration:
    app_id = os.environ.get("GITHUB_APP_ID")
    if not app_id:
        raise RuntimeError("GITHUB_APP_ID not set")
    private_key = _load_private_key()
    return GithubIntegration(int(app_id), private_key)


def gh_client(owner: str, repo: str) -> Github:
    gi = app_integration()
    inst = gi.get_installation(owner, repo)
    token = gi.get_access_token(inst.id).token
    return Github(login_or_token=token)


def oauth_authorize_url(state: str, redirect_uri: Optional[str] = None) -> str:
    client_id = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
    if not client_id:
        raise RuntimeError("GITHUB_OAUTH_CLIENT_ID not set")
    url = f"https://github.com/login/oauth/authorize?client_id={client_id}&state={state}&scope=repo"
    if redirect_uri:
        url += f"&redirect_uri={redirect_uri}"
    return url

