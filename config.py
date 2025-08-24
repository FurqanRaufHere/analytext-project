# config.py

# API Endpoints for each provider (for reference)
API_ENDPOINTS = {
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "gemini": "https://generativelanguage.googleapis.com/v1beta2/models/gemini-2.0-flash:generateText",
    "mistral": "https://api.mistral.ai/v1/models/devstral-medium-2507/completions",
}

# Per-provider cost estimates (per 1K tokens in USD)
PROVIDER_COSTS = {
    "groq": {
        "prompt": 0.002,      # Example placeholder
        "completion": 0.002,
    },
    "gemini": {
        "prompt": 0.001,
        "completion": 0.001,
    },
    "mistral": {
        "prompt": 0.0005,
        "completion": 0.0005,
    },
}

# Default model names for each provider
DEFAULT_MODELS = {
    "groq": "llama3-8b-8192",
    "gemini": "gemini-2.0-flash",
    "mistral": "devstral-medium-2507",
}
