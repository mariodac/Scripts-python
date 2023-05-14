import openai
import os

# código gerado pelo chatgpt

openai.api_key = "chave"

def ask_gpt(question, model_engine="davinci", max_tokens=2000, temperature=0.5):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=question,
        max_tokens=max_tokens,
        n=1,
        temperature=temperature,
    )

    message = completions.choices[0].text
    return message.strip()

question = "Quais são as últimas notícias sobre anime?"
answer = ask_gpt(question, max_tokens=2048-len(question))
print(answer)