import os
from dotenv import load_dotenv
import typesense

load_dotenv()

if not os.environ.get("SEARCH_API_KEY"):
  raise ValueError("Typesense API key not set")

typesense_client = typesense.Client({
  'nodes': [{
    'host': os.environ.get("TYPESENSE_HOST"),
    'port': os.environ.get("TYPESENSE_PORT"),
    'protocol': os.environ.get("TYPESENSE_PROTOCOL")
  }],
  'api_key': os.environ.get("ADMIN_API_KEY"),
  'connection_timeout_seconds': 2
})

typesense_search_client = typesense.Client({
  'nodes': [{
    'host': os.environ.get("TYPESENSE_HOST"),
    'port': os.environ.get("TYPESENSE_PORT"),
    'protocol': os.environ.get("TYPESENSE_PROTOCOL")
  }],
  'api_key': os.environ.get("SEARCH_API_KEY"),
  'connection_timeout_seconds': 2
})


def create_schema():
  """
  Run this function inside python shell once, to create the collection
  """
  schema = {
    'name': 'journal_entries',
    'fields': [
        {'name': 'id', 'type': 'string'},
        {'name': 'journal_title', 'type': 'string'},
        {'name': 'input_text', 'type': 'string'},
        {'name': 'response_text', 'type': 'string'},
        {'name': 'created_at', 'type': 'int64', 'facet': True}
    ],
    'default_sorting_field': 'created_at'
  }

  try:
    typesense_client.collections.create(schema)
  except Exception as e:
    print(f"Collection already exists or creation failed: {e}")
