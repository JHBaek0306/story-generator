import base64
import io
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel
from PIL import Image

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END

load_dotenv()

MAX_ITERATIONS = 1
MAX_IMAGE_SIZE = (800, 800)  # Base64 전송 전에 이미지 리사이즈
JPEG_QUALITY = 85

class State(BaseModel):
    image_path: str
    user_input: str
    genre: str
    image_caption: str = ""
    story: str = ""
    reflection: str = ""
    iteration: int = 0

# LLM
caption_llm = ChatOpenAI(model="gpt-5-mini", max_tokens=1024)
story_llm = ChatOpenAI(model="gpt-5-mini", temperature=1, max_tokens=1024)

# Image to Base64 Encoding
def encode_image(image_path: str) -> str:
    img = Image.open(image_path)
    img.thumbnail(MAX_IMAGE_SIZE)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=JPEG_QUALITY)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# Image Caption Node
def caption_node(state: State, config: Optional[RunnableConfig] = None) -> State:
    base64_image = encode_image(state.image_path)

    message = HumanMessage(
        content=[
            {"type": "text", "text": "Describe this image in detail, in about 250 words."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]
    )

    response = caption_llm.invoke([message], config=config)

    return state.copy(update={
        "image_caption": response.content
    })


# Story Creation Node
def story_node(state: State, config: Optional[RunnableConfig] = None) -> State:
    prompt = (
        f"You are an expert {state.genre} writer.\n"
        f"1. Provide a detailed ~250 word story based on the following image description and user input:\n"
        f"Image Description: {state.image_caption}\n"
        f"User Input: {state.user_input}\n"
    )

    response = story_llm.invoke([HumanMessage(content=prompt)], config=config)

    return state.copy(update={
        "story": response.content
    })


# Reflection Node
def reflection_node(state: State, config: Optional[RunnableConfig] = None) -> State:
    prompt = (
        f"You are an expert {state.genre} writer.\n"
        f"You wrote the following story:\n{state.story}\n\n"
        f"Critique it severely to maximize improvement, then rewrite a better version."
    )

    response = story_llm.invoke([HumanMessage(content=prompt)], config=config)

    return state.copy(update={
        "reflection": response.content,
        "iteration": state.iteration + 1
    })


# Conditional Edge
def should_continue(state: State) -> str:
    return "reflect" if state.iteration < MAX_ITERATIONS else END


# LangGraph 
graph = StateGraph(State)

graph.add_node("caption", caption_node)
graph.add_node("story", story_node)
graph.add_node("reflect", reflection_node)

graph.set_entry_point("caption")
graph.add_edge("caption", "story")
graph.add_edge("story", "reflect")
graph.add_conditional_edges("reflect", should_continue, {"reflect": "reflect", END: END})

app = graph.compile(debug=True)


# Execution Funciton
def run_image_story_graph(image_path: str, user_input: str, genre: str):
    initial_state = State(
        image_path=image_path,
        user_input=user_input,
        genre=genre
    )
    final_state = app.invoke(initial_state)
    return final_state
