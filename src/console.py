from datetime  import datetime
from threading import RLock
from colorama  import Fore, init

import os

init(convert=True)

class console:
    lock = RLock()
    
    black  = Fore.LIGHTBLACK_EX
    white  = Fore.LIGHTWHITE_EX
    red    = Fore.LIGHTRED_EX
    green  = Fore.LIGHTGREEN_EX
    blue   = Fore.LIGHTBLUE_EX
    yellow = Fore.LIGHTYELLOW_EX
    cyan   = Fore.CYAN
    purple = "\033[35m"
    orange = "\033[33m"
    pink   = "\033[95m"
    
    logs = {
        "DBG": blue,
        "ERR": red,
        "ACC": green,
        "PRO": purple,
        "SLV": pink
    }
    
    def clear(self):
        os.system("cls")
    
    def log(self, log_type: str, text: str = "", var: dict = {}, time: float = 0.0):
        with self.lock:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            
            if log_type == "INP":
                print(f"{self.white}{current_time} {self.logs[log_type]}{log_type} {self.white}{text} » ", end="")
                return input()
            
            elif var != {}:
                text += f"{self.black} "
                
                i = 0
                for v,k in var.items():
                    text += f" {self.white}{v} » {self.black}{k}"
                    if i != len(var)-1:
                        text += f"{self.white},"
                        
                    i += 1
                
            if time == 0.0:
                print(f"{self.white}{current_time} {self.logs[log_type]}{log_type} {self.white}{text}{self.white}")
            else:
                print(f"{self.white}{current_time} {self.logs[log_type]}{log_type} {self.white}{text} {self.black}({self.white}{time:.2f}s{self.black}){self.white}")