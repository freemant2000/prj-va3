from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from disl import Inject

class GoogleOAuth2:
    def __init__(self) -> None:
        self.client_secret_file=Inject()
        self.redirect_uri=Inject()

    def get_redirect_uri(self)->str:
        flow=self.make_flow()
        url, state=flow.authorization_url(access_type="offline")
        return url

    def make_flow(self)->Flow:
        flow=Flow.from_client_secrets_file(self.client_secret_file,
                                        scopes=["https://www.googleapis.com/auth/userinfo.email",
                                                "openid"])
        flow.redirect_uri=self.redirect_uri
        return flow

    def get_creds_with_code(self, code: str)->Credentials:
        flow=self.make_flow()
        flow.fetch_token(code=code)
        creds=flow.credentials
        return creds
