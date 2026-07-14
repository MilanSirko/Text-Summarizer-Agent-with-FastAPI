import os
import time
import yaml
from contextlib import AsyncExitStack, asynccontextmanager
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, ModelSettings, set_default_openai_api, set_default_openai_client, set_tracing_disabled

load_dotenv()
set_tracing_disabled(True)
set_default_openai_api('chat_completions')
set_default_openai_client(AsyncOpenAI(base_url=os.getenv('baseurl'), api_key=os.getenv('api')))

with open('config.yaml', 'r', encoding='UTF-8') as f:
    cng=yaml.safe_load(f)

exit_stack = AsyncExitStack()
agent=None
@asynccontextmanager
async def main():
    global textagent
    textagent=Agent(name='Text Summarizer', model=cng['model'], instructions=cng['instructions'],
    mcp_servers=[], model_settings=ModelSettings(max_tokens=cng['maxtoken'], temperature=cng['temperature']))

    yield
    await exit_stack.aclose()

async def aicall(text):
    global textagent
    start=time.perf_counter()
    agentcall=await Runner.run(textagent, text, max_turns=5)
    usage=agentcall.context_wrapper.usage
    fulltime=time.perf_counter()-start

    result={
        "summary": agentcall.final_output,
        "Tokens": usage.total_tokens,
        "Time": round(fulltime, 2)
    }
    return result

