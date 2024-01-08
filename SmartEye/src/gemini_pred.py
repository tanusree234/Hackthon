import os
import base64
import sqlite3
from pillow_heif import register_heif_opener

register_heif_opener()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

api_key = input("Provide the Gemini API: ")
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = api_key

# Get the directory of the current script or module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
)
# Navigate to the parent directory and then to the "captured/video" directory
video_dir = os.path.join(parent_dir, "captured", "video")
print(video_dir)

# Connect to the database
db_path = "current_alerts.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Fetch data from the database
cursor.execute("SELECT Name, Description FROM current_alerts WHERE Active = 1")
result = cursor.fetchall()

# Close the database connection
connection.close()

base_prompt = """
Based on the video identify the alerts name based on the description below  

Alert Name : Description
------------------------
"""

# Process the results
if result:
    # Create a string with the desired format
    result_string = "\n".join(
        [f"{name} : {description}" for name, description in result]
    )
    print(result_string)
else:
    print("No active alerts found.")

close_prompt = """\n\n if No alert situation occured then send as 'No Alert'. 

Provide the answer JSON format below
{
    "AlertName": <comma seperated alerts names based on the list provided>,
    "Summary": <Summary of key events/actions happened from the video>
}
"""

PROMPT = base_prompt + result_string + close_prompt

print(f"Complete PROMPT: {PROMPT}")

video_url = os.path.join(video_dir, "camera_feed_20240108200534.mp4")

llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
# example
message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": PROMPT,
        },  # You can optionally provide text parts
        {"type": "image_url", "image_url": video_url},
    ]
)
print(llm.invoke([message]))
