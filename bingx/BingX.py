import time
import hmac
import base64
import json
import urllib.parse
import urllib.request
import requests
from Secret import API_KEY, SECRET_KEY

ROOT_URL = "https://api-swap-rest.bingbon.pro"


def create_body(METHOD, PATH, CURRENCY=""):
    TIME_STAMP = str(int(time.time() * 1000))
    ORIG_STRING = METHOD + PATH + "apiKey=" + API_KEY + "&currency=" + CURRENCY + "&timestamp=" + TIME_STAMP
    SIGNATURE = urllib.parse.quote(base64.b64encode(
        hmac.new(SECRET_KEY.encode("utf-8"), ORIG_STRING.encode("utf-8"), digestmod="sha256").digest()))
    body = "apiKey=" + API_KEY + "&currency=" + CURRENCY + "&timestamp=" + TIME_STAMP + "&sign=" + SIGNATURE
    return body


def urllib_post(url, body, response_type="json"):
    full_url = ROOT_URL + url
    request = urllib.request.Request(full_url, data=body.encode("utf-8"), headers={'User-Agent': 'Mozilla/5.0'})
    print("url: ", full_url)
    print("body: ", body)
    response = urllib.request.urlopen(request).read()
    json_object = json.loads(response.decode('utf8'))
    if response_type == "json":
        return json_object
    elif response_type == "byte":
        return response
    if response_type != "json" or "byte":
        raise RuntimeError("Invalid response type: ", response_type)


def get_server_time():
    response = urllib_post("/api/v1/common/server/time", "", response_type="json")
    return response["data"]["currentTime"]


def get_balance(currency):
    response = urllib_post("/api/v1/user/getBalance", create_body("POST", "/api/v1/user/getBalance", CURRENCY=currency))
    balance = response["data"]["account"]["balance"]
    return balance


def get_latest_trade_price(pair):
    full_url = "https://api-swap-rest.bingbon.pro/api/v1/market/getLatestPrice"
    response = requests.get(full_url, "symbol=" + pair)
    return response.json()["data"]["tradePrice"]
