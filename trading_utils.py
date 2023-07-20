class TradingUtils:
    def __init__(self, api):
        self.api = api
        self.initial_balance = 100000  # Set this to your actual initial balance
        self.balance_offset = 0

    def get_account_balance(self):
        account = self.api.get_account()
        return float(account.cash) - self.balance_offset

    def reset_account_balance(self):
        account = self.api.get_account()
        current_balance = float(account.cash)
        self.balance_offset = current_balance - self.initial_balance

    def place_order(self, symbol, qty, side='buy'):
        try:
            self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type='market',
                time_in_force='gtc'
            )
            print(f"{side.capitalize()} order placed: {qty} shares of {symbol}")
        except Exception as e:
            print(f"Error placing order: {str(e)}")

    def get_latest_price(self, symbol):
        bars_info = self.api.get_barset(symbol, 'minute', limit=1)
        return bars_info[symbol][0].c

    def get_account_balance(self):
        return float(self.api.get_account().cash)
