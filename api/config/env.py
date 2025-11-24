# config/env.py
import os
from dotenv import load_dotenv

from api.utils.types import str_to_bool, to_float, to_int  # type: ignore

# Load .env for local development if available
if load_dotenv is not None:
    load_dotenv()


class Config:
    # Core flags
    DEBUG = str_to_bool(
        os.getenv("FLASK_DEBUG", os.getenv("DEBUG", "true")), default=True
    )

    # CORS
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS", "*"
    )  # e.g. "http://localhost:5173,https://mydemo.com"

    # Blockchain demo tunables
    DIFFICULTY = to_int("DIFFICULTY", 2)
    TARGET_BLOCK_TIME = to_int("TARGET_BLOCK_TIME", 3)
    RETARGET_INTERVAL = to_int("RETARGET_INTERVAL", 5)
    BLOCK_REWARD = to_float("BLOCK_REWARD", 10.0)

    # Server port (used if you wire it into app.run or FLASK CLI)
    PORT = to_int("PORT", 5000)
