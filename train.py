from dotenv import load_dotenv
from alpaca_trade_api.rest import REST
from stable_baselines3 import PPO
from trading_env import TradingEnv
import os

# Load environment variables
load_dotenv()

# Retrieve keys from environment variables
api_key = os.getenv('ALPACA_API_KEY')
secret_key = os.getenv('ALPACA_SECRET_KEY')
base_url = os.getenv('ALPACA_BASE_URL')

# Initialize your API here
api = REST(api_key, secret_key, base_url=base_url)

# Initialize environment
env = TradingEnv(api, 'AAPL')

# Initialize agent
model = PPO('MlpPolicy', env, verbose=1)

# Train agent
model.learn(total_timesteps=10000)

# Save the trained agent
model.save("ppo_trading_agent")
