from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants

authorization = AuthorizationServer()

def config_oauth(app):
    # TEMP placeholders – you will replace these with real DB logic
    def query_client(client_id):
        return None  # Replace with DB lookup

    def save_token(token_data, request):
        pass  # Replace with DB save logic

    authorization.init_app(app, query_client=query_client, save_token=save_token)
    authorization.register_grant(grants.ResourceOwnerPasswordCredentialsGrant)
