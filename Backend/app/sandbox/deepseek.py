from openai import OpenAI

client = OpenAI(
    api_key="sk-************************", 
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    max_tokens=1024,
    temperature=1.5,
    stream=False
)

print(response.choices[0].message.content)