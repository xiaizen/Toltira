import preload_models  # Add this line at the very top
from agents.orchestrator import orchestrate

def main():
    print("🤖 Bolt-v0 Unified AI System")
    print("Type your prompt (or 'exit' to quit)\n")
    
    while True:
        prompt = input("You: ")
        if prompt.lower() in ['exit', 'quit']:
            break
            
        response = orchestrate(prompt)
        print(f"\nAI: {response}\n")

if __name__ == "__main__":
    main()
    from agents.orchestrator import orchestrate
import time

def main():
    print("⚡ Bolt-v0 Unified AI System")
    print("Type your prompt (or 'exit' to quit)\n")
    
    while True:
        prompt = input("You: ")
        if prompt.lower() in ['exit', 'quit']:
            break
            
        start_time = time.time()
        response = orchestrate(prompt)
        elapsed = (time.time() - start_time) * 1000
        
        print(f"\nAI ({elapsed:.0f}ms):\n{'-'*40}")
        print(response)
        print(f"{'-'*40}\n")

if __name__ == "__main__":
    main()