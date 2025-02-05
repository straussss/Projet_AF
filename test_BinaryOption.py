from BinaryOption import BinaryOption

digital_call_1 = BinaryOption(100, 100, 0.05, 0.01, 30, delta_max=1, volatility=0.25, payoff=1,  typ='C', rep='C')

# Test digital call
print("### Test digital call")
print(f'Payoff = {digital_call_1.payoff}')
print(f'Delta_max = {digital_call_1.delta_max}')
print(f'Price_digital_call = {digital_call_1.price_digital}')
print(f'Price_bull_spread_call = {digital_call_1.price_spread}')

# digital_call.payoff = 2
# digital_call.delta_max = 10
# print(f'\nPayoff modified = {digital_call.payoff}')
# print(f'Delta_max modified = {digital_call.delta_max}')
# print(f'Price_digital_call = {digital_call.price_digital}')
# print(f'Price_bull_spread = {digital_call.price_spread}')
# print(f'Delta digital call : {digital_call.delta_th}')
# print(f'Delta bull spread : {digital_call.delta_rp}')

#print(f'\nStrike Overhedged : {digital_call.overhedge_spread}')

digital_call_2 = BinaryOption(100, 100, 0.05, 0.01, 30, delta_max=1, volatility=0.25, payoff=1, typ='C', rep='P')
# Test digital put
print("\n### Test digital call")
print(f'Payoff = {digital_call_2.payoff}')
print(f'Delta_max = {digital_call_2.delta_max}')
print(f'Price_digital_call = {digital_call_2.price_digital}')
print(f'Price_bull_spread_put = {digital_call_2.price_spread}')
