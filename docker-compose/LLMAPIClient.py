#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call Ollama API (Docker).

Author:
    Erik Johannes Husom

Created:

"""
import requests
import json



class LLMAPIClient():

    def __init__(self,
            api_url,
            model_name,
            role="user",
    ):

        self.api_url = api_url
        self.model_name = model_name
        self.role = role


    def call_api(self, content, model_name=None, role=None):

        if model_name is None:
            model_name = self.model_name
        if role is None:
            role = self.role

        # The data to be sent to the API
        data = {
            "model": model_name,
            "messages": [
                {
                    "role": role,
                    "content": content
                }
            ]
        }

        # Convert the Python dictionary to a JSON string
        data_json = json.dumps(data)

        # Make the POST request to the API
        response = requests.post(url, data=data_json)

        # Check if the request was successful
        if response.status_code == 200:
            # Print the response data
            print(response.text)
        else:
            # Print an error message
            print(f"Failed to get response, status code: {response.status_code}")

        return response

def use_ollama_client(model_name="mistral", content="How can we use Artificial Intelligence for a better society?"):

    # The URL of the API
    api_url = "http://localhost:11434/api/chat"

    ollama_client = LLMAPIClient(
            api_url=api_url,
            model_name=model_name,
            role="user"
    )

    response = ollama_client.call_api(content=content)
    print(response)

if __name__ == '__main__': 
