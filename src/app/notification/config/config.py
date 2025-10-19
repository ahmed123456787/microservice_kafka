from dotenv import load_dotenv
import os 

ENV_FILE = os.path.join(os.path.dirname(__file__), '../.env.dev')

# Load environment variables from .env file if it exists
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)


class AppConfig:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv('PORT', 8000))
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
    HOST = os.getenv('HOST', 'localhost')
    

AppConfig = AppConfig()