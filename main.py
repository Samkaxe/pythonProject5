import autogen

# Create an AssistantAgent with no OpenAI integration
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "model": "llama3.1",  # The name of the model you pulled
        "api_type": "ollama",  # Specifies the use of the Ollama API
        "client_host": "http://localhost:11434"  # Make sure this matches your Ollama server's host and port
    }
)

# Create a UserProxyAgent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),

)


# Example function to interact with Ollama API (or other APIs)
def call_ollama_api(prompt):
    import requests
    import json

    # Replace with your own API call logic
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json().get("response", "No response found")
    else:
        return f"Error: {response.status_code} - {response.text}"


# Example usage of AutoGen with custom API interaction
if __name__ == "__main__":
    # Write a Python function that takes a list of numbers and returns the average of the numbers.
    task_description = "Write a Python function that takes a list of numbers and returns the average of the numbers"

    # Custom API call (simulating LLM response generation)
    api_response = call_ollama_api(task_description)
    print("Ollama API Response:", api_response)

    # Initiate chat between UserProxy and Assistant (without OpenAI)
    response = user_proxy.initiate_chat(
        assistant,
        message=task_description
    )
    print(response)


# import requests
# import json
#
# # Define the API endpoint
# url = "http://localhost:11434/api/generate"
#
# # Set the headers
# headers = {
#     "Content-Type": "application/json"
# }
#
# # Define the payload
# payload = {
#     "model": "llama3.2:3b",
#     "prompt": "Write a Python function that takes a list of numbers and returns the average of the numbers.",
#     "stream": False  # Set to True if you prefer streaming responses
# }
#
# # Send the POST request
# response = requests.post(url, headers=headers, data=json.dumps(payload))
#
# # Check for successful response
# if response.status_code == 200:
#     result = response.json()
#     print("Generated Response:", result.get("response", "No response found"))
# else:
#     print(f"Error: {response.status_code} - {response.text}")