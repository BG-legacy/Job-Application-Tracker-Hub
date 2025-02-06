import os
import environ
from pathlib import Path
from openai import OpenAI

# Setup similar to settings.py
BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def test_openai_connection():
    print("\n=== OpenAI API Connection Test ===")
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=env('OPENAI_API_KEY'))
        
        # Test API with a simple completion
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, API connection successful!' if you can read this."}
            ]
        )
        
        print("\n✅ API Connection Successful!")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print("\n❌ API Connection Failed!")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_openai_connection() 