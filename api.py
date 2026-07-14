from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import aicall, main

app=FastAPI()

class input(BaseModel):
    text: str

@app.get('/')
async def root():
    return {'status': 'ok'}

@app.post('/agent')
async def agentcall(payload: input):
    async with main():
        try:
            result=await aicall(payload.text)
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
