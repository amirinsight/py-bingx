import hmac
import base64
import json
import urllib.parse
import urllib.request

from .utilities import get_system_time


class BingxAPI(object):
    ROOT_URL = "https://open-api.bingx.com"
    DEMO_URL = "https://open-api-vst.bingx.com"

    def __init__(self, api_key, secret_key,demo=False, timestamp="local"):
        self.API_KEY = api_key
        self.SECRET_KEY = secret_key
        self.timestamp = timestamp
        if demo:
            self.ROOT_URL = self.DEMO_URL
        self.HEADERS = {'User-Agent': 'Mozilla/5.0',
                        'X-BX-APIKEY': self.API_KEY}

    @staticmethod
    def __generate_params(**kwargs):
        params = ""
        if 'params' in kwargs:
            params = kwargs['params'] + "&"
            del kwargs['params']
        params += ''.join(str(kwarg) + "=" + str(kwargs[kwarg]) + "&" for kwarg in kwargs if kwargs[kwarg] != "NULL")[
                  :-1]
        return params

    @staticmethod
    def __jasonify(**kwargs):
        filtered_kwargs = {k: v for k, v in kwargs.items() if v != "NULL"}
        return json.dumps(filtered_kwargs)

    def __sign(self, method, path, params):
        orig_string = method + path + params
        signature = urllib.parse.quote(base64.b64encode(
            hmac.new(self.SECRET_KEY.encode("utf-8"), orig_string.encode("utf-8"), digestmod="sha256").digest()))
        return signature

    def __sign_hex(self, params):
        digest = hmac.new(self.SECRET_KEY.encode("utf-8"), params.encode("utf-8"), digestmod="sha256").digest()
        return digest.hex()

    def _post(self, url, body):
        request = urllib.request.Request(url, data=body.encode("utf-8"), headers=self.HEADERS, method="POST")
        response = urllib.request.urlopen(request).read()
        json_object = json.loads(response.decode('utf8'))
        return json_object

    def _delete(self, url, params):
        if params != "":
            url = url + "?" + params
        request = urllib.request.Request(url, headers=self.HEADERS, method="DELETE")
        response = urllib.request.urlopen(request).read()
        json_object = json.loads(response.decode('utf8'))
        return json_object

    def _get(self, url, params):
        if params != "":
            url = url + "?" + params
        request = urllib.request.Request(url, headers=self.HEADERS)
        response = urllib.request.urlopen(request).read()
        json_object = json.loads(response.decode('utf8'))
        return json_object

    def __get_server_time(self):
        path = "/openApi/swap/v2/server/time"
        url = self.ROOT_URL + path
        response = self._post(url, "")
        if "data" in response and "serverTime" in response["data"]:
            return str(response["data"]["serverTime"])
        else:
            return {"error":True,"response":response}

    @staticmethod
    def __handle_response(response):
        if response["code"] != 0:
            return response["msg"]
        else:
            return response["data"]

    def get_timestamp(self):
        if self.timestamp == "local":
            return get_system_time()
        elif self.timestamp == "server":
            return self.__get_server_time()
        else:
            raise ValueError("[!] INVALID VALUE FOR TIMESTAMP WAS INITIATED.")

    def get_all_contracts(self):
        path = "/openApi/swap/v2/quote/contracts"
        url = self.ROOT_URL + path
        response = self._get(url, "")
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def get_latest_price(self, pair):
        path = "/openApi/swap/v2/quote/price"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        if "data" in response and "price" in response["data"]:
            return response["data"]["price"]
        else:
            return {"error":True,"response":response}

    def get_market_depth(self, pair, limit="NULL"):
        path = "/openApi/swap/v2/quote/depth"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair, limit=limit)
        response = self._get(url, params)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def get_latest_trade(self, pair):
        path = "/openApi/swap/v2/quote/trades"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def get_latest_funding(self, pair):
        path = "/openApi/swap/v2/quote/premiumIndex"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        if "data" in response and "lastFundingRate" in response["data"]:
            return response["data"]["lastFundingRate"]
        else:
            return {"error":True,"response":response}

    def get_index_price(self, pair):
        path = "/openApi/swap/v2/quote/premiumIndex"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        if "data" in response and "indexPrice" in response["data"]:
            return response["data"]["indexPrice"]
        else:
            return {"error":True,"response":response}

    def get_market_price(self, pair):
        path = "/openApi/swap/v2/quote/premiumIndex"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        if "data" in response and "markPrice" in response["data"]:
            return response["data"]["markPrice"]
        else:
            return {"error":True,"response":response}

    def get_funding_history(self, pair):
        path = "/openApi/swap/v2/quote/fundingRate"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def get_kline_data(self, pair, interval, start_timestamp="NULL", end_timestamp="NULL", limit="NULL"):
        """
        Gives 500 candles if start and end times are not given.
        Timestamps are in epoch time.
        :param pair:
        :param interval:
        :param start_timestamp:
        :param end_timestamp:
        :param limit: Set a candle limit. Default is 500 and Max is 1440,
        :return:
        """

        path = "/openApi/swap/v3/quote/klines"
        url = self.ROOT_URL + path
        VALID_INTERVALS = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
        if str(interval) not in VALID_INTERVALS:
            raise ValueError("[!] INVALID INTERVAL VALUE. Valid Intervals are: ", str(VALID_INTERVALS))

        params = self.__generate_params(symbol=pair, interval=interval, startTime=start_timestamp,
                                        endTime=end_timestamp, limit=limit)
        response = self._get(url, params)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def get_open_positions(self, pair):
        """
        Get all the swap positions on a pair. (Not limited to your positions)
        """
        path = "/openApi/swap/v2/quote/openInterest"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def get_tiker(self, pair):
        """
        Get general useful info about the given pair.
        """
        path = "/openApi/swap/v2/quote/ticker"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def get_current_optimal_price(self, pair):
        """
        Obtain the current optimal order(Best bid and offer)
        # Use best bid to sell and use best offer to buy.
        """
        path = "/openApi/swap/v2/quote/bookTicker"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._get(url, body)
        best_bid = response["data"]["book_ticker"]["bid_price"]
        best_offer = response["data"]["book_ticker"]["ask_price"]
        return [best_offer, best_bid]

    def get_perpetual_balance(self):
        """
        Get asset information of user‘s Perpetual Account
        """
        path = "/openApi/swap/v2/user/balance"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._get(url, body)
        # data = response["data"]
        return response

    def get_my_perpetual_swap_positions(self, pair="NULL"):
        path = "/openApi/swap/v2/user/positions"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(currency=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._get(url, body)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def get_capital_flow(self):
        # To be implemented
        path = "/openApi/swap/v2/user/income"
        url = self.ROOT_URL + path
        raise NotImplementedError

    def export_fund_flow(self):
        # To be implemented
        path = "/openApi/swap/v2/user/income/export"
        url = self.ROOT_URL + path
        raise NotImplementedError

    def get_fee_rate(self):
        path = "/openApi/swap/v2/user/commissionRate"
        url = self.ROOT_URL + path
        response = self._get(url, "")
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    # Market Orders:

    def open_market_order(self, pair, position_side, volume, sl="NULL", tp="NULL", client_order_id="NULL"):
        """
        APIKEY must have 'perpetual futures trading' permission for this to work.

        :param pair: Symbol you want to trade i.e. BTC-USDT
        :param position_side: LONG/SHORT
        :param volume: Amount of trade for this position
        :param client_order_id: Your choosen order id (a unique number between 1 and 40)
        :param tp: Take profit for this position. You should set or use the default values for the following:
            type        TAKE_PROFIT_MARKET/TAKE_PROFIT
            quantity    Order quantity, contract quantity, currently only supports contract quantity in terms of currency, does not support inputting U$:quantity=U$/price
            stopPrice   Trigger price (Activate tp when the price hits this value)
            price       Order price
            workingType Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE
        :param sl: Stop loss for this position. You should set or use the default values for the following:
            type        STOP_MARKET/STOP
            quantity    Order quantity, contract quantity, currently only supports contract quantity in terms of currency, does not support inputting U$:quantity=U$/price
            stopPrice   Trigger price
            price       Order price
            workingType Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE
        :return: Order details
        """
        path = "/openApi/swap/v2/trade/order"
        url = self.ROOT_URL + path
        if position_side == "LONG":
            desicion = "BUY"
        elif position_side == "SHORT":
            desicion = "SELL"
        else:
            raise ValueError("position_side must be either 'SHORT' or 'LONG'")
        if tp != "NULL":
            tp = "{" + f'"type": "TAKE_PROFIT_MARKET", "quantity": {volume},"stopPrice": {tp},"price": {tp},"workingType":"MARK_PRICE"' + "}"
        if sl != "NULL":
            sl = "{" + f'"type": "TAKE_PROFIT_MARKET", "quantity": {volume},"stopPrice": {sl},"price": {sl},"workingType":"MARK_PRICE"' + "}"
        parameters = self.__generate_params(clientOrderID=client_order_id, positionSide=position_side, quantity=volume,
                                            side=desicion, symbol=pair, type="MARKET", takeProfit=tp, stopLoss=sl,
                                            timestamp=self.get_timestamp(), recvWindow="10000")
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        if "data" in response and "order" in response["data"]:
            return response["data"]["order"]
        else:
            return {"error":True,"response":response}

    def close_market_order(self, pair, position_side, volume, client_order_id="NULL"):
        """
        APIKEY must have 'perpetual futures trading' permission for this to work.

        :param pair: Symbol you want to trade i.e. BTC-USDT
        :param position_side: LONG/SHORT
        :param volume: Amount of trade for this position
        :param client_order_id: Your choosen order id (a unique number between 1 and 40)
        :return: Order details
        """
        path = "/openApi/swap/v2/trade/order"
        url = self.ROOT_URL + path
        if position_side == "LONG":
            desicion = "SELL"
        elif position_side == "SHORT":
            desicion = "BUY"
        else:
            raise ValueError("position_side must be either 'SHORT' or 'LONG'")
        parameters = self.__generate_params(clientOrderID=client_order_id, symbol=pair, type="MARKET", side=desicion,
                                            positionSide=position_side, quantity=volume, timestamp=self.get_timestamp(),
                                            recvWindow="10000")
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def place_trigger_market_order(self, pair, desicion, position_side, trigger_price, volume,
                                   trigger_price_type="NULL", client_order_id="NULL", time_in_force="NULL", tp="NULL",
                                   sl="NULL"):
        """
        APIKEY must have 'perpetual futures trading' permission for this to work.

        :param pair: Symbol you want to trade i.e. BTC-USDT
        :param desicion: SELL/BUY
        :param position_side: LONG/SHORT
        :param volume: Amount of trade for this position
        :param trigger_price: Stop price for this position
        :param client_order_id: Your choosen order id (a unique number between 1 and 40)
        :param trigger_price_type: StopPrice trigger price types: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default MARK_PRICE
        :param time_in_force: PostOnly(Cancel if it can be filled immediately), GTC(Execute or manually cancel), IOC(Cancel any part that's not immediately filled), and FOK(Fill or Kill)
        :param tp: Take profit for this position. You should set or use the default values for the following:
            type        TAKE_PROFIT_MARKET/TAKE_PROFIT
            quantity    Order quantity, contract quantity, currently only supports contract quantity in terms of currency, does not support inputting U$:quantity=U$/price
            stopPrice   Trigger price (Activate tp when the price hits this value)
            price       Order price
            workingType Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE
        :param sl: Stop loss for this position. You should set or use the default values for the following:
            type        STOP_MARKET/STOP
            quantity    Order quantity, contract quantity, currently only supports contract quantity in terms of currency, does not support inputting U$:quantity=U$/price
            stopPrice   Trigger price
            price       Order price
            workingType Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE
        :return: Order details
        """
        path = "/openApi/swap/v2/trade/order"
        url = self.ROOT_URL + path
        if tp != "NULL":
            tp = "{" + f'"type": "TAKE_PROFIT_MARKET", "quantity": {volume},"stopPrice": {tp},"price": {tp},"workingType":"MARK_PRICE"' + "}"
        if sl != "NULL":
            sl = "{" + f'"type": "TAKE_PROFIT_MARKET", "quantity": {volume},"stopPrice": {sl},"price": {sl},"workingType":"MARK_PRICE"' + "}"
        parameters = self.__generate_params(symbol=pair, type="TRIGGER_MARKET", side=desicion,
                                            positionSide=position_side, quantity=volume, stopPrice=trigger_price,
                                            workingType=trigger_price_type, takeProfit=tp, stopLoss=sl,
                                            timestamp=self.get_timestamp(), clientOrderID=client_order_id,
                                            timeInForce=time_in_force, recvWindow="10000")
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    # Limit Orders:

    def open_limit_order(self, pair, position_side, price, volume, sl="NULL", tp="NULL", client_order_id="NULL"):
        """
        APIKEY must have 'perpetual futures trading' permission for this to work.

        :param pair: Symbol you want to trade i.e. BTC-USDT
        :param position_side: LONG/SHORT
        :param price: Entry price for this position. Can be set to "BBO" to use the best bid and offer.
        :param volume: Amount of trade for this position
        :param client_order_id: Your choosen order id (a unique number between 1 and 40)
        :param tp: Take profit for this position. You should set or use the default values for the following:
            type        TAKE_PROFIT_MARKET/TAKE_PROFIT
            quantity    Order quantity, contract quantity, currently only supports contract quantity in terms of currency, does not support inputting U$:quantity=U$/price
            stopPrice   Trigger price (Activate tp when the price hits this value)
            price       Order price
            workingType Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE
        :param sl: Stop loss for this position. You should set or use the default values for the following:
            type        STOP_MARKET/STOP
            quantity    Order quantity, contract quantity, currently only supports contract quantity in terms of currency, does not support inputting U$:quantity=U$/price
            stopPrice   Trigger price
            price       Order price
            workingType Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE
        :return: Order details
        """
        path = "/openApi/swap/v2/trade/order"
        url = self.ROOT_URL + path
        if position_side == "LONG":
            desicion = "BUY"
        elif position_side == "SHORT":
            desicion = "SELL"
        else:
            raise ValueError("position_side must be either 'SHORT' or 'LONG'")
        if price == "BBO" and desicion == "BUY":
            price = self.get_current_optimal_price(pair)[0]
        if price == "BBO" and desicion == "SELL":
            price = self.get_current_optimal_price(pair)[1]

        if tp != "NULL":
            tp = "{" + f'"type": "TAKE_PROFIT_MARKET", "quantity": {volume},"stopPrice": {tp},"price": {tp},"workingType":"MARK_PRICE"' + "}"
        if sl != "NULL":
            sl = "{" + f'"type": "TAKE_PROFIT_MARKET", "quantity": {volume},"stopPrice": {sl},"price": {sl},"workingType":"MARK_PRICE"' + "}"
        parameters = self.__generate_params(clientOrderID=client_order_id, positionSide=position_side, quantity=volume,
                                            price=price, side=desicion, symbol=pair, type="LIMIT", takeProfit=tp,
                                            stopLoss=sl,
                                            timestamp=self.get_timestamp(), recvWindow="10000")
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        if "data" in response and "order" in response["data"]:
            return response["data"]["order"]
        else:
            return {"error":True,"response":response}

    def close_limit_order(self, pair, position_side, price, volume, client_order_id="NULL"):
        """
        APIKEY must have 'perpetual futures trading' permission for this to work.

        :param pair: Symbol you want to trade i.e. BTC-USDT
        :param position_side: LONG/SHORT
        :param price: Entry price for this position. Can be set to "BBO" to use the best bid and offer.
        :param volume: Amount of trade for this position
        :param client_order_id: Your choosen order id (a unique number between 1 and 40)
        :return: Order details
        """
        path = "/openApi/swap/v2/trade/order"
        url = self.ROOT_URL + path
        if position_side == "LONG":
            desicion = "SELL"
        elif position_side == "SHORT":
            desicion = "BUY"
        else:
            raise ValueError("position_side must be either 'SHORT' or 'LONG'")
        if price == "BBO" and desicion == "BUY":
            price = self.get_current_optimal_price(pair)[0]
        if price == "BBO" and desicion == "SELL":
            price = self.get_current_optimal_price(pair)[1]
        parameters = self.__generate_params(clientOrderID=client_order_id, symbol=pair, type="LIMIT", side=desicion,
                                            positionSide=position_side, price=price, quantity=volume,
                                            timestamp=self.get_timestamp(), recvWindow="10000")
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def place_trigger_limit_order(self, pair, desicion, position_side, price, volume, trigger_price,
                                  trigger_price_type="NULL", client_order_id="NULL", time_in_force="NULL", tp="NULL",
                                  sl="NULL"):
        """
        APIKEY must have 'perpetual futures trading' permission for this to work.

        :param pair: Symbol you want to trade i.e. BTC-USDT
        :param desicion: SELL/BUY
        :param position_side: LONG/SHORT
        :param price: Entry price for this position
        :param volume: Amount of trade for this position
        :param trigger_price: Stop price for this position
        :param sl: Stop loss for this position
        :param tp: Take profit for this position
        :param client_order_id: Your choosen order id (a unique number between 1 and 40)
        :param trigger_price_type: StopPrice trigger price types: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default MARK_PRICE
        :param time_in_force: PostOnly(Cancel if it can be filled immediately), GTC(Execute or manually cancel), IOC(Cancel any part that's not immediately filled), and FOK(Fill or Kill)
        :param tp: Take profit for this position. You should set or use the default values for the following:
            type        TAKE_PROFIT_MARKET/TAKE_PROFIT
            quantity    Order quantity, contract quantity, currently only supports contract quantity in terms of currency, does not support inputting U$:quantity=U$/price
            stopPrice   Trigger price (Activate tp when the price hits this value)
            price       Order price
            workingType Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE
        :param sl: Stop loss for this position. You should set or use the default values for the following:
            type        STOP_MARKET/STOP
            quantity    Order quantity, contract quantity, currently only supports contract quantity in terms of currency, does not support inputting U$:quantity=U$/price
            stopPrice   Trigger price
            price       Order price
            workingType Trigger price type for stopPrice: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default is MARK_PRICE
        :return: Order details
        """
        path = "/openApi/swap/v2/trade/order"
        url = self.ROOT_URL + path
        if tp != "NULL":
            tp = "{" + f'"type": "TAKE_PROFIT_MARKET", "quantity": {volume},"stopPrice": {tp},"price": {tp},"workingType":"MARK_PRICE"' + "}"
        if sl != "NULL":
            sl = "{" + f'"type": "TAKE_PROFIT_MARKET", "quantity": {volume},"stopPrice": {sl},"price": {sl},"workingType":"MARK_PRICE"' + "}"
        parameters = self.__generate_params(symbol=pair, type="TRIGGER_LIMIT", side=desicion,
                                            positionSide=position_side, price=price, quantity=volume,
                                            stopPrice=trigger_price, takeProfit=tp, stopLoss=sl,
                                            workingType=trigger_price_type, timestamp=self.get_timestamp(),
                                            clientOrderID=client_order_id, timeInForce=time_in_force,
                                            recvWindow="10000")
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def place_trailing_stop_order(self, pair, desicion, position_side, volume, price="NULL", price_rate="NULL",
                                  client_order_id="NULL", time_in_force="NULL"):
        """
        APIKEY must have 'perpetual futures trading' permission for this to work.

        :param pair: Symbol you want to trade i.e. BTC-USDT
        :param desicion: SELL/BUY
        :param position_side: LONG/SHORT
        :param volume: Amount of trade for this position
        :param price: Entry price for this position.
        :param price_rate: Price rate Maximum: 1
        :param client_order_id: Your choosen order id (a unique number between 1 and 40)
        :param time_in_force: PostOnly(Cancel if it can be filled immediately), GTC(Execute or manually cancel), IOC(Cancel any part that's not immediately filled), and FOK(Fill or Kill)
        :return: Order details
        """
        path = "/openApi/swap/v2/trade/order"
        url = self.ROOT_URL + path
        if price == "NULL" and price_rate == "NULL":
            raise ValueError("[!] EITHER PRICE OR PRICE_RATE MUST BE SET.")
        parameters = self.__generate_params(symbol=pair, type="TRAILING_STOP_MARKET", side=desicion,
                                            positionSide=position_side, quantity=volume, price=price,
                                            priceRate=price_rate,
                                            timestamp=self.get_timestamp(), clientOrderID=client_order_id,
                                            timeInForce=time_in_force, recvWindow="10000")
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def place_test_order(self, trade_type, pair, desicion, position_side, price, volume, stop_price, priceRate, sl, tp,
                         working_type, client_order_id, time_in_force):
        """
        APIKEY must have 'perpetual futures trading' permission for this to work.
        The participation and return are consistent with the ordering interface, but the actual order will not be placed
        , only the test results will be returned.The result is a fake order, and your funds will not be deducted.
        It will not appear on the real transaction panel and is only used to help you practice using the order interface

        :param trade_type: LIMIT, MARKET, TRIGGER_LIMIT, TRIGGER_MARKET
        :param pair: Symbol you want to trade i.e. BTC-USDT
        :param desicion: SELL/BUY
        :param position_side: LONG/SHORT
        :param price: Entry price for this position
        :param volume: Amount of trade for this position
        :param stop_price: Stop price for this position
        :param priceRate: Price rate Maximum: 1
        :param sl: Stop loss for this position
        :param tp: Take profit for this position
        :param client_order_id: Your choosen order id (a unique number between 1 and 40)
        :param working_type: StopPrice trigger price types: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, default MARK_PRICE
        :param time_in_force: PostOnly(Cancel if it can be filled immediately), GTC(Execute or manually cancel), IOC(Cancel any part that's not immediately filled), and FOK(Fill or Kill)
        :return: Order details
        """
        path = "/openApi/swap/v2/trade/order/test"
        url = self.ROOT_URL + path
        if tp != "NULL":
            tp = "{" + f'"type": "TAKE_PROFIT_MARKET", "quantity": {volume},"stopPrice": {tp},"price": {tp},"workingType":"MARK_PRICE"' + "}"
        if sl != "NULL":
            sl = "{" + f'"type": "TAKE_PROFIT_MARKET", "quantity": {volume},"stopPrice": {sl},"price": {sl},"workingType":"MARK_PRICE"' + "}"
        parameters = self.__generate_params(symbol=pair, type=trade_type, side=desicion, positionSide=position_side,
                                            price=price, quantity=volume, stopPrice=stop_price, price_rate=priceRate,
                                            stopLoss=sl, takeProfit=tp, workingType=working_type,
                                            timestamp=self.get_timestamp(), clientOrderID=client_order_id,
                                            timeInForce=time_in_force)
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def place_bulk_order(self):
        # To be implemented
        path = "/openApi/swap/v2/trade/batchOrders"
        url = self.ROOT_URL + path
        raise NotImplementedError

    def close_all_positions(self):
        """
            Closes any open position based on Market price.
        """
        path = "/openApi/swap/v2/trade/closeAllPositions"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(timestamp=self.get_timestamp(), recvWindow="10000")
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def cancel_order(self, pair, order_id="NULL", client_order_id="NULL"):
        """
        Cancel an order that is currently in an unfilled state
        """
        path = "/openApi/swap/v2/trade/order"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(orderId=order_id, symbol=pair, clientOrderID=client_order_id,
                                            timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._get(url, body)
        # data = response["data"]
        return response

    def cancel_all_orders_of_symbol(self, pair):
        path = "/openApi/swap/v2/trade/allOpenOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._delete(url, body)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def cancel_batch_orders(self, pair, orderid_list="NULL", client_orderID_list="NULL"):
        """
        orderIdList              LIST < int64 >      order number up to 10 orders in a list [1234567, 2345678]
        ClientOrderIDList        LIST < string >     Customized order ID for users, up to 10 orders[1234567, 2345678]
        """
        path = "/openApi/swap/v2/trade/batchOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(ClientOrderIDList=client_orderID_list, orderIdList=orderid_list,
                                            symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._delete(url, body)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def query_pending_orders(self, pair="NULL"):
        path = "/openApi/swap/v2/trade/openOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._get(url, body)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def query_order(self, pair, order_id="NULL", client_order_id="NULL"):
        """
        Pending	        Order that has not been closed
        PartiallyFilled	Order that has been Partially filled
        Cancelled       Order is canceled
        Filled	        Order is Filled
        Failed	        Order is Failed
        """
        path = "/openApi/swap/v2/trade/order"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(clientOrderID=client_order_id, orderId=order_id, symbol=pair,
                                            timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._get(url, body)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def get_margin_mode(self, pair):
        path = "/openApi/swap/v2/trade/marginType"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._get(url, body)
        if "data" in response and "marginType" in response["data"]:
            return response["data"]["marginType"]
        else:
            return {"error":True,"response":response}

    def set_margin_mode(self, pair, mode):
        """
        symbol	    String  There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
        marginType	String  ISOLATED or CROSSED
        In cross margin mode, any position can automatically utilize the available balance of the relevant cryptocurrency to avoid liquidations. If forced liquidation is triggered, users will lose all the available balance. Leverage adjustment will affect all positions of the trading pair.
        In isolated margin mode, a certain amount of margin (initial margin) will be allocated to a position. Users can adjust the margin for the position. If forced liquidation is triggered, the maximum loss incurred is the loss of position margin. Leverage adjustment will affect all positions of the trading pair.
        """
        if mode not in ["ISOLATED", "CROSSED"]:
            raise ValueError("[!] INVALID VALUE FOR MODE. Mode should be either ISOLATED or CROSSED")
        path = "/openApi/swap/v2/trade/marginType"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(marginType=mode, symbol=pair,
                                            timestamp=self.get_timestamp(), recvWindow="10000")
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        if response["code"] == '0':
            return f"Margin mode for {pair} was set to {mode}."

    def get_levarage(self, pair):
        path = "/openApi/swap/v2/trade/leverage"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._get(url, body)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def set_levarage(self, pair, position_side, amount):
        path = "/openApi/swap/v2/trade/leverage"
        url = self.ROOT_URL + path
        valid_ask = ['ASK', 'Ask', 'ask', 'short', 'Short', 'SHORT']
        valid_bid = ['BID', 'Bid', 'bid', 'long', 'Long', 'LONG']
        if position_side in valid_ask:
            position_side = "SHORT"
        elif position_side in valid_bid:
            position_side = "LONG"
        else:
            raise ValueError("[!] INVALID VALUE FOR POSITION SIDE")
        parameters = self.__generate_params(leverage=amount, side=position_side, symbol=pair,
                                            timestamp=self.get_timestamp(), recvWindow="10000")
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._post(url, body)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def query_force_orders(self, pair, auto_close_type="NULL", start_timestamp="NULL", end_timestamp="NULL",
                           limit="NULL"):
        """
        symbol	        String 	There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
        autoCloseType	String	"LIQUIDATION" for liquidation orders, "ADL" for ADL orders.

        If "autoCloseType" is not passed, both forced liquidation orders and ADL liquidation orders will be returned
        If "startTime" is not passed, only the data within 7 days before "endTime" will be returned
        """
        path = "/openApi/swap/v2/trade/forceOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(autoCloseType=auto_close_type, endTime=end_timestamp, limit=limit,
                                            startTime=start_timestamp, symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._get(url, body)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def query_orders_history(self, pair, limit=500, order_id="NULL", start_timestamp="NULL", end_timestamp="NULL"):
        # The maximum query time range shall not exceed 7 days
        # Query data within the last 7 days by default
        # limit is: number of result sets to return //Default: 500 //Maximum: 1000
        path = "/openApi/swap/v2/trade/allOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(endTime=end_timestamp, limit=limit, orderId=order_id,
                                            startTime=start_timestamp, symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, signature=self.__sign_hex(parameters))
        response = self._get(url, body)
        if "data" in response:
            return response["data"]
        else:
            return {"error":True,"response":response}

    def query_transactional_order_history(self):
        # To be implemented
        path = "/openApi/swap/v2/trade/allFillOrders"
        url = self.ROOT_URL + path
        raise NotImplementedError

    def adjust_isolated_margin(self):
        # To be implemented
        path = "/openApi/swap/v2/trade/positionMargin"
        url = self.ROOT_URL + path
        raise NotImplementedError
