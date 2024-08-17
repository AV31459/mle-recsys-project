import os
from dotenv import load_dotenv

load_dotenv('.env_service')

print(os.getenv('SERVICE_HOST', '!!!None!!!'))
