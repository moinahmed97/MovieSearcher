from fastapi import FastAPI
from agent import agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/ask")
async def ask_agent(title: str):
    """Endpoint to ask the agent for streaming availability."""
    result = await agent.run(title)
    return {"response": result.data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)