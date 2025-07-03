from transformers import GPT2Tokenizer
import re
from collections import defaultdict

# Initialize tokenizer once
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def optimize_responses(bolt_res: str, v0_res: str, max_tokens: int = 300) -> str:
    """
    Advanced response merging with:
    1. Semantic deduplication using key concepts
    2. Sentence scoring for importance
    3. Token-aware truncation
    4. Context-aware merging
    """
    # Split responses into sentences with better handling
    sentence_endings = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
    bolt_sentences = [s.strip() for s in re.split(sentence_endings, bolt_res) if s.strip()]
    v0_sentences = [s.strip() for s in re.split(sentence_endings, v0_res) if s.strip()]
    
    # Score sentences by importance
    scored_sentences = []
    for source, sentences in [('bolt', bolt_sentences), ('v0', v0_sentences)]:
        for s in sentences:
            # Score based on key phrases and structure
            score = 1.0
            if 'key insight' in s.lower(): score += 2.0
            if 'recommend' in s.lower(): score += 1.5
            if 'solution' in s.lower(): score += 1.2
            if 'important' in s.lower(): score += 1.0
            if s.endswith(':'): score += 0.8  # Likely heading
            if len(s.split()) > 15: score -= 0.3  # Penalize long sentences
            scored_sentences.append((s, score, source))
    
    # Remove duplicates using key concepts
    unique_sentences = []
    concept_map = defaultdict(list)
    
    for sentence, score, source in scored_sentences:
        # Extract key concepts (nouns and verbs)
        words = re.findall(r'\b(\w{4,})\b', sentence.lower())
        concepts = {w for w in words if w not in {'this', 'that', 'there', 'which'}}
        
        # Check if concept already covered
        is_duplicate = False
        for concept in concepts:
            if concept in concept_map:
                for existing in concept_map[concept]:
                    if existing[0] == sentence:  # Exact duplicate
                        is_duplicate = True
                    elif concept in key_concepts(existing[0]):  # Semantic duplicate
                        # Keep the higher scored version
                        if score > existing[1]:
                            unique_sentences.remove(existing)
                            concept_map[concept].remove(existing)
                        else:
                            is_duplicate = True
        
        if not is_duplicate:
            unique_sentences.append((sentence, score, source))
            for concept in concepts:
                concept_map[concept].append((sentence, score, source))
    
    # Sort by importance
    unique_sentences.sort(key=lambda x: x[1], reverse=True)
    
    # Build final response within token limit
    final_response = []
    token_count = 0
    
    for sentence, _, source in unique_sentences:
        tokens = tokenizer.encode(sentence, add_special_tokens=False)
        token_length = len(tokens)
        
        if token_count + token_length <= max_tokens:
            prefix = "🔩 BOLT: " if source == "bolt" else "🚀 V0: "
            final_response.append(prefix + sentence)
            token_count += token_length
        else:
            # Add partial content if significant space remains
            remaining = max_tokens - token_count
            if remaining > 10:  # Enough for at least a few words
                partial = tokenizer.decode(tokens[:remaining]) + "..."
                prefix = "🔩 BOLT: " if source == "bolt" else "🚀 V0: "
                final_response.append(prefix + partial)
            break
    
    return '\n\n'.join(final_response)

def key_concepts(sentence: str) -> set:
    """Extract key concepts from a sentence"""
    words = re.findall(r'\b(\w{4,})\b', sentence.lower())
    return {w for w in words if w not in {'this', 'that', 'there', 'which', 'should', 'could'}}