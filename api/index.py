from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import config
from agents import Runner
from agent import Shopping

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    message: str

conversation_history = []

@app.post("/agent")
async def run_agent(data: UserMessage):
    result = await Runner.run(
        starting_agent=Shopping,
        input=str(data.message),
        context={"history": conversation_history},
        run_config=config,
    )
    return {"response": str(result.final_output)}
