# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

okGo = True
try:
    import numpy as np
    import pylab as plt
    import pyfits as pf
    import common as const
    reload(const)
    import os
    import glob
    import ebf
except: 
    print 'core: Import failed.'
    okGo = False

# <codecell>

if okGo==True:
    
    allStars = []
    allICStars = []

    fileList = glob.glob(const.galah_dir + str(const.d) + '/data/ccd_1/*.fits')

    for thisFileName in fileList:
        thisFile = pf.open(thisFileName)
        if thisFile[0].header['RUNCMD']=='RUN':
            fibres = thisFile['STRUCT.MORE.FIBRES'].data['TYPE']=='P'
            stars = thisFile['STRUCT.MORE.FIBRES'].data['NAME'][fibres] #program stars
            
#             try:
            ICStarsF = np.char.find(stars,'galahic_')!=-1
            ICStars = np.char.lstrip(stars[ICStarsF],'galahic_').astype(int)
#             except:
#                 ICStarsF = np.zeros(fibres.shape[0]).astype(bool)
#                 ICStars = np.char.lstrip(fibres[ICStarsF],'galahic_').astype(int)
                
            allStars=np.hstack((allStars,stars.tolist()))
            allICStars=np.hstack((allICStars,ICStars.tolist()))
            
        thisFile.close()

    allStars = np.unique(allStars)
    allICStars = np.unique(allICStars)
    totalStars = len(allStars)#.shape
    totalICStars = len(allICStars)#.shape
    
    print 'Total stars:',totalStars,'IC stars:', totalICStars

# <codecell>

if totalICStars>0:
    
    ID_Obs = allICStars
    ID_IC = ebf.read(const.base_folder+const.IC_folder+'galahic_v2.0L.ebf', '/galah_id')
    Bmag = ebf.read(const.base_folder+const.IC_folder+'galahic_v2.0L.ebf', '/apass_bmag ')
    Vmag = ebf.read(const.base_folder+const.IC_folder+'galahic_v2.0L.ebf', '/apass_vmag ')
    f = np.sum([ID_IC == ID_Obs[i] for i in range(ID_Obs.shape[0])],axis=0).astype(bool)
    
    create_CMD(Bmag[f], Vmag[f])

# <codecell>

plt.

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

