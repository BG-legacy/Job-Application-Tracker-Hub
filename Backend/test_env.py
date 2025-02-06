import os
import environ
from pathlib import Path

# Setup similar to settings.py
BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def test_env_variables():
    print("\n=== Environment Variables Test ===")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"ENV file path: {os.path.join(BASE_DIR, '.env')}")
    print(f"ENV file exists: {os.path.exists(os.path.join(BASE_DIR, '.env'))}")
    
    # Test OpenAI API Key
    api_key = env('OPENAI_API_KEY', default='Not found')
    print(f"\nOpenAI API Key: {'Found (not shown for security)' if api_key != 'Not found' else 'Not found'}")
    print(f"API Key length: {len(api_key) if api_key != 'Not found' else 0}")

if __name__ == "__main__":
    test_env_variables() 