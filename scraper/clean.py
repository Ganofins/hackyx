import typesense
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = typesense.Client({
  'nodes': [{
    'host': os.getenv("TYPESENSE_HOST"),
    'port': os.getenv("TYPESENSE_PORT"),      
    'protocol': os.getenv("TYPESENSE_PROTOCOL")   
  }],
  'api_key': os.getenv("TYPESENSE_API_KEY"),
  'connection_timeout_seconds': 2
})

count = client.collections['contents'].retrieve()['num_documents']
print("Cleaning...")
for i in range(count):
    try:
        document = client.collections['contents'].documents[str(i)].retrieve()
        if "youtube" in document.get('url') or "youtu.be" in document.get('url'):
          client.collections['contents'].documents[str(i)].delete()
          print(f"{document.get('url')} deleted successfully")
    except Exception as e:
        print(f"Failed to delete document {i}: {e}")
