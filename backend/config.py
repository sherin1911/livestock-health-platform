import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "livestock-health-platform-secret-key"
    )

    DATABASE_PATH = os.path.join(
        BASE_DIR,
        "instance",
        "livestock.db"
    )

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    MAX_CONTENT_LENGTH = 25 * 1024 * 1024

    ALLOWED_IMAGE_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "webp"
    }

    ALLOWED_AUDIO_EXTENSIONS = {
        "mp3",
        "wav",
        "m4a",
        "ogg",
        "webm"
    }