import numpy as np
import math
import matplotlib.pyplot as plt
x = np.arange(1, 1000, 1)
u = 4096/1024
us = 30
F = 15*1024 
d = 2
# x
y = []
for t in x:
    y_1 = max(F/us, F/d, t*F/(us + t * u))
    y.append(y_1)
    print(y_1)
plt.plot(x, y, label="sigmoid")
plt.xlabel("x")
plt.ylabel("y")
# plt.ylim(0, 1)
plt.legend()
plt.show()
