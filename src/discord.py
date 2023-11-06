from .client import buildClient

from functools           import wraps
from tls_client.response import Response

def response(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        data: Response = func(*args, **kwargs)
        
        response = {
            "json": data.json(),
            "status_code": data.status_code,
            "success": data.status_code in (200, 201, 203, 204)
        }
        
        return response
    
    return wrapper

class discord:
    def __init__(
        self,
        token: str,
        proxy: str
    ) -> None:
        
        self.session = buildClient(proxy, "discord.com")
        self.session.headers |= {
            "authorization": token,
            "x-discord-timezone": "Europe/Warsaw",
			"x-debug-options": "bugReporterEnabled",
			"x-discord-locale": "pl",
			"x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InBsLVBMIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI0MzU4OCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        }
        
    @response
    def extract_link(
        self,
        link: str
    ):
        
        headers = self.session.headers.copy()
        headers["referer"] = link
        
        spl = link.split("/")
        idd = spl[5]
        jwt = spl[6]
        
        return self.session.post(
            f"https://discord.com/api/v9/entitlements/partner-promotions/{idd}",
            json={
                "jwt": jwt
            },
            headers=headers
        )