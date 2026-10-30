from turkcerag.llm import CHAT_MODEL, get_client

client = get_client()

resp = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[
        {"role": "system", "content": "Kısa ve net cevap veren bir asistansın."},
        {"role": "user", "content": "KVKK nedir? Tek cümleyle anlat."},
    ],
)
print(resp.choices[0].message.content)
print("input:", resp.usage.prompt_tokens, "output:", resp.usage.completion_tokens)
