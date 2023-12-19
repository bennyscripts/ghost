import requests

def shorten(url: str) -> str:
    data = {"url": url, "domain": "0"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "cookie": "PHPSESSID=2tn011k8lj2a4o11lafj5nakvm"
    }

    response = requests.post("https://cutt.ly/scripts/shortenUrl.php", data=data, headers=headers)
    response.raise_for_status()

    return response.text