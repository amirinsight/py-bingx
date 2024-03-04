==================
This is py-bingx-d
==================

Updated 4 March 2024 ⏰

.. image:: https://img.shields.io/pypi/v/py-bingx.svg
    :target: https://pypi.python.org/pypi/py-bingx

.. image:: https://img.shields.io/pypi/l/py-bingx.svg 
    :target: https://pypi.python.org/pypi/py-bingx

.. image:: https://img.shields.io/github/stars/amirinsight/py-bingx.svg?style=social&label=Stars 
   :target: https://github.com/amirinsight/py-bingx
   :alt: Star This Project


py-bingx-d is developed (`py-bingx package <https://github.com/amirinsight/py-bingx>`_) an unofficial Python wrapper for the `BingX Perpetual Swap API <https://bingx-api.github.io/docs/swap/introduce.html>`_. You can use this package to create trading bots. Make sure to read my `disclaimer <https://github.com/rikhtehgaran/py-bingx#disclaimer>`_ and consider starring this project.

Usage
-----

Register an account on `BingX <https://bingx.com/en-us/register>`_. 

`Create an API <https://bingx.com/en-us/account/api>`_
and make sure you copy your Secret Key before leaving the page. 🗝

.. code:: bash

    pip install py-bingx-d

.. code:: python

    from bingx.api import BingxAPI 

    ...

    # Please note that it is smarter to use environment variables than hard coding your keys into your code.
    API_KEY = '<api_public_key>' 
    SECRET_KEY = '<api_secret_key>'

    # It is faster and more efficient to use local timestamps. If you are getting an error try using "server" timestamp.
    bingx = BingxAPI(API_KEY, SECRET_KEY, demo=False, timestamp="local") # For use VST demo account set demo to True
    order_data = bingx.open_market_order('BTC-USDT', 'LONG', 0.01, tp="63277", sl="60658")

Functions 🧰
------------

py-bingx was written with the goal of being user-friendly. Feel free to ask your questions and state any bugs/issues with the code.

You can find the list of py-bingx functions below: 

Market Data Functions 💹
------------------------

- ``get_all_contracts()`` - Gets a list of all contracts/trading pairs available on Bingx 
- ``get_latest_price(pair)`` - Gets the latest price for a trading pair 💱
- ``get_market_depth(pair, limit)`` - Gets the order book depth data for a trading pair 📊
- ``get_latest_trade(pair)`` - Gets recent trades for a trading pair 💸
- ``get_latest_funding(pair)`` - Gets latest funding rate for a trading pair 💵
- ``get_index_price(pair)`` - Gets index price for a trading pair 📈
- ``get_market_price(pair)`` - Gets market price for a trading pair 📉
- ``get_funding_history(pair)`` - Gets historical funding rate data for a trading pair 📜
- ``get_kline_data(pair, interval, start_time, end_time, limit)`` - Gets candlestick/kline data for a trading pair 🕯
- ``get_open_positions(pair)`` - Gets open interest data for a trading pair 👀
- ``get_tiker(pair)`` - Gets ticker data including 24hr prices and volumes 📣
- ``get_current_optimal_price(pair)`` - Gets best bid and offer prices for a trading pair 💰

Account Data Functions  👤
--------------------------

- ``get_perpetual_balance()`` - Get user account balance info 💳
- ``get_my_perpetual_swap_positions(pair)`` - Get user open positions for a trading pair 📈
- ``get_fee_rate()`` - Get fee rate for trading 💸

Trading Functions 📈
--------------------

- ``open_market_order()`` - Opens a market order to buy/sell a trading pair 💹
- ``close_market_order()`` - Closes an open market order ❌
- ``place_trigger_market_order()`` - Places a stop-trigger market order ⏱
- ``open_limit_order()`` - Opens a limit order for a trading pair 🎯
- ``close_limit_order()`` - Closes an open limit order ❌
- ``place_trigger_limit_order()`` - Places a stop-trigger limit order ⏱
- ``place_trailing_stop_order()`` - Places a trailing stop order 📉
- ``place_test_order()`` - Places a test order that does not execute 🧪
- ``close_all_positions()`` - Closes all open positions for user  ❌
- ``cancel_order()`` - Cancels a pending order ❌
- ``cancel_all_orders_of_symbol()`` - Cancels all pending orders for a trading pair ❌
- ``cancel_batch_orders()`` - Cancels multiple pending orders ❌

TODO 📝
-------

This package is functional but the following list should be achieved pre release:

- Add Response exception handling. 💥
- Implement the remaining less important endpoints. 🔧
- Leverage async/await (Use async methods and aiohttp to make requests asynchronously rather than blocking.) ⚡
- Add proper logging. (Add a structured logger like loguru to log requests, errors etc.) 📝
- Write tests. (Add unit and integration tests using pytest) ✅
- Refactor code to be more pythonic and modular. 🐍
- Add WS support to report order updates.

Disclaimer 📜
-------------

This open source code is provided "as is" without warranty of any kind. The author makes no representations or warranties about the accuracy, completeness, or suitability of this code for any purpose. Use of this code is at your own risk.

The author is not affiliated with BingX and is not liable for any damages arising from the use of this code. Cryptocurrency trading involves substantial risk of loss. You should not rely on this code as your sole method of trading. No promises or guarantees are made regarding the performance of any trades executed using this code. Always do your own research and due diligence before executing any trades.

This code is still under developement and may contain bugs and errors. Use at your own discretion.
