from fastapi import FastAPI
# Ensure settings (and .env) are loaded before routers import
import settings
from routers import webhooks
app = FastAPI()
app.include_router(webhooks.router)
from routers import oauth
app.include_router(oauth.router)
