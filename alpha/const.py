# -*- coding:utf-8 -*-

"""
some constants and global queues

Author: QiaoXiaofeng
Date:   2020/01/11
Email:  andyjoe318@gmail.com
"""

from collections import deque

# Version
VERSION = "1.0.2_200427_alpha"

# Exchange Names
HUOBI_SWAP = "huobi_swap"  # Huobi Swap https://huobiapi.github.io/docs/coin_margined_swap/v1/cn/
HUOBI_FUTURE = "huobi_future"  # Huobi Future https://huobiapi.github.io/docs/dm/v1/cn/#5ea2e0cde2
HUOBI_PRO = "huobi_pro" # Huobi Pro https://huobiapi.github.io/docs/spot/v1/cn/#185368440e

# Market Types
MARKET_TYPE_TRADE = "trade"
MARKET_TYPE_ORDERBOOK = "orderbook"
MARKET_TYPE_KLINE = "kline"
MARKET_TYPE_KLINE_60 = "kline_60min"

# REQUEST AGENT 
USER_AGENT = "AlphaQuant" + VERSION

# Others
MINUTES = 60
HOURS = 60 * MINUTES
DEFAULT_INTERVAL = 10 #* MINUTES
ONE_DAY_INTERVAL = 24# * HOURS