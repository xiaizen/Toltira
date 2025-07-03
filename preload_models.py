from agents import bolt_agent, v0_agent
import contextlib
import sys
import io

@contextlib.contextmanager
def suppress_stdout():
    """Temporarily suppress stdout output"""
    original = sys.stdout
    sys.stdout = io.StringIO()
    try:
        yield
    finally:
        sys.stdout = original

print("⚙️ Preloading AI models...")
# Suppress model loading output
with suppress_stdout():
    bolt_agent.process("Warmup")
    v0_agent.process("Warmup")
print("✅ Models loaded and ready!")