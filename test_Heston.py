from Heston import Heston
import numpy as np

np.random.seed(seed=42)

test = Heston(100, 100, 0.05, 0.01, 30, 0.25)

print(test.W)

