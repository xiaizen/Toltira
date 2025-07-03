from . import bolt_agent, v0_agent
from utils.token_manager import optimize_responses
from utils.perf_tracker import tracker
import re

# Simple response cache
response_cache = {}

def allocate_tokens(prompt: str) -> tuple:
    """Dynamic token allocation based on content analysis"""
    from .bolt_agent import count_tokens as bolt_token_counter
    
    # Estimate prompt complexity
    prompt_tokens = bolt_token_counter(prompt)
    
    if prompt_tokens > 100:
        # Complex query - more tokens
        total = 400
        if any(kw in prompt.lower() for kw in ["creative", "design", "story"]):
            return (120, 280)  # Favor v0 for creative
        return (250, 150)     # Favor Bolt for complex technical
    elif prompt_tokens > 50:
        # Medium query
        total = 300
        return (160, 140)
    
    # Simple query
    total = 200
    return (100, 100)

def orchestrate(prompt: str, max_tokens: int = 300) -> str:
    """Coordinator with caching and smart token allocation"""
    tracker.start_timer()  # Start tracking performance
    
    # Cache check
    cache_key = prompt[:100].lower().replace(" ", "_")
    if cache_key in response_cache:
        # Use token counting function from agents
        token_count = bolt_agent.count_tokens(response_cache[cache_key])
        tracker.record(cache_hit=True, token_count=token_count)
        return response_cache[cache_key] + " [cached]"
    
    # Allocate tokens based on prompt content
    bolt_tokens, v0_tokens = allocate_tokens(prompt)
    
    # Get agent responses with token constraints
    bolt_res = bolt_agent.process(prompt, max_tokens=bolt_tokens)
    v0_res = v0_agent.process(prompt, max_tokens=v0_tokens)
    
    # Optimize and merge responses
    response = optimize_responses(bolt_res, v0_res, max_tokens)
    
    # Cache result
    response_cache[cache_key] = response
    
    # Record performance (use token counting function)
    token_count = bolt_agent.count_tokens(response)
    tracker.record(token_count=token_count)
    return response