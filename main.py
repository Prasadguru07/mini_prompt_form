from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Minimalist AI Prompt Form")

class PromptSchema(BaseModel):
    name: str = Field(..., example="Guruprasad")
    role: str = Field(default="Helpful Assistant", example="Python Expert")

@app.get("/config/{model_id}")
async def get_model_config(model_id: str):
    return {"status": "success", "active_model": model_id}

@app.post("/generate-greeting")
async def create_prompt(data: PromptSchema):
    system_prompt = f"You are a {data.role}. Please greet {data.name}."
    
    return {
        "user_name": data.name,
        "assigned_role": data.role,
        "generated_system_prompt": system_prompt
    }