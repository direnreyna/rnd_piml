# main.py

"""
Main orchestration script for testing environment detection and device usage.
"""

from adapter import EnvironmentAdapter

def main() -> None:
    """
    Main function to initialize the adapter and print environment info.
    """
    adapter = EnvironmentAdapter()
    description = adapter.describe_environment()
    print(description)

if __name__ == "__main__":
    main()