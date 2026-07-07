import numpy as np

g = 9.81
R = 8.314462618
M = 0.0289644
p0 = 1013.25

def rho(ele, temp):
    temp_k = temp + 273.125
    p = (p0 * np.exp(-g * M * ele / (R * temp_k))* 100)/(R * temp_k)
    return p

if __name__ == "__main__":
    print(rho(500, 30))