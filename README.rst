================
This is py-bingx
================

py-bingx is an unofficial Python wrapper for the `BingX Perpetual Swap API <https://bingx-api.github.io/docs/swap/introduce.html>`_.
I am not affiliated with BingX.


TODO
----
Add Response exception handling.


Usage
-----

Register an account on `BingX <https://bingx.com/en-us/register>`_.

`Create an API <https://bingx.com/en-us/account/api>`_
and make sure you copy you Secret Key before leaving the page.

.. code:: bash

    pip install py-bingx

.. code:: python

    from bingx.api import BingxAPI

    ...

    API_KEY = '<api_public_key>'
    SECRET_KEY = '<api_secret_key>'

    # It is faster and more efficient to use local timestamps. If you are getting an error try using "server" timestamp.
    bingx = BingxAPI(API_KEY, SECRET_KEY, timestamp="local")
    bingx.open_market_order('FLOKI-USDT', 'LONG', 121220, tp="0.00001800", sl="0.00001700")
