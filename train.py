from alpaca_trade_api.rest import REST
from stable_baselines3 import PPO
from trading_env import TradingEnv

# Initialize your API here
api = REST('PKZABUTATLNSTGGE3X1Y', 'WgULwt9TOHq0GCVHz6bqur6JSnCY2GSWovSKg7gE', base_url='https://paper-api.alpaca.markets')

# Initialize environment
env = TradingEnv(api, 'AAPL')

# Initialize agent
model = PPO('MlpPolicy', env, verbose=1)

# Train agent
model.learn(total_timesteps=10000)

# Save the trained agent
model.save("ppo_trading_agent")
