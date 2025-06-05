import secrets
import hashlib
import base64


class generate_code_challenge:
    
    def generate_code_challenge():
        code_client = secrets.token_urlsafe(64)
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_client.encode())
                                              .digest()).rstrip(b'=').decode()
        return code_challenge
                                              
                         