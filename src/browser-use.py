import asyncio
from dotenv import load_dotenv
from browser_use import Agent
from browser_use.llm import ChatOpenAI

load_dotenv()

task = """
    今日の東京とチューリッヒの天気と気温を教えてください。
    """

async def main():
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model="o4-mini", temperature=1.0),
    )
    await agent.run()

asyncio.run(main())