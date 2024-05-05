from openai import AzureOpenAI, OpenAI
from collections import deque
from dotenv import load_dotenv
import os
import platform
import requests
import json
import re

load_dotenv()

class LLM:
    def __init__(self, name):
        self.name = name

    def using(self):
        print(f"Using {self.name}")

class AzureClient(LLM):
    def __init__(self):
        super().__init__("Azure OpenAI")
        self.api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        self.resource = os.environ.get("AZURE_RESOURCE_GROUP")
        self.deployment_name = os.environ.get("AZURE_DEPLOYMENT_NAME")

    def create_client(self, messages):
        self.using()
        client = AzureOpenAI(
            api_key=self.api_key,
            api_version="2023-12-01-preview",
            azure_endpoint=f"https://{self.resource}.openai.azure.com"
        )
        completion_stream = client.chat.completions.create(
            messages=messages,
            model=self.deployment_name,
            stream=False,
            user='summarizeapi'
        )
        return {"response": completion_stream.choices[0].message.content}

class GroqClient(LLM):
    def __init__(self):
        super().__init__("Groq")
        self.api_key = os.environ.get("GROQ_API_KEY")

    def create_client(self, messages):
        self.using()
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        response = client.chat.completions.create(
            messages=messages,
            model="llama2-70b-4096"
        )
        return {"response": response.choices[0].message.content}

class OpenAIClient(LLM):
    def __init__(self):
        super().__init__("OpenAI")
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def create_client(self, messages):
        self.using()
        client = OpenAI(
            api_key=self.api_key
        )
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-0125"
        )
        return {"response": response.choices[0].message.content}

class TogetherAIClient(LLM):
    def __init__(self):
        super().__init__("TogetherAI")
        self.api_key = os.environ.get("TOGETHERAI_API_KEY")

    def create_client(self, messages):
        self.using()
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.together.xyz/v1"
        )
        response = client.chat.completions.create(
            messages=messages,
            model="mistralai/Mixtral-8x7B-Instruct-v0.1"
        )
        return {"response": response.choices[0].message.content}


#####################################################

   
def parse_response(text):
    text = str(text)

    pattern = r'\{\'response\': \'(.+?)\'}'

    # Use re.findall() to find all occurrences of the pattern in the text
    matches = re.findall(pattern, text)

    # If matches are found, return the first match
    if matches:
        return matches[0]
    else:
        return None

def LLM_review(root_folder):
    tree = {
        "name": os.path.basename(root_folder),
        "type": "folder",
        "children": []
    }

    # Queue to perform BFS
    queue = [(root_folder, tree["children"])]

    while queue:
        current_folder, current_children = queue.pop(0)

        for item in os.listdir(current_folder):
            item_path = os.path.join(current_folder, item)
            item_type = "folder" if os.path.isdir(item_path) else "file"
            item_data = {
                "name": item,
                "type": item_type
            }

            if item_type == "folder":
                item_data["children"] = []
                queue.append((item_path, item_data["children"]))

            current_children.append(item_data)

    return tree

def LLM_summarize(info, client_type):
    messages = []

    info_json = json.dumps(info)

    # System Prompt
    messages.append(
        {
        "role": "system",
        "content": "Let's play a game. Imagine you're a software developer tasked with reviewing a new project repository on GitHub. Your goal is to identify the framework (if applicable) of the repository. Your team is particularly interested in filenames that adhere to common naming conventions and contain keywords indicative of important components or functionalities within the codebase. Your task is to generate a summary of the repository, including relevant filenames and the suspected purpose of the repo. Answer questions quickly and briefly. The contents of the folder include: " + info_json
        }
    )
    
    client = {
        "azure": AzureClient(),
        "groq": GroqClient(),
        "openai": OpenAIClient(),
        "togetherai": TogetherAIClient()
    }.get(client_type)

    if not client:
        raise ValueError("Invalid client type specified.")

    response = client.create_client(messages)
    print()
    
    try:
        files = parse_response(response)
        print(files)
    except:
        print("mhmm... something went wrong...try again maybe?")