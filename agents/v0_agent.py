from transformers import pipeline, AutoTokenizer
import torch

# Load creative model
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
generator = pipeline(
    "text-generation",
    model=model_name,
    device=0 if torch.cuda.is_available() else -1
)

def process(prompt: str, max_tokens: int = 100) -> str:
    """v0 agent - optimized for creative/exploratory topics"""
    # Generate response with token constraint
    response = generator(
        prompt,
        max_new_tokens=max_tokens,
        num_return_sequences=1,
        temperature=0.7,
        top_k=50,
        truncation=True
    )
    return response[0]['generated_text'].replace(prompt, "").strip()

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))