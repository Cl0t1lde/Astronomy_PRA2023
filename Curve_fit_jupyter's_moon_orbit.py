import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Load the Excel file
df = pd.read_excel("moon.xlsx")

# Print the column names to check
print(df.columns)

# Select time and one moon's x position (e.g., Callisto)
t = df['Unix time'].astype(float)
y = df['Callisto'].astype(float)

# Drop rows with missing data
mask = ~np.isnan(t) & ~np.isnan(y)
t = t[mask]
y = y[mask]

# Normalize time (for numerical stability)
t = t - t.min()

# Define the sinusoidal function
def sinusoid(t, A, omega, phi, offset):
    return A * np.sin(omega * t + phi) + offset

# Period of the moon callisto in seconds 
period_seconds = 16.7 * 86400  

# Define the guesses for the fit 
A_guess = (y.max() - y.min()) / 2
offset_guess = y.mean()
omega_guess = 2 * np.pi / period_seconds  # Period in seconds
phi_guess = 0
initial_guess = [A_guess, omega_guess, phi_guess, offset_guess]

# Print the initial guess 
print(f"Initial guess: A={A_guess}, omega={omega_guess}, phi={phi_guess}, offset={offset_guess}")

# Fit the curve
params, _ = curve_fit(sinusoid, t, y, p0=initial_guess, maxfev=10000)
A, omega, phi, offset = params
print(f"Fit result: A={A}, omega={omega}, phi={phi}, offset={offset}")

# Plot original data and fitted curve
t_fit = np.linspace(t.min(), t.max(), 1000)
y_fit = sinusoid(t_fit, A, omega, phi, offset)

plt.plot(t, y, 'bo', label='Data')
plt.plot(t_fit, y_fit, 'r-', label='Fit')
plt.xlabel("Time (Unix time)")
plt.ylabel("Pixel")
plt.title("Sinusoidal Fit to Callisto Data")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
