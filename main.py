from trading_env import TradingEnv
env = TradingEnv(symbol="AAPL", starting_balance=100000)
initial_state = env.reset()
next_state, reward, done, _ = env.step(10)  # Try an arbitrary action (10 in this case)
env.render()
