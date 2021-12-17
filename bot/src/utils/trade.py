from pybit import HTTP
from typing import List, Dict, Any, Union
from utils.interfaces import MyPositionAmount, MyPositionLeverage
from pybit.exceptions import FailedRequestError, InvalidRequestError
import logging

logger = logging.getLogger(__name__)


class Trade:
    def __init__(self, api_key: str, api_secret: str, base_url: str) -> None:
        if base_url not in ["https://api.bybit.com"]:
            raise ValueError(f"Invalid 'base_url' {base_url}. base_url should be in ['https://api.bybit.com']")

        self.session = HTTP(base_url, api_key=api_key, api_secret=api_secret)

    # Get all symbols list.
    def symbols_list(self) -> List[str]:
        res: Any = self.session.query_symbol()
        symbols = [s["name"] for s in res["result"] if "name" in s]
        symbols = [s for s in symbols if "USDT" in s]
        return symbols

    # Get Leverage
    # if isIsolated is True, Isolated Margin is used.
    def set_leverage(self, symbol: str, buy_leverage: int, sell_leverage: int) -> Union[Dict, str]:
        if symbol.upper() not in self.symbols_list():
            raise ValueError(f"Invalid symbol {symbol} for Bybit USDT Perpetual.")

        if buy_leverage < 0 or sell_leverage < 0:
            raise ValueError(f"Invalid leverage value ['{buy_leverage}', '{sell_leverage}'. Leverage should be more than 0.")

        try:
            res: Any = self.session.set_leverage(
                symbol=symbol.upper(),
                buy_leverage=buy_leverage,
                sell_leverage=sell_leverage,
            )
            return res
        except FailedRequestError as e:
            err_msg = f"FailedRequestError: {e.message} (Trade.{self.set_leverage.__name__})"
            logger.error(err_msg)
            return err_msg
        except InvalidRequestError as e:
            err_msg = f"InvalidRequestError: {e.message} (Trade.{self.set_leverage.__name__})"
            logger.error(err_msg)
            return err_msg

    # To check my current position list.
    # If you have position, sell or buy with reduce only to close your posison.
    # If not, create a new position.
    def my_position_amount(self, symbol: str) -> Union[MyPositionAmount, str]:
        if symbol.upper() not in self.symbols_list():
            raise ValueError(f"Invalid symbol {symbol} for Bybit USDT Perpetual.")

        try:
            position_list: Union[Dict, str] = self.session.my_position(symbol=symbol.upper())
            if isinstance(position_list, Dict):
                position_amount: MyPositionAmount = {"buy": 0, "sell": 0}
                for item in position_list["result"]:
                    if item["side"] == "Buy":
                        position_amount["buy"] += item["size"]
                    elif item["side"] == "Sell":
                        position_amount["sell"] += item["size"]
                return position_amount
            else:
                return position_list
        except FailedRequestError as e:
            err_msg = f"FailedRequestError: {e.message} (Trade.{self.my_position_amount.__name__})"
            logger.error(err_msg)
            return err_msg
        except InvalidRequestError as e:
            err_msg = f"InvalidRequestError: {e.message} (Trade.{self.my_position_amount.__name__})"
            logger.error(err_msg)
            return err_msg

    # To check my current position list.
    # If you have position, sell or buy with reduce only to close your posison.
    # If not, create a new position.
    def my_position_leverage(self, symbol: str) -> Union[MyPositionLeverage, str]:
        if symbol.upper() not in self.symbols_list():
            raise ValueError(f"Invalid symbol {symbol} for Bybit USDT Perpetual.")

        try:
            position_list: Union[Dict, str] = self.session.my_position(symbol=symbol.upper())
            if isinstance(position_list, Dict):
                position_leverage: MyPositionLeverage = {"buy_leverage": 0, "sell_leverage": 0}
                for item in position_list["result"]:
                    if item["side"] == "Buy":
                        position_leverage["buy_leverage"] = item["leverage"]
                    elif item["side"] == "Sell":
                        position_leverage["sell_leverage"] = item["leverage"]
                return position_leverage
            else:
                return position_list
        except FailedRequestError as e:
            err_msg = f"FailedRequestError: {e.message} (Trade.{self.my_position_leverage.__name__})"
            logger.error(err_msg)
            return err_msg
        except InvalidRequestError as e:
            err_msg = f"InvalidRequestError: {e.message} (Trade.{self.my_position_leverage.__name__})"
            logger.error(err_msg)
            return err_msg

    # Create limit order for a new long or short position.
    def create_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        order_price: float,
        stop_loss_price: float,
    ) -> Union[Dict, str]:
        if side.lower() not in ["buy", "sell"]:
            raise ValueError(f"Invalid 'side' value {side}. 'side' should be in ['buy', 'sell']")

        if symbol.upper() not in self.symbols_list():
            raise ValueError(f"Invalid symbol {symbol} for Bybit USDT Perpetual.")

        side = side.upper()[0] + side.lower()[1:]

        try:
            res = self.session.place_active_order(
                symbol=symbol.upper(),
                side=side,
                order_type="Limit",
                qty=quantity,
                price=order_price,
                stop_loss=stop_loss_price,
                time_in_force="GoodTillCancel",
                reduce_only=False,
                close_on_trigger=False,
            )

            return res
        except FailedRequestError as e:
            err_msg = f"FailedRequestError: {e.message} (Trade.{self.create_limit_order.__name__})"
            logger.error(err_msg)
            return err_msg
        except InvalidRequestError as e:
            err_msg = f"InvalidRequestError: {e.message} (Trade.{self.create_limit_order.__name__})"
            logger.error(err_msg)
            return err_msg

    # Create limit order for a new long or short position.
    def close_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        order_price: float,
    ) -> Union[Dict, str]:
        if side.lower() not in ["buy", "sell"]:
            raise ValueError(f"Invalid 'side' value {side}. 'side' should be in ['buy', 'sell']")

        if symbol.upper() not in self.symbols_list():
            raise ValueError(f"Invalid symbol {symbol} for Bybit USDT Perpetual.")

        side = side.upper()[0] + side.lower()[1:]

        try:
            res = self.session.place_active_order(
                symbol=symbol.upper(),
                side=side,
                order_type="Limit",
                qty=quantity,
                price=order_price,
                time_in_force="GoodTillCancel",
                reduce_only=True,
                close_on_trigger=False,
            )

            return res
        except FailedRequestError as e:
            err_msg = f"FailedRequestError: {e.message} (Trade.{self.close_limit_order.__name__})"
            logger.error(err_msg)
            return err_msg
        except InvalidRequestError as e:
            err_msg = f"InvalidRequestError: {e.message} (Trade.{self.close_limit_order.__name__})"
            logger.error(err_msg)
            return err_msg

    # Cancel all active orders
    def cancel_all_active_orders(self, symbol: str) -> Union[Dict, str]:
        if symbol.upper() not in self.symbols_list():
            raise ValueError(f"Invalid symbol {symbol} for Bybit USDT Perpetual.")

        try:
            res = self.session.cancel_all_active_orders(symbol=symbol.upper())
            return res
        except FailedRequestError as e:
            err_msg = f"FailedRequestError: {e.message} (Trade.{self.cancel_all_active_orders.__name__})"
            logger.error(err_msg)
            return err_msg
        except InvalidRequestError as e:
            err_msg = f"InvalidRequestError: {e.message} (Trade.{self.cancel_all_active_orders.__name__})"
            logger.error(err_msg)
            return err_msg
