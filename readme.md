# Stock Trading Environment using Reinforcement Learning

This repository contains a custom reinforcement learning environment for stock trading using Alpaca's API. The objective of this project is to develop an intelligent trading bot that can make buy, sell, and hold decisions to maximize profit over time.

## Getting Started

To get started with the project, clone this repository to your local machine.

```bash
git clone https://github.com/<your_username>/stock-trading-rl.git
```

Next, navigate into the project's directory.

```bash
cd stock-trading-rl
```

## Prerequisites

The following libraries need to be installed for this project:

- gym: A toolkit for developing and comparing reinforcement learning algorithms.
- alpaca-trade-api: Alpaca's API client for Python.
- numpy: A package for scientific computing with Python.
- matplotlib: A Python 2D plotting library.

You can install them with:

```bash
pip install gym alpaca-trade-api numpy matplotlib
```

## Running the Project

Before running the project, make sure to update the `api_key` and `api_secret` parameters in the `api` object in the Trading Environment. These should correspond to your Alpaca API credentials.

The main code for the project is contained within `trading_env.py`. This file defines the `TradingEnv` class, which extends OpenAI Gym's `Env` class. The `TradingEnv` class implements the main functions required for a gym environment, including `step()`, `reset()`, and `render()`.

To create an instance of the environment, pass in the Alpaca API client, the symbol for the stock, and any additional parameters like starting balance or stop loss:

```python
env = TradingEnv(api, symbol="AAPL", starting_balance=50000, stop_loss=0.2)
```

You can then interact with the environment using the step() method, which takes an action and returns the next state, reward, and whether the episode is done:

```python
next_state, reward, done, _ = env.step(action)
```

The environment accepts discrete actions in the range of 0-21, where each number corresponds to a percentage of the available cash or stocks to buy or sell. Action 21 is reserved for the "hold" action.

## Project Structure

The project contains the following files:

- `trading_env.py`: This file contains the main code for the trading environment.
- `trading_utils.py`: This file contains helper functions for interacting with the Alpaca API, such as getting the latest price, placing an order, or getting the account balance.

## Results

You can visualize the performance of your agent by using the `render()`function of the environment, which plots the stock's closing price and your account balance over time.

```python
env.render()
```

## Disclaimer

This project is intended for educational and research purposes only. It is not intended to be used for actual trading. The authors are not responsible for any potential losses incurred as a result of using this code.

## License

This project is licensed under the terms of the MIT license.
