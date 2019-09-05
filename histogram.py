import csv
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


i = plt.figure(4)
cellExpressionArray = np.genfromtxt('S5Dlx_P36_1a_IHC_STR_10x_190829_dTomRed_50ms-Image Export-022019-8-29-17,45_Expression_Test_results.csv', delimiter=',')
plt.hist(cellExpressionArray, bins=20)
plt.ylabel('Frequency')
plt.xlabel('Expression Strength (0-255)')
plt.title('S5Dlx STR 50ms')
plt.show()

i = plt.figure(5)
cellExpressionArray = np.genfromtxt('S5Dlx_P36_2a_IHC_CA1_10x_190829_dTomRed_50ms-Image Export-012019-8-29-17,47_Expression_Test_results.csv', delimiter=',')
plt.hist(cellExpressionArray, bins=20)
plt.ylabel('Frequency')
plt.xlabel('Expression Strength (0-255)')
plt.title('S5Dlx CA1 50ms')
plt.show()
