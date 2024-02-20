#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call Ollama API (Docker).

Author:
    Erik Johannes Husom

Created:

"""
import json

import requests


class LLMAPIClient:
    def __init__(
        self,
        api_url,
        model_name,
        role="user",
    ):
        self.api_url = api_url
        self.model_name = model_name
        self.role = role

    def call_api(self, content, model_name=None, role=None, stream=False):

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
            ],
            "stream": stream
        }

        # Convert the Python dictionary to a JSON string
        data_json = json.dumps(data)

        # Make the POST request to the API
        response = requests.post(self.api_url, data=data_json)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to get response, status code: {response.status_code}")
            return response

        response_json = json.loads(response.text)

        metadata = {}
        # name of model
        metadata["model_name"] = response_json["model"]
        # timestamp for creation of response
        metadata["created_at"] = response_json["created_at"]
        # time spent generating the response
        metadata["total_duration"] = response_json["total_duration"]
        # time spent in nanoseconds loading the model
        metadata["load_duration"] = response_json["load_duration"]
        # number of tokens in the prompt
        metadata["prompt_token_length"] = response_json["prompt_eval_count"]
        # time spent in nanoseconds evaluating the prompt
        metadata["prompt_duration"] = response_json["prompt_eval_duration"]
        # number of tokens the response
        metadata["response_token_length"] = response_json["eval_count"]
        # time in nanoseconds spent generating the response
        metadata["response_duration"] = response_json["eval_duration"]

        # prompt_length = len(content)
        # response_length = len(response.text)
        # print(f"Prompt length: {prompt_length}")
        # print(f"Response length: {response_length}")

        return response, metadata


def use_ollama_client(
    model_name="mistral",
    content="How can we use Artificial Intelligence for a better society?",
    stream=False,
):
    # The URL of the API
    api_url = "http://localhost:11434/api/chat"

    ollama_client = LLMAPIClient(api_url=api_url, model_name=model_name, role="user")

    response = ollama_client.call_api(content=content, stream=stream)
    print(response.text)


if __name__ == "__main__":

    use_ollama_client(content="What is the capital in France?")
