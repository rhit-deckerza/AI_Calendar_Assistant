from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = "Rk4s7EYksi0A8zi7l56ZFO2PjzLq7rnZ"
model = "open-mistral-7b"

client = MistralClient(api_key=api_key)

chat_response = client.chat(
    model=model,
    messages=[ChatMessage(role="user", content="What is the best French cheese?")]
)

print(chat_response.choices[0].message.content)