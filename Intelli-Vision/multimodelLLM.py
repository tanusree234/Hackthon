import os
import shutil

from llama_index.multi_modal_llms import ReplicateMultiModal
from llama_index.multi_modal_llms.replicate_multi_modal import (
    REPLICATE_MULTI_MODAL_LLM_MODELS,
)
from llama_index import SimpleDirectoryReader
import pandas as pd

os.environ["REPLICATE_API_TOKEN"] = "r8_NKxX4zgZ5h9lRerJbKyzXj60BGWFAjG3J9SXv"

prompts = [
    "what is the person is holding?",
    "Is there any danger activity observed?",
]
# "is there anything unusual in the image?",


# https://github.com/run-llama/llama_index/blob/main/docs/examples/multi_modal/multi_modal_pydantic.ipynb
def move_jpg_files(source_folder, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get a list of all .jpg files in the source folder
    jpg_files = [f for f in os.listdir(source_folder) if f.lower().endswith(".jpg")]

    # Move each .jpg file to the destination folder
    for jpg_file in jpg_files:
        source_path = os.path.join(source_folder, jpg_file)
        destination_path = os.path.join(destination_folder, jpg_file)
        shutil.move(source_path, destination_path)
        print(f"Moved: {jpg_file}")


source_folder_path = "./frames"
interm_dest_folder_path = os.path.join(source_folder_path, "processing")
final_dest_folder_path = os.path.join(source_folder_path, "processed")
# Create output folder if it doesn't exist
if not os.path.exists(interm_dest_folder_path):
    os.makedirs(interm_dest_folder_path)
if not os.path.exists(final_dest_folder_path):
    os.makedirs(final_dest_folder_path)

move_jpg_files(source_folder_path, interm_dest_folder_path)
# put your local directory here
image_documents = SimpleDirectoryReader(interm_dest_folder_path).load_data()

llm_model = "fuyu-8b"
res = []
for prompt_idx, prompt in enumerate(prompts):
    for image_idx, image_doc in enumerate(image_documents):
        # for llm_idx, llm_model in enumerate(REPLICATE_MULTI_MODAL_LLM_MODELS):
        try:
            ## Initialize the MultiModal LLM model
            multi_modal_llm = ReplicateMultiModal(
                model=REPLICATE_MULTI_MODAL_LLM_MODELS[llm_model],
                max_new_tokens=100,
                temperature=0.1,
                num_input_files=1,
                top_p=0.9,
                num_beams=1,
                repetition_penalty=1,
            )

            mm_resp = multi_modal_llm.complete(
                prompt=prompt,
                image_documents=[image_doc],
            )
        except Exception as e:
            print(
                f"Error with LLM model inference with prompt {prompt}, image {image_idx}, and MM model {llm_model}"
            )
            print("Inference Failed due to: ", e)
            continue
        res.append(
            {
                "image": str(image_doc.image_path),
                "image_idx": image_idx,
                "model": llm_model,
                "prompt": prompt,
                "response": mm_resp,
            }
        )
        move_jpg_files(interm_dest_folder_path, final_dest_folder_path)

df = pd.DataFrame(res)
df.to_csv("multimodeloutput.csv", index=False)