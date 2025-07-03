import time
import math

class PerformanceTracker:
    def __init__(self):
        self.start_time = 0
        self.times = []
        self.cache_hits = 0
        self.total_queries = 0
        self.token_counts = []
    
    def start_timer(self):
        self.start_time = time.time()
    
    def record(self, cache_hit=False, token_count=0):
        elapsed_ms = (time.time() - self.start_time) * 1000
        self.times.append(elapsed_ms)
        self.token_counts.append(token_count)
        self.total_queries += 1
        if cache_hit:
            self.cache_hits += 1
    
    def stats(self):
        if not self.times:
            return "No queries yet"
        
        avg_time = sum(self.times) / len(self.times)
        avg_tokens = sum(self.token_counts) / len(self.token_counts) if self.token_counts else 0
        cache_rate = (self.cache_hits / self.total_queries) * 100
        
        # Calculate performance grade (A-F)
        time_grade = "A" if avg_time < 50 else "B" if avg_time < 100 else "C" if avg_time < 200 else "D" if avg_time < 500 else "F"
        
        return (
            f"⏱️ {avg_time:.1f}ms avg ({time_grade}) | "
            f"🗝️ {cache_rate:.1f}% cache | "
            f"📊 {avg_tokens:.0f} avg tokens"
        )

# Global tracker instance
tracker = PerformanceTracker()