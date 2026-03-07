"""
Run Second Brain automated tests.
Supports run_in_repl mode: returns results as string for chat-based runs in code_execution.
"""

import os
import sys
import io
import unittest


def run_in_repl(verbosity: int = 2) -> str:
    """
    Discover and run tests; return output as string for chat/code_execution.
    """
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=verbosity)
    result = runner.run(suite)
    out = stream.getvalue()
    summary = f"\nRan {result.testsRun} tests. Failures: {len(result.failures)}, Errors: {len(result.errors)}, Skipped: {len(result.skipped)}."
    return out + summary


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--repl":
        print(run_in_repl())
        return 0
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
