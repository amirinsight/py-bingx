# {'code': 80014, 'msg': 'client apiKey.GetSign: apiKey has no permission', 'data': {}}
# {'code': 80014, 'msg': 'signature not match', 'data': {}}
# {'code': 80014, 'msg': 'Insufficient margin, please adjust and resubmit', 'data': {}} # TODO: return mgs if code is not 0.
# {'code': 80012, 'msg': 'the account has positions or pending orders', 'data': {}}
# {'code': 80014, 'msg': 'Take Profit price should be lower than trigger price', 'data': {}} in Short trades
# {'code': 80014, 'msg': 'Insufficient position, please adjust and resubmit', 'data': {}} place_market_order("ALGO-USDT", "Short", 5, "Close")
# {'code': 80014, 'msg': 'Invalid parameters, err:strconv.ParseFloat: parsing "None": invalid syntax', 'data': {}}
"""def place_market_order(self, pair, position_side, volume, action_of_choice, tp=" ", sl=" "):
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
                                        entrustVolume=volume, side=position_side, symbol=pair,
                                        timestamp=self.get_timestamp(), takerProfitPrice=tp, tradeType="Market",
                                        stopLossPrice=sl)
    body = self.__generate_params(params=parameters, sign=self.__sign("POST", path, parameters))
    response = self._post(url, body)
    # data = response["data"]
    return response
"""
