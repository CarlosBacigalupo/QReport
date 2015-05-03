# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np

# <codecell>

a = np.array(['one','two'])
np.savetxt('main.txt',a, fmt='%s')

# <codecell>

output_files = ['main.txt']

# <codecell>


