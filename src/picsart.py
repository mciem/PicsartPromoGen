from .client import buildClient

from string              import ascii_letters, digits
from random              import choices
from functools           import wraps
from tls_client.response import Response

def response(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        data: Response = func(*args, **kwargs)
        
        response = {
            "json": data.json(),
            "status_code": data.status_code,
        }
        
        response["success"] = response["json"]["status"] == "success"
        
        return response
    
    return wrapper


class picsart:
    def __init__(
        self,
        proxy: str
    ) -> None:
        
        self.session = buildClient(proxy, "picsart.com")
    
    @staticmethod
    def rand_string(
        n: int
    ) -> str:
        
        return "".join(choices(ascii_letters+digits, k=n))
    
    @response
    def create_account(
        self,
        g_recaptcha_token: str,
        email: str,
        password: str
    ) -> dict[str, any]:
        
        headers = self.session.headers.copy()
        headers |= {
            "g-recaptcha-action": "signup",
            "g-recaptcha-token": g_recaptcha_token,
            "token": "hI3KTwebV5yr2Gj" # it doesnt change ig
        }
        

        return self.session.post(
            "https://api.picsart.com/user-account/auth/signup",
            json={
                "consents": [],
                "email": email,
                "password": password
            },
            headers=headers
        )
    
    @response
    def get_discord_link(self):
        return self.session.get(
            "https://api.picsart.com/discord/link"
        )