from transformers import AutoTokenizer

# Load tokenizers (free, locally)
tokenizers = {
    "gpt2": AutoTokenizer.from_pretrained("gpt2"),
    "bert": AutoTokenizer.from_pretrained("bert-base-uncased"),
    "roberta": AutoTokenizer.from_pretrained("roberta-base")
}

def tokenize_text(text: str):
    """Returns token lists and counts for all tokenizers."""
    if not text or not text.strip():
        return {k: {"tokens": [], "count": 0} for k in tokenizers.keys()}

    results = {}
    for name, tokenizer in tokenizers.items():
        try:
            tokens = tokenizer.tokenize(text)
        except Exception:
            # Handle unusual characters safely
            text_clean = text.encode("utf-8", errors="ignore").decode("utf-8")
            tokens = tokenizer.tokenize(text_clean)

        # Truncate long token lists for UI display
        display_tokens = tokens[:50] if len(tokens) > 50 else tokens
        results[name] = {
            "tokens": display_tokens,
            "count": len(tokens)
        }
    return results
