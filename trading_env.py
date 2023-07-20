import gym
from gym import spaces
import numpy as np
from trading_utils import TradingUtils
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class TradingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, api, symbol, starting_balance=100000):
        super(TradingEnv, self).__init__()

        self.api = api

        self.symbol = symbol
        self.balance = starting_balance
        self.shares_held = 0
        self.current_price = 0
        self.previous_balance = starting_balance
        self.balance_history = [starting_balance]  # Initialize the balance history

        self.percentages = {i: (i % 10 or 10) / 10 for i in range(21)}  # Maps actions to percentages

        self.utils = TradingUtils(self.api)
        self.action_space = spaces.Discrete(21)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)


    def step(self, action):
        # Execute the action
        action_pct = self.percentages[action]
        if action_pct <= 1.0:  # Buy
            price = self.utils.get_latest_price(self.symbol)
            cash_available = self.utils.get_account_balance()
            num_shares_to_buy = (action_pct * cash_available) // price
            self.utils.place_order(self.symbol, num_shares_to_buy, 'buy')
        elif action_pct > 1.0:  # Sell
            num_shares_to_sell = action_pct // 2
            self.utils.place_order(self.symbol, num_shares_to_sell, 'sell')

        # Observe the next state
        next_state = self.api.get_barset(self.symbol, 'day', limit=5).df[self.symbol]

        # Calculate the reward
        new_balance = self.utils.get_account_balance()
        self.balance_history.append(new_balance)  # Update the balance history
        reward = new_balance - self.balance
        self.balance = new_balance

        # Check if the episode is done
        done = self.balance <= 0

        return next_state, reward, done, {}


    def reset(self):
        self.utils.reset_account_balance()
        self.balance = self.utils.get_account_balance()
        self.balance_history = [self.balance]  # Reset the balance history
        self.shares_held = 0

        # Get the last 5 days of price data for the stock

        # Compute start and end dates
        end = datetime.now() - timedelta(days=1)
        start = end - timedelta(days=6)  # Fetch data for the last 5 days

        # Get bars
        price_data = self.api.get_bars(self.symbol, '1D', start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d')).df


        price_data = price_data['close'].values.tolist()

        # Combine balance, shares_held, and price_data to create the initial state
        initial_state = price_data + [self.balance, self.shares_held]

        return initial_state

    def render(self):
        # Get the stock price history        
        # Compute start and end dates
        end = datetime.now() - timedelta(days=1)
        start = end - timedelta(days=101)  # Fetch data for the last 100 days

        # Get bars
        price_history = self.api.get_bars(self.symbol, '1D', start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d')).df
        prices = price_history['close'].values.tolist()

        # Plot the stock prices
        plt.figure(figsize=(10,6))
        plt.subplot(2, 1, 1)
        plt.plot(prices)
        plt.title('Stock price for {}'.format(self.symbol))

        # Plot the account balance
        plt.subplot(2, 1, 2)
        plt.plot(self.balance_history)
        plt.title('Account balance')
        plt.tight_layout()
        plt.show()
