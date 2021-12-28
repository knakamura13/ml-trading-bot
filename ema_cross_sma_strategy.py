# 
# EMA Cross SMA Strategy
# 
# © Kyle Nakamura (kjnakamura)
# 
strategy("EMA Cross SMA Strategy", "EMA Cross", overlay=true)

# Set EMA and SMA lookback periods
EMAPeriod = input(50, "Fast EMA Period")
SMAPeriod = input(50, "Slow EMA Period")
STDPeriod = input(50, "Std. Dev. Period")

# Calculate EMA and SMA
EMA = ema(close, EMAPeriod)
SMA = sma(close, SMAPeriod)
STD = stdev(close, STDPeriod)

# Create buy/sell signals using crossover and crossunder
BUY = crossover(EMA, SMA)
SELL = crossunder(EMA, SMA)

# Plot EMA and SMA
plot(EMA, color=color.red, linewidth=2)
plot(SMA, color=color.blue, linewidth=2)

# Execute the strategy
if BUY:
    strategy.order("buy", strategy.long)
if SELL and strategy.position_size > 0:
    strategy.order("sell", strategy.short)

