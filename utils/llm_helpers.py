# utils/llm_helpers.py

import os
import time
import json
import requests
from transformers import AutoTokenizer
from config import PROVIDER_COSTS, DEFAULT_MODELS
from dotenv import load_dotenv

def validate_environment_variables():
    """Validate that all required environment variables are set."""
    required_vars = ["GROQ_API_KEY", "GEMINI_API_KEY", "MISTRAL_API_KEY"]
    missing_vars = [var for var in required_vars if os.getenv(var) is None]
    
    if missing_vars:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

load_dotenv()
validate_environment_variables()
GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

# ------------------- Tokenizer -------------------
tokenizer = AutoTokenizer.from_pretrained("gpt2")

def estimate_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

def calculate_cost(provider: str, prompt_tokens: int, completion_tokens: int) -> float:
    costs = PROVIDER_COSTS.get(provider, {"prompt": 0.0, "completion": 0.0})
    return (prompt_tokens / 1000 * costs["prompt"] + completion_tokens / 1000 * costs["completion"])

# ------------------- Prompts -------------------
PROMPTS = {
    "summarize": """You are a concise summarizer.
Produce a 3-sentence summary of the text below.
Output only JSON: {{ "summary": "..." }}

Text:
{text}
""",
    "sentiment": """Classify sentiment: Positive / Neutral / Negative.
Provide justification in JSON: {{ "label": "...", "reason": "..." }}

Text:
{text}
""",
    "style": """Analyze writing style: Formal / Informal / Neutral.
Rate complexity: Simple / Medium / Complex.
Give 2 examples in JSON: {{ "style": "...", "complexity": "...", "examples": ["...", "..."] }}

Text:
{text}
"""
}

# ------------------- REST API calls -------------------
def _call_provider_api(task, prompt, provider, model, **options):
    try:
        if provider.lower() == "groq":
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model or DEFAULT_MODELS.get("groq", "llama3-8b-8192"),
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                **options
            }

        elif provider.lower() == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": options.get("max_tokens", 1024),
                    "topP": 0.8,
                    "topK": 40
                }
            }

        elif provider.lower() == "mistral":
            url = "https://api.mistral.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {MISTRAL_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "mistral-medium-latest",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 300,
                **options
            }

        else:
            raise ValueError(f"Provider {provider} not supported")

        r = requests.post(url, headers=headers, json=payload)
        r.raise_for_status()

        # Parse JSON response
        if "json" in r.headers.get("Content-Type", ""):
            resp_json = r.json()
            # Most APIs put text output under different keys:
            if provider.lower() == "gemini":
                # Gemini response format: candidates[0].content.parts[0].text
                return resp_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            elif provider.lower() == "mistral":
                # Mistral chat completions format: choices[0].message.content
                return resp_json.get("choices", [{}])[0].get("message", {}).get("content", "")
            elif provider.lower() == "groq":
                # Groq uses OpenAI-compatible format: choices[0].message.content
                return resp_json.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                return str(resp_json)
        return r.text

    except Exception as e:
        return json.dumps({"error": str(e)})


# ------------------- Generic wrapper -------------------
def _run_llm_task(task, text, provider, model=None, **options):
    model = model or DEFAULT_MODELS.get(provider, "")
    prompt = PROMPTS[task].format(text=text)
    prompt_tokens = estimate_tokens(prompt)

    start = time.time()
    try:
        output_text = _call_provider_api(task, prompt, provider, model, **options)
        completion_tokens = estimate_tokens(output_text)
        latency = time.time() - start
        error = None
    except Exception as e:
        output_text = ""
        completion_tokens = 0
        latency = time.time() - start
        error = str(e)

    return output_text, prompt_tokens, completion_tokens, latency, error

# ------------------- Public functions -------------------
def summarize(text, provider, model=None, **options):
    return _run_llm_task("summarize", text, provider, model, **options)

def analyze_sentiment(text, provider, model=None, **options):
    return _run_llm_task("sentiment", text, provider, model, **options)

def analyze_style(text, provider, model=None, **options):
    return _run_llm_task("style", text, provider, model, **options)
