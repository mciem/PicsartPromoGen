from random import choice

class utils:
    def __init__(self) -> None:
        self.__proxies = self.__loadFromFile("proxies")
    
    def __loadFromFile(self, file: str) -> list:
        with open(f"data/{file}.txt", "r", errors="ignore") as f:
            return f.read().splitlines()
    
    def write(self, file: str, data: str):
        with open(file, "a+") as f:
            f.write(data+"\n")
    
    def getProxy(self) -> str:
        return choice(self.__proxies)
    