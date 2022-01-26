from BinaryOption import BinaryOption
from VanillaOption import VanillaOption

call = VanillaOption(100, 100, 0.05, 0.01, 30, volatility=0.25)
digital_call = BinaryOption(100, 100, 0.05, 0.01, 30, volatility=0.25, payoff=1)

#Test inheritance
print("### Test inheritance")
print(f'Price = {digital_call.Price == call.Price}')
print(f'Delta = {digital_call.Delta == call.Delta}')
print(f'Gamma = {digital_call.Gamma == call.Gamma}')
print(f'Theta = {digital_call.Theta == call.Theta}')
print(f'Vega = {digital_call.Vega == call.Vega}')

# Miscleanous
print("\n\n### Miscleanous")
print(f'Payoff = {digital_call.Payoff}')
digital_call.Payoff = 10
print(f'Payoff modified = {digital_call.Payoff}')

