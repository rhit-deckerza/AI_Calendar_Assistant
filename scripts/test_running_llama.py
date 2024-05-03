import openai

openai.api_key = "99oNX59pUwWKwDV8WqEg8oN8GtOjlP7gBKXJhYoQd98VArFQFZesUuD5WuZzSTzK",
openai.api_base = "https://api.llama-api.com"


try:
    response = openai.ChatCompletion.create(
        model="llama-13b-chat",
        messages=[
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "user", "content": "Who were the founders of Microsoft?"}
        ]
    )
    # Print the response content directly
    print(response['choices'][0]['message']['content'])
except Exception as e:
    print(e)


