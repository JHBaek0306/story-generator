from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from image_caption_node import response

load_dotenv()

# LLM configuration
llm = ChatOpenAI(model="gpt-5-mini", temperature=1)

# Image description
raw_content = response.content
if isinstance(raw_content, list):
    image_caption = " ".join(
        part.get("text", "") for part in raw_content if isinstance(part, dict) and part.get("type") == "text"
    )
else:
    image_caption = str(raw_content)

# Prompt template for the Reflexion Agent
story_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert writer.
            1. {first_instruction}
            2. Reflect and critique your answer. Be severe to maximize improvement.
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Create a story based on the image description."),
    ]
)

first_responder_prompt_template = story_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word story based on the image description."
)

reflection_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert critic.
            Critique the given story in detail and point out weaknesses.
            Then, rewrite the story to improve it."""
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

def generate_story_with_reflection(image_caption: str, iterations: int = 2):
    story = None
    messages = [HumanMessage(content=f"Image description: {image_caption}")]

    for i in range(iterations):
        print(f"\n=== Iteration {i+1}: Story Creation ===")
        story_response = llm.invoke(first_responder_prompt_template.format_messages(messages=messages))
        story = story_response.content
        print(story)

        print(f"\n=== Iteration {i+1}: Reflection & Improvement ===")
        reflection_response = llm.invoke(reflection_prompt_template.format_messages(messages=[HumanMessage(content=story)]))
        story = reflection_response.content
        print(story)

        # Try again based on the improved story in the next loop
        messages = [HumanMessage(content=story)]

    return story

if __name__ == "__main__":
    final_story = generate_story_with_reflection(image_caption, iterations=2)
    print("\n=== Final Story ===")
    print(final_story)
