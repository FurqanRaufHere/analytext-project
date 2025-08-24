from utils.tokenizer_helpers import tokenize_text

sample_texts = [
    "Hello world! This is a short tweet.",
    "This is a very long text " * 30,  # long text
    "Special chars: ñ, ü, 🚀, ©, €"
]

for text in sample_texts:
    result = tokenize_text(text)
    print(result)
