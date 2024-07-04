import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
GET_LINKS_API = os.getenv('GET_LINKS_API')
SEND_LINKS_API = os.getenv('SEND_LINKS_API')
SEND_VECTOR_API = os.getenv('SEND_VECTOR_API')
