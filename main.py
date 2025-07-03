import preload_models  # Must be first to preload models
from agents.orchestrator import orchestrate
from utils.perf_tracker import tracker
import time

def main():
    print("\n⚡ Bolt-v0 Unified AI System")
    print("==============================")
    print("Type your prompt (or 'exit' to quit)\n")
    
    try:
        while True:
            # Show stats in the prompt
            prompt = input(f"You [{tracker.stats()}]: ")
            if prompt.lower() in ['exit', 'quit']:
                break
                
            start_time = time.perf_counter()
            response = orchestrate(prompt)
            elapsed = (time.perf_counter() - start_time) * 1000
            
            print(f"\n🤖 AI Response ({elapsed:.0f}ms):")
            print('-' * 60)
            print(response)
            print('-' * 60)
            print()  # Extra line for spacing
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
    finally:
        print("\n📊 Final Statistics:")
        print(f"Total Queries: {tracker.total_queries}")
        print(f"Cache Hit Rate: {tracker.cache_hits/tracker.total_queries*100:.1f}%")
        print(f"Average Response Time: {sum(tracker.times)/len(tracker.times):.1f}ms")
        print("Goodbye!")

if __name__ == "__main__":
    main()