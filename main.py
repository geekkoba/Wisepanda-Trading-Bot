from dotenv import load_dotenv
load_dotenv()

from src.database import main as database
from src.telegram import main as telegram
from src.engine import main as engine

database.initialize()

engine.initialize()

telegram.initialize()
