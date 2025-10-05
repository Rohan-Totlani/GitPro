from services.embeddings import embed_texts
from services.llm import summarize_text


async def refine_commit_message(message: str) -> str:
    """Given a raw commit message, produce a refined, conventional commit style message."""
    prompt = f"Refine this commit message into a concise conventional-commit style message:\n\n{message}\n\nRefined:" 
    refined = await summarize_text(prompt, fallback=message)
    return refined
