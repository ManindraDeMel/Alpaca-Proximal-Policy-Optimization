import gym
from gym import spaces
import numpy as np
from trading_utils import TradingUtils
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class TradingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, api, symbol, starting_balance=50000, stop_loss=0.2):
        super(TradingEnv, self).__init__()

        self.api = api

        self.symbol = symbol
        self.balance = starting_balance
        self.shares_held = 0
        self.current_price = 0
        self.previous_balance = starting_balance
        self.balance_history = [starting_balance]  # Initialize the balance history
        self.stop_loss = stop_loss
        self.percentages = {i: (i % 10 or 10) / 10 if i != 21 else 0 for i in range(22)}
        self.buy_prices = {}

        self.utils = TradingUtils(self.api)
        self.action_space = spaces.Discrete(22)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)


    def step(self, action):
        # Execute the action
        action_pct = self.percentages[action]
        price = self.utils.get_latest_price(self.symbol)
        cash_available = self.utils.get_account_balance()
        shares_available = self.utils.get_shares_held(self.symbol)

        if action == 21:  # Hold
            potential_buy_reward = (action_pct * cash_available) // price
            potential_sell_reward = action_pct * shares_available
            if potential_buy_reward > cash_available or potential_sell_reward == 0:
                reward = 10  # reward for profitable holding
            else:
                reward = 2  # no reward for holding
        elif action <= 10:  # Buy
            num_shares_to_buy = min((action_pct * cash_available) // price, cash_available // price)
            if num_shares_to_buy * price > cash_available:
                reward = -100  # Penalize if trying to buy more stocks than can afford
            elif num_shares_to_buy == 0:
                reward = -50  # Penalize if trying to buy zero stocks
            else:
                try:
                    self.utils.place_order(self.symbol, num_shares_to_buy, 'buy')
                    self.shares_held += num_shares_to_buy  # update the number of shares held
                    # Store the buy price for these shares
                    self.buy_prices[num_shares_to_buy] = price  
                    reward = 0  # No reward for valid buy action
                except Exception as e:
                    reward = -100  # Penalize if tried to buy more than available shares
                    print(f"Error occurred: {str(e)}")
        elif action > 10:  # Sell
            num_shares_to_sell = min(action_pct * shares_available, shares_available)
            if num_shares_to_sell == 0:
                reward = -50  # Penalize if trying to sell zero stocks
        else:
            avg_buy_price = sum(self.buy_prices.values()) / len(self.buy_prices)
            if price > avg_buy_price:  # Compare the current price to the average buy price
                reward = 1000  # Large reward for selling at a profit
            else:
                reward = 0  # No reward for selling at a loss
            self.utils.place_order(self.symbol, num_shares_to_sell, 'sell')
            self.shares_held -= num_shares_to_sell  # update the number of shares held


        # Calculate the reward
        new_balance = self.utils.get_account_balance()
        self.balance_history.append(new_balance)  # Update the balance history
        reward += new_balance - self.balance  # Additional reward based on balance
        self.balance = new_balance

        # Obtain the data
        end = datetime.now() - timedelta(days=2)  # 1 day ago
        start = end - timedelta(days=6)  # 5 days before the end date
        next_state_df = self.api.get_bars(self.symbol, '1D', start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d')).df
        next_state = next_state_df['close'].values.tolist()
        next_state = next_state + [self.balance, self.shares_held]

        # Check if the episode is done
        if  self.previous_balance * (1 - self.stop_loss) > self.balance:
            done = True
            self.reset()
        else:
            done = False
        
        print(f"\nReward for this cycle is: {reward}\n")

        return next_state, reward, done, {}


    def reset(self):        
        self.balance = self.utils.get_account_balance()
        self.previous_balance = self.balance
        self.balance_history = [self.balance]  # Reset the balance history
        self.shares_held = 0
        self.utils.sell_all_owned_shares()

        print(f"env reset. Starting balance is {self.balance}")
        # Get the last 5 days of price data for the stock

        # Compute start and end dates
        end = datetime.now() - timedelta(days=2)
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
        end = datetime.now() - timedelta(days=2)
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
