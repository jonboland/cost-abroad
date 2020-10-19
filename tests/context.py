from pathlib import Path
import sys

# Enables cost_abroad module imports when running tests
context = Path(__file__).resolve().parents[1] / "cost_abroad"
sys.path.insert(0, str(context))