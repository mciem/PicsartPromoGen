from src.capsolver import capsolver
from src.picsart   import picsart
from src.console   import console
from src.utils     import utils

from threading import Lock, Thread

import yaml
import time

class promo:
    def __init__(self) -> None:
        self.lock = Lock()
        
        self.cfg = yaml.safe_load(open("config.yaml"))
        
        self.utls = utils()
        self.cnsl = console()
        self.cpsl = capsolver(self.cfg["capsolver"]["key"])
        
        self.promos = 0
    
    def gen(self):
        proxy = self.utls.getProxy()
        
        picsr = picsart(proxy)
        
        st = time.time()
        greca = self.cpsl.solve_captcha(proxy)
        self.cnsl.log("SLV", "solved captcha", {"key": greca[:16]}, time.time()-st)
        
        email, passw = f"{picsart.rand_string(16)}@gmail.com", picsart.rand_string(8)+"!@#"
        self.cnsl.log("DBG", "creating account", {"email": email, "password": passw})
        
        st = time.time()
        acc = picsr.create_account(greca, email, passw)
        if acc["success"]:
            bearer = acc["json"]["token"]["access_token"]
            apikey = acc["json"]["key"]
            
            picsr.session.headers |= {
                "authorization": f"Bearer {bearer}",
                "x-api-key": apikey
            }
            
            self.cnsl.log("ACC", "created account", {"authorization": bearer[:16], "api-key": apikey[:16]}, time.time()-st)
            
            st = time.time()
            lnk = picsr.get_discord_link()
            if lnk["success"]:
                link = lnk["json"]["response"]
                
                with self.lock:
                    self.promos += 1
                    
                    self.cnsl.log("PRO", "got promo link", {"link": link[:16], "total": self.promos}, time.time()-st)
                    self.utls.write("data/promos.txt", link)
            
            else:
                self.cnsl.log("ERR", "failed to get promo link", {"reason": acc["json"]["message"]})
        
        else:
            self.cnsl.log("ERR", "failed to generate account", {"reason": acc["json"]["message"]})
    
    def loop(self):
        while True:
            try:                   self.gen()
            except Exception as e: self.cnsl.log("ERR", "error occured", {"value": str(e)})  
    
    def start(self):
        for _ in range(self.cfg["gen"]["threads"]):
            Thread(target=self.loop).start()
            

if __name__ == "__main__":
    promo().start()