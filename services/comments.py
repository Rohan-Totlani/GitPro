def comment_issue(gh, owner: str, repo: str, issue_number: int, body: str):
    # If gh (Github client) is not provided, create one from the GitHub App
    if gh is None:
        try:
            from github_app import gh_client
            # gh_client expects owner and repo separately
            gh = gh_client(owner, repo)
        except Exception:
            raise
    repo_obj = gh.get_repo(f"{owner}/{repo}")
    issue = repo_obj.get_issue(number=issue_number)
    issue.create_comment(body)

def comment_commit(gh, owner: str, repo: str, commit_sha: str, body: str):
    if gh is None:
        from github_app import gh_client
        gh = gh_client(owner, repo)
    repo_obj = gh.get_repo(f"{owner}/{repo}")
    # create commit comment
    repo_obj.create_commit_comment(commit_sha, body)
