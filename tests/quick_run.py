import asyncio
from services.llm import summarize_text
from services.embeddings import embed_texts


async def main():
    s = await summarize_text("This is a test PR describing a bug where the app crashes when clicking save.")
    print("LLM summary:\n", s)
    em = embed_texts(["fix bug in save flow", "add tests for saving"])
    print("Embeddings shape:", em.shape)


if __name__ == '__main__':
    asyncio.run(main())
