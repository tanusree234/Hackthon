import getpass
import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass("Provide your Google API Key")

# llm = ChatGoogleGenerativeAI(model="gemini-pro")
# result = llm.invoke("Write a ballad about LangChain")

# for chunk in llm.stream("Write a limerick about LLMs."):
#     print(chunk.content)
#     print("---")

# results = llm.batch(
#     [
#         "What's 2+2?",
#         "What's 3+5?",
#     ]
# )
# for res in results:
#     print(res.content)
import base64

image_url = r"captured_frames/frame_1702546011.jpg"
# content = requests.get(image_url).content

llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
# example
message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "Provide complete details about the image, including the objects present and their respective color or any harmful details in the image",
        },  # You can optionally provide text parts
        {"type": "image_url", "image_url": image_url},
    ]
)
print(llm.invoke([message]))
