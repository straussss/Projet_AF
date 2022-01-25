from VanillaOption import VanillaOption

#Test Call

call = VanillaOption(100, 100, 0.05, 0.01, 30, volatility=0.25)
print(call.Price)
print(call.Delta)
print(call.Gamma)
print(call.Theta)
print(call.Vega)

put = VanillaOption(100, 100, 0.05, 0.01, 30, typ='P', volatility=0.25)
print(put.Price)
print(put.Delta)
print(put.Gamma)
print(put.Theta)
print(put.Vega)

