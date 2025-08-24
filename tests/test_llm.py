text = "Artificial Intelligence is transforming industries worldwide."

def summarize(text, provider):
    # Dummy implementation for testing purposes
    summary = f"Summary by {provider}: {text[:30]}..."
    p_tokens = 10
    c_tokens = 8
    latency = 0.1
    err = None
    return summary, p_tokens, c_tokens, latency, err

for provider in ["groq", "gemini", "mistral"]:
    summary, p_tokens, c_tokens, latency, err = summarize(text, provider)
    print(provider, summary, err)
