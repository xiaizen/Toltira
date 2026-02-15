from transformers import pipeline, AutoTokenizer
import torch

# Global model loading
_model = None
_tokenizer = None

def load_model():
    global _model, _tokenizer
    if _model is None:
        model_name = "facebook/bart-large-mnli"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = pipeline(
            "zero-shot-classification",
            model=model_name,
            device=0 if torch.cuda.is_available() else -1
        )

def process(prompt: str, max_tokens: int = 100) -> str:
    """Bolt.new agent - optimized for technical/performance topics"""
    load_model()  # Ensure model is loaded
    
    # Define categories for efficient routing
    categories = ["performance", "optimization", "technical", "code", "algorithm"]
    
    # Classify prompt to determine relevance
    result = _model(prompt, categories, multi_label=False)
    
    if result['scores'][0] < 0.7:
        # Not technical enough - delegate to v0
        return "This appears to be a creative request. Passing to v0 for better handling."
    
    # Generate response with token constraint
    inputs = _tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=min(512, max_tokens * 2)
    )
    
    # Simplified generation for efficiency
    with torch.no_grad():
        output = _model.model.generate(**inputs, max_new_tokens=max_tokens)
    
    return _tokenizer.decode(output[0], skip_special_tokens=True)

def count_tokens(text: str) -> int:
    return len(_tokenizer.encode(text))