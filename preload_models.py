from agents import bolt_agent, v0_agent

print("⚙️ Preloading AI models...")
bolt_agent.process("Initialization")
v0_agent.process("Initialization")
print("✅ Models loaded and ready!")
from agents import bolt_agent, v0_agent
import contextlib
import io

@contextlib.contextmanager
def suppress_stdout():
    """Temporarily suppress stdout output"""
    with open(io.StringIO(), 'w') as buffer:
        original = __import__('sys').stdout
        __import__('sys').stdout = buffer
        try:
            yield
        finally:
            __import__('sys').stdout = original

print("⚙️ Preloading AI models...")
# Suppress model loading output
with suppress_stdout():
    bolt_agent.process("Warmup")
    v0_agent.process("Warmup")
print("✅ Models loaded and ready!")