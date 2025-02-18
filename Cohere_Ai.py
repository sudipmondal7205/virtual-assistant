import cohere 

co = cohere.Client(
  api_key = "your_api_key", 
) 

response = co.generate(
    model='command-r-plus',
    prompt="tell me the history of india",
    temperature=0.3,
    max_tokens=500
)
print(response.generations[0].text.strip())
