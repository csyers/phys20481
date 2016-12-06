import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 10000)
y = np.sin(2*np.pi*0.5*x)



from gatspy.periodic import LombScargleFast

fmin = 0.1 # minimum frequency
fmax = 3 # maximum frequency
res = 10000 # number of frequencies to be analyzed btwn fmin & fmax

delta_f = (fmax-fmin)/res

# Compute the Lomb-Scargle periodogram of y as a function of x.
# The list comprehension below is a placeholder for the error array;
# if none is available, it simply gives each data point equal weight.
LS = LombScargleFast().fit(x, y, [1 for _ in x])
power = LS.score_frequency_grid(fmin, delta_f,res)

plt.subplot(121)
plt.plot(x, y)

plt.subplot(122)
# These are the frequencies corresponding with the power array.
freqs = np.linspace(fmin, fmax, res)
plt.plot(freqs, power)
plt.show()