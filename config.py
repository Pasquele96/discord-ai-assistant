import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Bot Token
TOKEN = os.getenv('DISCORD_TOKEN')

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Bot command prefix
COMMAND_PREFIX = '!'

# Other configuration variables can be added here as needed