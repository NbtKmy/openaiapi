import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from browser_use import Agent, Controller, Browser, BrowserConfig
from browser_use.llm import ChatOpenAI
import gradio as gr

load_dotenv()


class Answer(BaseModel):
	text: str

controller = Controller(output_model=Answer)

# Browser nicht anzeigen
browser = Browser(
        config=BrowserConfig(
            headless=True,
        )
    )

async def ask_agent(text):
    agent = Agent(
        task=text,
        controller=controller,
        browser=browser,
        llm=ChatOpenAI(model="o4-mini", temperature=1.0),
    )
    history = await agent.run()
    result = history.final_result()
	
    res_text = ""
    if not result:
        res_text = "No result found."

    try:
        parsed: Answer = Answer.model_validate_json(result)
        res_text = parsed.text
    except Exception as e:
        return f"Parse error: {str(e)}"

    return res_text

demo = gr.Interface(
    fn=ask_agent,
    inputs="text",
    outputs="text"
)

demo.launch(server_port=8501)
