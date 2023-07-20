from alpaca_trade_api.rest import REST
from stable_baselines3 import PPO
from trading_env import TradingEnv

# Initialize your API here
api = REST('PKV6P7C3XAWBB8CEGM0T', 'YnYdBSPYUROHH8c7Ozlbud1qudV8SLcOtWSqBgN2', base_url='https://paper-api.alpaca.markets')

# Initialize environment
env = TradingEnv(api, 'AAPL')

# Initialize agent
model = PPO('MlpPolicy', env, verbose=1)

# Train agent
model.learn(total_timesteps=10000)

# Save the trained agent
model.save("ppo_trading_agent")
