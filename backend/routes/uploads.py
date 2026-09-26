from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

import os
import uuid


uploads_bp = Blueprint(
    "uploads",
    __name__,
    url_prefix="/api/uploads",
)


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOADS_DIR = os.path.join(
    BASE_DIR,
    "uploads",
)

PHOTO_DIR = os.path.join(
    UPLOADS_DIR,
    "photos",
)

AUDIO_DIR = os.path.join(
    UPLOADS_DIR,
    "audio",
)


os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)


# ============================================================
# FILE SETTINGS
# ============================================================

ALLOWED_PHOTO_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
}

ALLOWED_AUDIO_EXTENSIONS = {
    "mp3",
    "wav",
    "m4a",
    "aac",
    "ogg",
    "webm",
}


# ============================================================
# HELPERS
# ============================================================

def get_extension(filename):
    if not filename or "." not in filename:
        return ""

    return filename.rsplit(".", 1)[1].lower()


def allowed_file(filename, allowed_extensions):
    extension = get_extension(filename)

    return extension in allowed_extensions


def create_unique_filename(filename):
    original_name = secure_filename(filename)

    if not original_name:
        original_name = "upload"

    extension = get_extension(original_name)

    unique_id = uuid.uuid4().hex

    if extension:
        return f"{unique_id}.{extension}"

    return unique_id


def save_uploaded_file(file, destination_directory):
    if file is None:
        return None

    if not file.filename:
        return None

    stored_name = create_unique_filename(file.filename)

    file_path = os.path.join(
        destination_directory,
        stored_name,
    )

    file.save(file_path)

    return stored_name


def build_file_response(
    file_type,
    stored_name,
    original_name,
):
    if file_type == "photo":
        relative_url = f"/api/uploads/photos/{stored_name}"
    else:
        relative_url = f"/api/uploads/audio/{stored_name}"

    return {
        "success": True,
        "message": "File uploaded successfully.",
        "type": file_type,
        "originalName": original_name,
        "fileName": stored_name,
        "filename": stored_name,
        "url": relative_url,
        "path": relative_url,
    }


# ============================================================
# PHOTO UPLOAD
# ============================================================

@uploads_bp.route("/photo", methods=["POST"])
@uploads_bp.route("/photos", methods=["POST"])
@jwt_required()
def upload_photo():
    file = request.files.get("photo")

    if file is None:
        file = request.files.get("image")

    if file is None:
        file = request.files.get("file")

    if file is None:
        return jsonify(
            {
                "success": False,
                "message": "No photo file was provided.",
            }
        ), 400

    original_name = file.filename

    if not allowed_file(
        original_name,
        ALLOWED_PHOTO_EXTENSIONS,
    ):
        return jsonify(
            {
                "success": False,
                "message": (
                    "Invalid photo format. "
                    "Allowed formats: JPG, JPEG, PNG and WEBP."
                ),
            }
        ), 400

    try:
        stored_name = save_uploaded_file(
            file,
            PHOTO_DIR,
        )

        if not stored_name:
            return jsonify(
                {
                    "success": False,
                    "message": "Unable to save the photo.",
                }
            ), 500

        response_data = build_file_response(
            "photo",
            stored_name,
            original_name,
        )

        return jsonify(response_data), 201

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Photo upload failed.",
                "error": str(error),
            }
        ), 500


# ============================================================
# AUDIO UPLOAD
# ============================================================

@uploads_bp.route("/audio", methods=["POST"])
@uploads_bp.route("/audios", methods=["POST"])
@jwt_required()
def upload_audio():
    file = request.files.get("audio")

    if file is None:
        file = request.files.get("voice")

    if file is None:
        file = request.files.get("file")

    if file is None:
        return jsonify(
            {
                "success": False,
                "message": "No audio file was provided.",
            }
        ), 400

    original_name = file.filename

    if not allowed_file(
        original_name,
        ALLOWED_AUDIO_EXTENSIONS,
    ):
        return jsonify(
            {
                "success": False,
                "message": (
                    "Invalid audio format. "
                    "Allowed formats: MP3, WAV, M4A, AAC, OGG and WEBM."
                ),
            }
        ), 400

    try:
        stored_name = save_uploaded_file(
            file,
            AUDIO_DIR,
        )

        if not stored_name:
            return jsonify(
                {
                    "success": False,
                    "message": "Unable to save the audio.",
                }
            ), 500

        response_data = build_file_response(
            "audio",
            stored_name,
            original_name,
        )

        return jsonify(response_data), 201

    except Exception as error:
        return jsonify(
            {
                "success": False,
                "message": "Audio upload failed.",
                "error": str(error),
            }
        ), 500


# ============================================================
# SERVE PHOTOS
# ============================================================

@uploads_bp.route("/photos/<path:filename>", methods=["GET"])
def serve_photo(filename):
    safe_name = os.path.basename(filename)

    if not safe_name:
        return jsonify(
            {
                "success": False,
                "message": "Invalid photo filename.",
            }
        ), 400

    file_path = os.path.join(
        PHOTO_DIR,
        safe_name,
    )

    if not os.path.isfile(file_path):
        return jsonify(
            {
                "success": False,
                "message": "Photo not found.",
            }
        ), 404

    return send_from_directory(
        PHOTO_DIR,
        safe_name,
    )


# ============================================================
# SERVE AUDIO
# ============================================================

@uploads_bp.route("/audio/<path:filename>", methods=["GET"])
def serve_audio(filename):
    safe_name = os.path.basename(filename)

    if not safe_name:
        return jsonify(
            {
                "success": False,
                "message": "Invalid audio filename.",
            }
        ), 400

    file_path = os.path.join(
        AUDIO_DIR,
        safe_name,
    )

    if not os.path.isfile(file_path):
        return jsonify(
            {
                "success": False,
                "message": "Audio not found.",
            }
        ), 404

    return send_from_directory(
        AUDIO_DIR,
        safe_name,
    )


# ============================================================
# UPLOAD STATUS
# ============================================================

@uploads_bp.route("/status", methods=["GET"])
def upload_status():
    photos_folder_ready = os.path.isdir(PHOTO_DIR)
    audio_folder_ready = os.path.isdir(AUDIO_DIR)

    return jsonify(
        {
            "success": True,
            "status": "operational",
            "photoUploads": photos_folder_ready,
            "audioUploads": audio_folder_ready,
            "allowedPhotoFormats": sorted(
                list(ALLOWED_PHOTO_EXTENSIONS)
            ),
            "allowedAudioFormats": sorted(
                list(ALLOWED_AUDIO_EXTENSIONS)
            ),
        }
    ), 200