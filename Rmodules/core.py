# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import pylab as plt

# <codecell>

#Dummy code to follow
a = np.array([1,2,3])

# <codecell>

np.savetxt('main.txt',a)
plt.plot(a)
plt.savefig('plot1.png')

plt.plot(-a)
plt.savefig('plot2.png')

# <codecell>

output_files  = ['main.txt','plot1.png','plot2.png']

