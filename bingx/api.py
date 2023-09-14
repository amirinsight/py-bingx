import hmac
import base64
import json
import urllib.parse
import urllib.request
from utilities import *


class BingxAPI(object):
    ROOT_URL = "https://api-swap-rest.bingbon.pro"
    HEADERS = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self, api_key, secret_key, timestamp="local"):
        self.API_KEY = api_key
        self.SECRET_KEY = secret_key
        self.timestamp = timestamp

    @staticmethod
    def __generate_params(**kwargs):
        body = ""
        if 'params' in kwargs:
            body = kwargs['params'] + "&"
            del kwargs['params']
        body += ''.join(str(kwarg) + "=" + str(kwargs[kwarg]) + "&" for kwarg in kwargs if kwargs[kwarg] != "NULL")[:-1]
        return body

    def __sign(self, method, path, params):
        orig_string = method + path + params
        signature = urllib.parse.quote(base64.b64encode(
            hmac.new(self.SECRET_KEY.encode("utf-8"), orig_string.encode("utf-8"), digestmod="sha256").digest()))
        return signature

    def _post(self, url, body):
        request = urllib.request.Request(url, data=body.encode("utf-8"), headers=self.HEADERS)
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
        path = "/api/v1/common/server/time"
        url = self.ROOT_URL + path
        response = self._post(url, "")
        return str(response["data"]["currentTime"])

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
            # TODO: Turn into exception
            return "INVALID TIMESTAMP WAS INITIATED."

    def get_all_contracts(self):
        path = "/api/v1/market/getAllContracts"
        url = self.ROOT_URL + path
        response = self._get(url, "")
        return response["data"]

    def get_latest_price(self, pair):
        path = "/api/v1/market/getLatestPrice"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        return response["data"]

    def get_latest_trade_price(self, pair):
        path = "/api/v1/market/getLatestPrice"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        return response["data"]["tradePrice"]

    def get_market_depth(self, pair, depth):
        path = "/api/v1/market/getMarketDepth"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair, level=depth)
        response = self._get(url, params)
        return response["data"]

    def get_latest_trade(self, pair):
        path = "/api/v1/market/getMarketTrades"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        return response["data"]

    def get_latest_funding(self, pair):
        path = "/api/v1/market/getLatestFunding"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        return response["data"]

    def get_funding_history(self, pair):
        path = "/api/v1/market/getHistoryFunding"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        return response["data"]

    def get_kline_data(self, pair, interval):
        path = "/api/v1/market/getLatestKline"
        url = self.ROOT_URL + path
        valid_intervals = ['1', '3', '5', '15', '30', '60', '120', '240', '360', '720', '1D', '1W', '1M']
        if str(interval) not in valid_intervals:
            # TODO: Turn into Exception
            return "INVALID INTERVAL. Valid Intervals are: ", str(valid_intervals)

        params = self.__generate_params(symbol=pair, klineType=interval)
        response = self._get(url, params)
        return response["data"]

    def get_kline_history(self, pair, interval, startTimestamp, endTimestamp):
        path = "/api/v1/market/getHistoryKlines"
        url = self.ROOT_URL + path
        valid_intervals = ['1', '3', '5', '15', '30', '60', '120', '240', '360', '720', '1D', '1W', '1M']
        if str(interval) not in valid_intervals:
            # TODO: Turn into Exception
            return "INVALID INTERVAL. Valid Intervals are: ", str(valid_intervals)

        params = self.__generate_params(symbol=pair, klineType=interval, startTs=startTimestamp, endTs=endTimestamp)
        response = self._get(url, params)
        return response["data"]

    def get_open_positions(self, pair):
        """
        Get all the swap positions on a pair. (Not limited to your positions)
        """
        path = "/api/v1/market/getOpenPositions"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        return response["data"]

    def get_tiker(self, pair):
        """
        Get general useful info about the given pair.
        """
        path = "/api/v1/market/getTicker"
        url = self.ROOT_URL + path
        params = self.__generate_params(symbol=pair)
        response = self._get(url, params)
        return response["data"]

    def get_balance(self, currency_symbol):
        path = "/api/v1/user/getBalance"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, currency=currency_symbol,
                                            timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def get_my_perpetual_swap_positions(self, pair):
        path = "/api/v1/user/getPositions"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, currency=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def get_my_positions(self, pair):
        path = "/api/v1/user/getPositions"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, currency=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def place_limit_order(self, pair, position_side, price, volume, action_of_choice, tp="NULL", sl="NULL"):
        # APIKEY must have 'perpetual futures trading' permission for this to work.
        """
                symbol	            String  There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
                apiKey	            String  Interface Key
                timestamp	        String  Timestamp of initiating the request, unit: ms
                side	            String  (Bid(Long)/Ask(Short))
                entrustPrice	    float64 Price
                entrustVolume	    float64 Volume
                action	            String  Open/Close
                Optional Arguments:
                takerProfitPrice	float64	Take Profit Price
                stopLossPrice	    float64	Stop Loss Price
        """
        path = "/api/v1/user/trade"
        url = self.ROOT_URL + path
        valid_ask = ['Ask', 'ask', 'short', 'Short']
        valid_bid = ['Bid', 'bid', 'long', 'Long']
        if position_side in valid_ask:
            position_side = "Ask"
        elif position_side in valid_bid:
            position_side = "Bid"
        else:
            # TODO: Make this and Exception
            return "INVALID PARAMETER FOR POSITION SIDE"
        parameters = self.__generate_params(action=action_of_choice, apiKey=self.API_KEY, entrustPrice=price,
                                            entrustVolume=volume, side=position_side, stopLossPrice=sl, symbol=pair,
                                            takerProfitPrice=tp, timestamp=self.get_timestamp(), tradeType="Limit")
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def place_market_order(self, pair, position_side, volume, action_of_choice, tp="NULL", sl="NULL"):
        # Your APIKEY must have 'perpetual futures trading' permission for this to work.
        # Price is not required for Market orders
        """
                symbol	            String  There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
                apiKey	            String  Interface Key
                timestamp	        String  Timestamp of initiating the request, unit: ms
                side	            String  (Bid(Long)/Ask(Short))
                entrustVolume	    float64 Volume
                action	            String  Open/Close
                Optional Arguments:
                takerProfitPrice	float64	Take Profit Price
                stopLossPrice	    float64	Stop Loss Price
        """
        path = "/api/v1/user/trade"
        url = self.ROOT_URL + path
        valid_ask = ['Ask', 'ask', 'short', 'Short']
        valid_bid = ['Bid', 'bid', 'long', 'Long']
        if position_side in valid_ask:
            position_side = "Ask"
        elif position_side in valid_bid:
            position_side = "Bid"
        else:
            # TODO: Make this and Exception
            return "INVALID PARAMETER FOR POSITION SIDE"
        parameters = self.__generate_params(action=action_of_choice, apiKey=self.API_KEY, entrustPrice="0",
                                            entrustVolume=volume, side=position_side, stopLossPrice=sl, symbol=pair,
                                            takerProfitPrice=tp, timestamp=self.get_timestamp(), tradeType="Market")
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def close_limit_order(self):
        pass

    def close_market_order(self):
        pass

    def close_position(self, pair, position_id):
        """
        Closes given position based on Market price.
        """
        path = "/api/v1/user/oneClickClosePosition"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, positionId=position_id, symbol=pair,
                                            timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def close_all_positions(self):
        """
            Closes any open position based on Market price.
        """
        path = "/api/v1/user/oneClickCloseAllPositions"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def cancel_order(self, pair, order_id):
        """
        Cancel an order that is currently in a unfilled state
        """
        path = "/api/v1/user/cancelOrder"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, orderId=order_id, symbol=pair,
                                            timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def cancel_orders_of_symbol(self, pair):
        path = "/api/v1/user/batchCancelOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def cancel_all_orders(self):
        # TODO: Use **kwargs to cancel multiple order IDs but not all of them
        path = "api/v1/user/cancelAll"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def query_pending_orders(self, pair):
        path = "/api/v1/user/pendingOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def query_order_status(self, pair, order_id):
        """
        Pending	        Order that has not been closed
        PartiallyFilled	Order that has been Partially filled
        Cancelled       Order is canceled
        Filled	        Order is Filled
        Failed	        Order is Failed
        """
        path = "/api/v1/user/queryOrderStatus"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, orderId=order_id, symbol=pair,
                                            timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def get_margin_mode(self, pair):
        path = "/api/v1/user/getMarginMode"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def set_margin_mode(self, pair, mode):
        """
        symbol	    String  There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
        marginMode	String  Isolated or Cross
        In cross margin mode, any position can automatically utilize the available balance of the relevant cryptocurrency to avoid liquidations. If forced liquidation is triggered, users will lose all the available balance. Leverage adjustment will affect all positions of the trading pair.
        In isolated margin mode, a certain amount of margin (initial margin) will be allocated to a position. Users can adjust the margin for the position. If forced liquidation is triggered, the maximum loss incurred is the loss of position margin. Leverage adjustment will affect all positions of the trading pair.
        """
        if mode not in ["Isolated", "Cross"]:
            # TODO: Turn message into exception.
            return "Invalid mode. Mode should be either Isolated or Cross"
        path = "/api/v1/user/setMarginMode"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, marginMode=mode, symbol=pair,
                                            timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def get_levarage(self, pair):
        path = "/api/v1/user/getLeverage"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def set_levarage(self, pair, position_side, amount):
        """
        :return: Nothing {} if the request is successful and code:0
        """
        path = "/api/v1/user/setLeverage"
        url = self.ROOT_URL + path
        valid_ask = ['Ask', 'ask', 'short', 'Short']
        valid_bid = ['Bid', 'bid', 'long', 'Long']
        if position_side in valid_ask:
            position_side = "Ask"
        elif position_side in valid_bid:
            position_side = "Bid"
        else:
            # TODO: Make this and Exception
            return "INVALID PARAMETER FOR POSITION SIDE"
        parameters = self.__generate_params(apiKey=self.API_KEY, levarage=amount, side=position_side, symbol=pair,
                                            timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def query_force_orders(self, pair, auto_close_type, last_order_id, length_per_request="100"):
        """
        symbol	        String 	There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT
        autoCloseType	String	"LIQUIDATION" for liquidation orders, "ADL" for ADL orders.
        lastOrderId	    int64 	Used for paging, fill in 0 for the first time; for subsequent requests, fill in the last order id from the previous return results.
        length	        int64 	Length per request, max 100
        """
        path = "/api/v1/user/forceOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(autoCloseType=auto_close_type, lastOrderId=last_order_id,
                                            length=length_per_request, symbol=pair)
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def query_history_orders(self, last_order_id, pair="NULL", length_per_request="100"):
        path = "/api/v1/user/historyOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, lastOrderId=last_order_id, length=length_per_request,
                                            symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def place_stop_order(self, pair, volume, position_id, order_id="NULL", tp="NULL", sl="NULL"):
        """
        Stop-loss orders should be in place whenever you have an open position to limit your potential losses.
        Stop-entry orders can be used to enter the market in the direction the market is moving, frequently referred to as breakout trading.
        If the market is moving higher, a stop-entry order will make you long; if the market is moving lower, a stop-entry will make you short.
        """
        # APIKEY must have 'perpetual futures trading' permission for this to work.
        path = "/api/v1/user/stopOrder"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, entrustVolume=volume, orderId=order_id,
                                            positionId=position_id, stopLossPrice=sl, symbol=pair, takeProfitPrice=tp,
                                            timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def cancel_stop_order(self, pair, order_id):
        """
        Cancel an order that is currently in a unfilled state
        """
        path = "/api/v1/user/cancelStopOrder"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, orderId=order_id, symbol=pair,
                                            timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        # data = response["data"]
        return response

    def query_pending_stop_orders(self, pair):
        path = "/api/v1/user/pendingStopOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data

    def query_history_stop_orders(self, pair, last_order_id, length_per_request="100"):
        path = "/api/v1/user/historyStopOrders"
        url = self.ROOT_URL + path
        parameters = self.__generate_params(apiKey=self.API_KEY, lastOrderId=last_order_id, length=length_per_request,
                                            symbol=pair, timestamp=self.get_timestamp())
        body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
        response = self._post(url, body)
        data = response["data"]
        return data
