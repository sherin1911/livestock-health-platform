from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


# ============================================================
# ALLOWED ROLES
# ============================================================

ROLES = {
    "FARMER",
    "FIELD_WORKER",
    "VETERINARIAN",
    "LAB_STAFF",
    "DISTRICT_OFFICER",
    "STATE_ADMIN",
    "SUPER_ADMIN"
}


# ============================================================
# GET CURRENT IDENTITY
# ============================================================

def get_current_identity():

    identity = get_jwt_identity()

    if not isinstance(identity, dict):
        return {
            "user_id": None,
            "username": identity,
            "role": "FARMER"
        }

    return {
        "user_id": identity.get("user_id"),
        "username": identity.get("username"),
        "role": str(
            identity.get("role") or "FARMER"
        ).upper()
    }


# ============================================================
# GET CURRENT ROLE
# ============================================================

def get_current_role():

    identity = get_current_identity()

    return identity["role"]


# ============================================================
# CHECK ROLE
# ============================================================

def user_has_role(*allowed_roles):

    current_role = get_current_role()

    normalized_roles = {
        str(role).upper()
        for role in allowed_roles
    }

    return current_role in normalized_roles


# ============================================================
# ROLE REQUIRED DECORATOR
# ============================================================

def role_required(*allowed_roles):

    normalized_roles = {
        str(role).upper()
        for role in allowed_roles
    }

    def decorator(function):

        @wraps(function)
        @jwt_required()
        def wrapped_function(*args, **kwargs):

            identity = get_current_identity()

            current_role = identity["role"]

            if current_role not in normalized_roles:

                return jsonify({
                    "success": False,
                    "message": (
                        "You do not have permission "
                        "to access this resource."
                    ),
                    "requiredRoles":
                        sorted(
                            list(
                                normalized_roles
                            )
                        ),
                    "currentRole":
                        current_role
                }), 403

            return function(
                *args,
                **kwargs
            )

        return wrapped_function

    return decorator


# ============================================================
# ADMIN DECORATOR
# ============================================================

def admin_required():

    return role_required(
        "STATE_ADMIN",
        "SUPER_ADMIN"
    )


# ============================================================
# GOVERNMENT DECORATOR
# ============================================================

def government_required():

    return role_required(
        "DISTRICT_OFFICER",
        "STATE_ADMIN",
        "SUPER_ADMIN"
    )


# ============================================================
# VETERINARY DECORATOR
# ============================================================

def veterinary_required():

    return role_required(
        "VETERINARIAN"
    )


# ============================================================
# LABORATORY DECORATOR
# ============================================================

def laboratory_required():

    return role_required(
        "LAB_STAFF"
    )


# ============================================================
# FARMER / FIELD WORKER DECORATOR
# ============================================================

def field_reporting_required():

    return role_required(
        "FARMER",
        "FIELD_WORKER"
    )


# ============================================================
# OPERATIONAL USER DECORATOR
# ============================================================

def operational_user_required():

    return role_required(
        "FIELD_WORKER",
        "VETERINARIAN",
        "LAB_STAFF",
        "DISTRICT_OFFICER",
        "STATE_ADMIN",
        "SUPER_ADMIN"
    )


# ============================================================
# SUPER ADMIN DECORATOR
# ============================================================

def super_admin_required():

    return role_required(
        "SUPER_ADMIN"
    )