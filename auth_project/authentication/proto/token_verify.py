import jwt
import logging


def token_verification(token):

    data = {
        "user_id": 0,
        "valid": False,
    }

    if not token:
        logging.warning("Token not provided in request.")
        return data["user_id"], data["valid"]

    try:
        secret_key = "taskauth"
        decoded_data = jwt.decode(token, "taskauth", algorithms=["HS256"])
        user_id = decoded_data.get("sub", {})
        data.update({"user_id": user_id, "valid": True})
        return data["user_id"], data["valid"]

    except jwt.ExpiredSignatureError:
        logging.error("Unauthorized. Expired authentication token.")
        data["message"] = "Unauthorized. Invalid authentication token."
        return data["user_id"], data["valid"]

    except jwt.InvalidTokenError as err:
        logging.error(
            "Unauthorized. Invalid authentication token:- %s", err, exc_info=True
        )
        return data["user_id"], data["valid"]

    except Exception as e:
        logging.error(
            "token_verification - Error while verifying auth token. Error: %s",
            str(e),
            exc_info=True,
        )
        return data["user_id"], data["valid"]
