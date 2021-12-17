# from typing import Optional
from typing import Dict
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.params import Query
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from utils.request import request_predict_endpoint
from utils.trade import Trade
from utils.interfaces import Settings

app = FastAPI()

template = Jinja2Templates(directory="templates")

settings = Settings()
trader = Trade(settings.BYBIT_API_KEY, settings.BYBIT_SECRET_KEY, settings.API_BASE_URL)


@app.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    return template.TemplateResponse("index.html", {"request": request})


@app.get("/trade")
def trade(
    symbol: str = Query(..., description="The target pair name of Bybit USDT Perpetual."),  # type: ignore
    leverage: int = Query(None, description="The sell and buy leverage."),  # type: ignore
):
    if symbol not in trader.symbols_list():
        raise HTTPException(status_code=404, detail=f"Invalid symbol {symbol}")

    results = {}
    if leverage is not None:
        res = trader.set_leverage(symbol=symbol, buy_leverage=leverage, sell_leverage=leverage)
        results["set_leverage"] = res

    # Cancel all active orders.
    res = trader.cancel_all_active_orders(symbol=symbol)
    results["cancel_all_active_orders"] = res

    # Check my position.
    my_position_amount = trader.my_position_amount(symbol=symbol)
    results["my_position_amount"] = my_position_amount

    # Get prediction value
    # predict_api_endpoint = os.environ.get("PREDICT_API_ENDPOINT", "http://localhost:8000/")
    # predict = request_predict_endpoint(predict_api_endpoint)
    predict = {"buy": 0.4345, "sell": 0.539, "buy_price": 45000, "sell_price": 50000}
    results["predict"] = predict

    if isinstance(predict, Dict) and isinstance(my_position_amount, Dict):
        results["predict"] = predict
        buy_predict = predict["buy"]
        sell_predict = predict["sell"]

        # Close short position or (and) create long position
        if buy_predict > 0:
            # If you have already short positions.
            if my_position_amount["sell"] > 0:
                # Close short position
                res = trader.close_limit_order(
                    symbol=symbol,
                    side="buy",
                    quantity=my_position_amount["sell"],
                    order_price=predict["buy_price"],
                )
                results["close_short_position"] = res

                # Create long position
                res = trader.create_limit_order(
                    symbol=symbol,
                    side="buy",
                    quantity=0.001,
                    order_price=predict["buy_price"],
                    stop_loss_price=predict["buy_price"] * 0.97,
                )
                results["create_buy_limit_order"] = res
            else:
                # Create long position
                res = trader.create_limit_order(
                    symbol=symbol,
                    side="buy",
                    quantity=0.001,
                    order_price=predict["buy_price"],
                    stop_loss_price=predict["buy_price"] * 0.97,
                )
                results["create_buy_limit_order"] = res

        if sell_predict > 0:
            # If you have already long positions.
            if my_position_amount["buy"] > 0:
                # Close long position
                res = trader.close_limit_order(
                    symbol=symbol,
                    side="sell",
                    quantity=my_position_amount["buy"],
                    order_price=predict["sell_price"],
                )
                results["close_long_position"] = res

                # Create short position
                res = trader.create_limit_order(
                    symbol=symbol,
                    side="sell",
                    quantity=0.001,
                    order_price=predict["sell_price"],
                    stop_loss_price=predict["sell_price"] * 1.03,
                )
                results["create_sell_limit_order"] = res
            else:
                # Create short position
                res = trader.create_limit_order(
                    symbol=symbol,
                    side="sell",
                    quantity=0.001,
                    order_price=predict["sell_price"],
                    stop_loss_price=predict["sell_price"] * 1.03,
                )
                results["create_sell_limit_order"] = res

    return {"results": results}
