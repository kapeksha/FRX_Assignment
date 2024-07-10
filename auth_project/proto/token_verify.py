import jwt
import logging


def token_verification(token):

    data = {
        "success": False,
        "user_id": 0,
    }

    if not token:
        logging.warning("Token not provided in request.")
        return data["success"], data["user_id"]

    try:
        secret_key = "taskauth"
        decoded_data = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = decoded_data.get("sub", {}).get("user_id", 0)
        data.update({"success": True, "user_id": user_id})
        return data["success"], data["user_id"]

    except jwt.ExpiredSignatureError:
        logging.error("Unauthorized. Expired authentication token.")
        data["message"] = "Unauthorized. Invalid authentication token."
        return data["success"], data["user_id"]

    except jwt.InvalidTokenError:
        logging.error("Unauthorized. Invalid authentication token.")
        return data["success"], data["user_id"]

    except Exception as e:
        logging.error(
            "token_verification - Error while verifying auth token. Error: %s",
            str(e),
            exc_info=True,
        )
        return data["success"], data["user_id"]
