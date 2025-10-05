Gitpro - GitHub App with LLM-powered summaries and reviewer suggestions

Overview
- FastAPI app that receives GitHub webhooks, summarizes issues/PRs using Google Gemini (1.5 Flash), and suggests reviewers using sentence-transformers embeddings and FAISS.

Environment variables
- GITHUB_APP_ID - GitHub app id
- GITHUB_APP_PRIVATE_KEY_PATH - path to private key file
- GITHUB_WEBHOOK_SECRET - webhook secret
- GOOGLE_API_KEY - Google API key / bearer token for Generative Language API (or use Workload Identity / OAuth flow)
- GOOGLE_PROJECT_ID - Google Cloud project id
- GOOGLE_LOCATION - Google region (default: us-central1)
- EMBEDDING_MODEL - sentence-transformers model name (default: all-mpnet-base-v2)

Run locally with Docker
```bash
docker build -t gitpro:local .
docker run -e GITHUB_WEBHOOK_SECRET=foo -e GOOGLE_API_KEY=bar -p 8000:8000 gitpro:local
```

Deploying to Render
- Create a Web Service pointing to this repository, set the environment variables in Render dashboard, and use the provided Dockerfile.

Notes
- This repo provides a minimal demonstration. You should add secure storage for embeddings, background workers, and robust error handling before production.

Keeping secrets private (local development)
- This repository includes a `.env.example` with variable names. Create a `.env` file in the project root with your real values. `.env` is included in `.gitignore` and will not be committed.
- Example:
```text
cp .env.example .env
# edit .env and add your keys
```
- The app loads `.env` automatically via `python-dotenv` (see `settings.py`).

Keeping secrets private (GitHub)
- Never commit private keys, tokens, or `.env` to your git repository.
- Add `.env` to `.gitignore` (already added).
- Use a `.env.example` (checked in) to document required variables without exposing secrets.

Deploying securely to Render
- Render and other platforms provide a secure secrets manager. Do NOT push `.env` to your git remote.
- Steps to deploy on Render safely:
	1. Create a new Web Service on Render and connect your GitHub repository.
	2. In the Render dashboard for the service, go to Environment > Environment Variables.
		3. Add the required variables (GITHUB_APP_ID, GITHUB_APP_PRIVATE_KEY, GITHUB_WEBHOOK_SECRET, GOOGLE_API_KEY, GOOGLE_PROJECT_ID, etc.). For the GitHub app private key, paste the PEM contents into the `GITHUB_APP_PRIVATE_KEY` variable (not a file path).
	4. Use the provided Dockerfile (Render will honor it) or let Render build using the Python environment.
	5. Configure the GitHub App webhook URL to point to your Render service URL + `/webhook` and set the webhook secret to the same `GITHUB_WEBHOOK_SECRET` value you added to Render.

CI/CD and rotating secrets
- Avoid storing secrets in CI configuration. Use Render's environment variable settings or a secret manager.
- Rotate keys periodically and provide clear instructions for regenerating or revoking GitHub app keys.

Google Gemini setup notes
- To use Gemini you need a Google Cloud project with the Generative Language API enabled and an API key or appropriate OAuth service account credentials. For quick testing you can create an API key, add it as `GOOGLE_API_KEY`, and set `GOOGLE_PROJECT_ID`.
- For production, prefer service accounts with short-lived tokens or workload identity rather than long-lived API keys.

