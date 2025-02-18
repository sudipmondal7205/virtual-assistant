


from openai import OpenAI

openai = OpenAI(
    api_key="22zON2Cz9zlWGgan9XyPcoUm11JqDiGC",
    base_url="https://api.deepinfra.com/v1/openai",
)

stream = True # or False

chat_completion = openai.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    messages=[{"role": "user", "content": "tell me about the weather of  india"}],
    stream=stream,
)

if stream :
    for event in chat_completion:
        if event.choices[0].delta.content is not None :
            print(event.choices[0].delta.content, end='')
else:
    print(chat_completion.choices[0].message.content)
