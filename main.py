from agent import aicall, main
import asyncio

async def runtest():
    async with main():
        while True:
            user=input('You:')
            response=await aicall(user)
            print(response['summary'])
            print(f'{response["Time"]} - {response["Tokens"]}')

asyncio.run(runtest())
