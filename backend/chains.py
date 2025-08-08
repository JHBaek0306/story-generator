import base64
from typing import TypedDict, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END

load_dotenv()

# State
class State(TypedDict):
    image_caption: str
    story: str
    iteration: int


# LLM
caption_llm = ChatOpenAI(model="gpt-5-mini", temperature=1)
story_llm = ChatOpenAI(model="gpt-5-mini", temperature=1)


# image base64 encoding
def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Image description Node
def caption_node(state: State, config: Optional[RunnableConfig] = None) -> State:
    base64_image = encode_image("./picture.jpg")

    message = HumanMessage(
        content=[
            {"type": "text", "text": "Describe this image in detail, in 250 words."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]
    )

    response = caption_llm.invoke([message])

    # content response to string
    raw_content = response.content
    if isinstance(raw_content, list):
        caption = " ".join(
            part.get("text", "") for part in raw_content
            if isinstance(part, dict) and part.get("type") == "text"
        )
    else:
        caption = str(raw_content)

    return {
        "image_caption": caption,
        "story": "",
        "iteration": 0
    }


# Story creation Node
def story_node(state: State, config: Optional[RunnableConfig] = None) -> State:
    prompt = (
        f"You are an expert writer.\n"
        f"1. Provide a detailed ~250 word story based on the following image description:\n"
        f"{state['image_caption']}\n"
    )

    response = story_llm.invoke([HumanMessage(content=prompt)])

    return {
        **state,
        "story": str(response.content)
    }


# Reflection Node
def reflection_node(state: State, config: Optional[RunnableConfig] = None) -> State:
    prompt = (
        f"You wrote the following story:\n{state['story']}\n\n"
        f"Critique it severely to maximize improvement, then rewrite a better version."
    )

    response = story_llm.invoke([HumanMessage(content=prompt)])

    return {
        **state,
        "story": str(response.content),
        "iteration": state["iteration"] + 1
    }


# conditional edge function
def should_continue(state: State) -> str:
    if state["iteration"] < 2:
        return "reflect"
    return END


# LangGraph 
graph = StateGraph(State)

graph.add_node("caption", caption_node)
graph.add_node("story", story_node)
graph.add_node("reflect", reflection_node)

graph.set_entry_point("caption")
graph.add_edge("caption", "story")
graph.add_edge("story", "reflect")
graph.add_conditional_edges("reflect", should_continue, { "reflect": "reflect", END: END })

app = graph.compile()

if __name__ == "__main__":
    final_state = app.invoke(State(image_caption="", story="", iteration=0))
    print("\n=== Final Story ===\n")
    print(final_state["story"])
