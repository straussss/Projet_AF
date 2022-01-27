from BinaryOption import BinaryOption

digital_call = BinaryOption(100, 100, 0.05, 0.01, 30, delta_max=1, volatility=0.25, payoff=1)

# Test digital call
print("### Test digital call")
print(f'Payoff = {digital_call.payoff}')
print(f'Price_digital_call = {digital_call.price_digital}')

digital_call.payoff = 2
print(f'Payoff modified = {digital_call.payoff}')
print(f'Price_digital_call = {digital_call.price_digital}')
#print(f'Price_bull_spread = {digital_call.price_bull_spread}')
