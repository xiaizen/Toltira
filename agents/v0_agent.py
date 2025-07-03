from transformers import pipeline, AutoTokenizer
import torch

# Global model loading
_model = None
_tokenizer = None

def load_model():
    global _model, _tokenizer
    if _model is None:
        model_name = "gpt2"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = pipeline(
            "text-generation",
            model=model_name,
            device=0 if torch.cuda.is_available() else -1
        )

def process(prompt: str, max_tokens: int = 100) -> str:
    """v0 agent - optimized for creative topics"""
    load_model()  # Ensure model is loaded
    
    # Generate response with token constraint
    response = _model(
        prompt,
        max_new_tokens=max_tokens,
        num_return_sequences=1,
        temperature=0.7,
        top_k=50,
        truncation=True,
        pad_token_id=_tokenizer.eos_token_id  # Add this to suppress warning
    )
    return response[0]['generated_text'].replace(prompt, "").strip()

def count_tokens(text: str) -> int:
    return len(_tokenizer.encode(text))