import base64
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-5-mini", temperature=1)

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
# Path to the image
image_path = "./picture.jpg"

# Encode the image
base64_image = encode_image(image_path)

message = HumanMessage(
    content= [       
        {"type": "text", "text": "Describe this image in detail, in 250 words."},
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }
    ]
)

response = llm.invoke([message])
# print(response.content)