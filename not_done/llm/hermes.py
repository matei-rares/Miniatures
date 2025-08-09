from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="NousResearch/Hermes-3-Llama-3.1-8B")
pipe(messages)