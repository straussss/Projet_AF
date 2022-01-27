from VanillaOption import VanillaOption

call = VanillaOption(100, 100, 0.05, 0.01, 30, volatility=0.25)
print("### Test Call")
print(f'Price = {call.Price}')
print(f'Delta = {call.Delta}')
print(f'Gamma = {call.Gamma}')
print(f'Theta = {call.Theta}')
print(f'Vega = {call.Vega}')

put = VanillaOption(100, 100, 0.05, 0.01, 30, typ='P', volatility=0.25)
print("\n\n\n### Test Put")
print(f'Price = {put.Price}')
print(f'Delta = {put.Delta}')
print(f'Gamma = {put.Gamma}')
print(f'Theta = {put.Theta}')
print(f'Vega = {put.Vega}')

