#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Client for LLM APIs.

This module provides a client for calling the LLM APIs, focusing on simplicity and flexibility.
It allows users to interact with the API to send requests and receive responses.

Author:
    Erik Johannes Husom

Created:
    2024-02-01

"""
import json

import requests


class LLMAPIClient:
    """A client for interacting with LLM (Large Language Model) APIs such as Ollama.
    
    Attributes:
        api_url (str): The URL of the API endpoint.
        model_name (str): Default model name to use for requests.
        role (str): Default role to use in the message payload.
    """

    def __init__(
        self,
        api_url,
        model_name,
        role="user",
    ):
        """Initialize the API client with a specific API URL, model name, and role."""

        self.api_url = api_url
        self.model_name = model_name
        self.role = role

    def call_api(self, content, model_name=None, role=None, stream=False):
        """Send a request to the API with the given content, model name, and role.
        
        Args:
            content (str): The content of the message to be sent to the API.
            model_name (str, optional): The model name to use for this request. Defaults to None.
            role (str, optional): The role to use for this message. Defaults to None.
            stream (bool, optional): Whether to stream the response. Defaults to False.
        
        Returns:
            tuple: A tuple containing the API response and extracted metadata as a dictionary.
        """

        if model_name is None:
            model_name = self.model_name
        if role is None:
            role = self.role

        data = {
            "model": model_name, 
            "messages": [{"role": role, "content": content}],
            "stream": stream
        }

        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()  # Raises HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None, {}

        response_json = json.loads(response.text)

        metadata = {}
        # name of model
        metadata["model_name"] = response_json["model"]
        # timestamp for creation of response
        metadata["created_at"] = response_json["created_at"]
        # time spent generating the response
        metadata["total_duration"] = response_json["total_duration"]
        # time spent in nanoseconds loading the model
        metadata["load_duration"] = response_json["load_duration"]
        # number of tokens in the prompt
        metadata["prompt_token_length"] = response_json["prompt_eval_count"]
        # time spent in nanoseconds evaluating the prompt
        metadata["prompt_duration"] = response_json["prompt_eval_duration"]
        # number of tokens the response
        metadata["response_token_length"] = response_json["eval_count"]
        # time in nanoseconds spent generating the response
        metadata["response_duration"] = response_json["eval_duration"]

        return response, metadata


def use_ollama_client(
    model_name="mistral",
    content="How can we use Artificial Intelligence for a better society?",
    stream=False,
):
    # The URL of the API
    api_url = "http://localhost:11434/api/chat"

    ollama_client = LLMAPIClient(api_url=api_url, model_name=model_name, role="user")

    response, metadata = ollama_client.call_api(content=content, stream=stream)
    print(response.text)
    print(metadata)


if __name__ == "__main__":

    use_ollama_client(content="What is the capital in France?")
