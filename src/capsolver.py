from httpx import Client
from time  import sleep

class capsolver:
    def __init__(
        self,
        api_key: str
    ) -> None:
        
        self.api_key = api_key
        self.session = Client(headers={
            "Host": "api.capsolver.com",
            "Content-Type": "application/json"
        }, timeout=20)
    
    def __create_task(
        self,
        proxy: str
    ) -> dict:
        
        return self.session.post(
            "https://api.capsolver.com/createTask",
            json={
                "clientKey": self.api_key,
                "task": {
                    "type": "ReCaptchaV3M1TaskProxyLess",
                    "websiteURL": "https://picsart.com",
                    "websiteKey": "6LdM2s8cAAAAAN7jqVXAqWdDlQ3Qca88ke3xdtpR",
                    "pageAction": "signup",
                    "minScore":   0.9,
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                    #"proxy": f"http://{proxy}"
                }
            }
        ).json()
    
    def __check_status(
        self,
        task_id: str
    ) -> dict:
        
        return self.session.post(
            "https://api.capsolver.com/getTaskResult",
            json={
                "clientKey": self.api_key,
                "taskId": task_id
            }
        ).json()
    
    def solve_captcha(
        self,
        proxy: str
    ) -> str:
        task = self.__create_task(proxy)
        
        if task["errorId"] == 1:
            raise Exception(f"failed to create task: {task['errorDescription']}")
        
        retrie = 0
        status = self.__check_status(task["taskId"])
        while status["status"] == "processing":
            if retrie == 20:
                raise Exception("failed to get task solution")
            
            sleep(1)
            
            status = self.__check_status(task["taskId"])
            retrie += 1
        
        return status["solution"]["gRecaptchaResponse"]
            