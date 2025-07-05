import secrets
import hashlib
import base64


class generate_code_challenge:
    # Will most likely be used only for APIs that require it
    # If it gets used more than once I will make an Abstract Base Class
    def generate_code_challenge() -> str:
        code_client = secrets.token_urlsafe(64)
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_client.encode())
                                              .digest()).rstrip(b'=').decode()
        return code_challenge
                                              
                         