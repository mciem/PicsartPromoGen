from tls_client import Session

def buildClient(proxy: str, url: str) -> None:
    session = Session(random_tls_extension_order=True, client_identifier='chrome_117')
    session.headers = {
		"accept":             "*/*",
		"accept-language":    "en-US;q=0.8,en;q=0.7",
		"content-type":       "application/json",
        "connection":         "keep-alive",
		"host":               url,
		"origin":             f"https://{url}",
        "platform":           "website",
		"sec-ch-ua":          '"Chromium";v="117", "Google Chrome";v="117", "Not;A=Brand";v="99"',
		"sec-ch-ua-mobile":   "?0",
		"sec-ch-ua-platform": '"Windows"',
		"sec-fetch-dest":     "empty",
		"sec-fetch-mode":     "cors",
		"sec-fetch-site":     "same-site",
		"user-agent":         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }

    session.proxies = f"http://{proxy}" if proxy is not None else None
    session.get(f"https://{url}")
        
    return session