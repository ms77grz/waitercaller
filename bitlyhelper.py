from config import TOKEN
import json
import requests

ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper:

    def shorten_url(self, longurl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, longurl)
            response = requests.get(url).json()
            return response["data"]["url"]
        except Exception as e:
            print(e)
