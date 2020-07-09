# -*- coding:utf-8 -*-
"""
Consitent investmet
"""
import time
from alpha import const
from alpha.utils import tools
from alpha.utils import logger
from alpha.config import config
from alpha.market import Market
from alpha.trade import Trade
from alpha.order import Order
from alpha.orderbook import Orderbook
from alpha.kline import Kline
from alpha.markettrade import Trade as MarketTrade
from alpha.asset import Asset
from alpha.position import Position
from alpha.error import Error
from alpha.tasks import LoopRunTask
from alpha.order import ORDER_ACTION_SELL, ORDER_ACTION_BUY, ORDER_STATUS_FAILED, ORDER_STATUS_CANCELED, ORDER_STATUS_FILLED,\
    ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET
from alpha.const import ONE_DAY_INTERVAL

class StrategyEx1:

    def __init__(self):
        """ Init
        """
        self.strategy = config.strategy
        self.platform = config.accounts[0]["platform"]
        self.account = config.accounts[0]["account"]
        self.access_key = config.accounts[0]["access_key"]
        self.secret_key = config.accounts[0]["secret_key"]
        self.host = config.accounts[0]["host"]
        self.wss = config.accounts[0]["wss"]
        self.symbol = config.symbol
        self.raw_symbol = config.symbol
        self.last_trade_timestamp = 0

        self.ask1_price = 0
        self.bid1_price = 0
        self.ask1_volume = 0
        self.bid1_volume = 0

        # 交易模块
        cc = {
            "strategy": self.strategy,
            "platform": self.platform,
            "symbol": self.symbol,
            "account": self.account,
            "access_key": self.access_key,
            "secret_key": self.secret_key,
            "host": self.host,
            "wss": self.wss,
            "order_update_callback": self.on_event_order_update,
            "asset_update_callback": self.on_event_asset_update,
            "position_update_callback": self.on_event_position_update,
            "init_success_callback": self.on_event_init_success_callback,
        }
        self.trader = Trade(**cc)
        
        # 1秒执行1次
        LoopRunTask.register(self.on_ticker, ONE_DAY_INTERVAL)

    async def on_ticker(self, *args, **kwargs):
        """ 定时执行任务
        """
        ts_diff = int(time.time()) - self.last_trade_timestamp
        if ts_diff < ONE_DAY_INTERVAL:
            logger.warn("Schedule time is not reached:", self.strategy, self.symbol, ts_diff, caller=self)
            return
        await self.place_orders()
    
    async def place_orders(self):
        """ 下单
        """
        orders_data = []
        if self.trader.position and self.trader.position.short_quantity:
            # 平空单
            price = self.ask1_price - 0.1
            quantity = -self.trader.position.short_quantity
            action = ORDER_ACTION_BUY
            new_price = str(price)  # 将价格转换为字符串，保持精度
            if quantity:
                orders_data.append({"price": new_price, "quantity": quantity, "action": action, "order_type": ORDER_TYPE_LIMIT, "lever_rate": 1})
                self.last_ask_price = self.ask1_price
        if self.trader.assets and self.trader.assets.assets.get(self.raw_symbol):
            # 开空单
            price = self.bid1_price + 0.1
            volume = float(self.trader.assets.assets.get(self.raw_symbol).get("free")) * price // 100 
            if volume >= 1:
                quantity = - volume #  空1张
                action = ORDER_ACTION_SELL
                new_price = str(price)  # 将价格转换为字符串，保持精度
                if quantity:
                    orders_data.append({"price": new_price, "quantity": quantity, "action": action, "order_type": ORDER_TYPE_LIMIT, "lever_rate": 1})
                    self.last_bid_price = self.bid1_price

        if orders_data:
            order_nos, error = await self.trader.create_orders(orders_data)
            if error:
                logger.error(self.strategy, "create future order error! error:", error, caller=self)
            logger.info(self.strategy, "create future orders success:", order_nos, caller=self)

    async def on_event_order_update(self, order: Order):
        """ 订单状态更新
        """
        logger.debug("order update:", order, caller=self)

    async def on_event_asset_update(self, asset: Asset):
        """ 资产更新
        """
        logger.debug("asset update:", asset, caller=self)

    async def on_event_position_update(self, position: Position):
        """ 仓位更新
        """
        logger.debug("position update:", position, caller=self)
    
    async def on_event_init_success_callback(self, success: bool, error: Error, **kwargs):
        """ init success callback
        """
        logger.debug("init success callback update:", success, error, kwargs, caller=self)

