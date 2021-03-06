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
    import datetime
except: 
    print 'core: Sub-modules import failed.'
    okGo = False


# <HEADER>
# Date: at the start of the observations (i.e. previous night)
# Observers: ??
# Number of stars, number of fields: from the data
# Seeing range: from the comments file

# <DATA>
# Map of newly observed fields: from the data
# map of all observed fields (color coded by survey/Kepler/other): ??
# (V,V-K) color-magnitude diagram of newly observed stars: from IC

def create_CMD(Kmag,Vmag):
    plt.scatter(Vmag-Kmag, Vmag, c='k', s=1)
    plt.title('Observed stars on '+convert_date(const.d))
    plt.xlabel('V-K [mag]')
    plt.ylabel('V [mag]')
    plt.gca().invert_yaxis() 
    plt.savefig('CMD.png')
    plt.close()
#     plt.show()
    output_files.append('CMD.png')

def create_fields_map(RA, Dec):
    plt.scatter(RA, Dec, c='k', s=50, marker='+')
    plt.title('Observed fields on '+convert_date(const.d))
    plt.xlabel('R.A. [h]')
    plt.ylabel('Dec. [deg]')
    plt.savefig('fields.png')
    plt.close()
#     plt.show()
    output_files.append('fields.png')

def convert_date(inDate):
    try:
        my_date = datetime.datetime.strptime(str(inDate), "%y%m%d")
        outDate =  my_date.strftime("%d %B %Y")
    except:
        print 'Could not convert date.'
        outDate = str(inDate)
    return outDate

def get_seeing_range():
    sRange = [0., 0.]
    try:
        comments = np.loadtxt(const.galah_dir+str(const.d)+'/comments/comments_'+str(const.d)+'.txt',delimiter=',' , usecols=[2])
        sRange = [np.min(comments), np.max(comments)] 
    except:
        pass
    return sRange

output_files = []
output_dict = {}
totalICStars = 0
allFields = []
RA = []
Dec = []

if okGo==True:
    
    output_dict['Observing Date'] = convert_date(const.d)
#     output_dict['Observers'] = ''

    allStars = []
    allBMStars = []
    allICStars = []

    fileList = glob.glob(const.galah_dir + str(const.d) + '/data/ccd_1/*.fits')

    for thisFileName in fileList:
        thisFile = pf.open(thisFileName)
        if ((thisFile[0].header['NDFCLASS']=='MFOBJECT') or (thisFile[0].header['NDFCLASS']=='MFFLX')):
            RA.append(thisFile[0].header['MEANRA'])
            Dec.append(thisFile[0].header['MEANDEC'])
            allFields.append(thisFile[0].header['CFG_FILE'])
            
            try:
                if thisFile[0].header['NDFCLASS']=='MFFLX':
                    BMstars = np.array([thisFile[0].header['STD_NAME']])
                    stars = np.array([])
                    ICStars =np.array([])
                    
                else:
                    fibres = thisFile['STRUCT.MORE.FIBRES'].data['TYPE']=='P'
                    stars = thisFile['STRUCT.MORE.FIBRES'].data['NAME'][fibres] #program stars

                    ICStarsF = np.char.find(stars,'galahic_')!=-1
                    ICStars = np.char.lstrip(stars[ICStarsF],'galahic_').astype(int)
                    BMstars = np.array([])

            except:
                stars = np.array([])
                ICStars =np.array([])
                BMstars = np.array([])
                
            allStars=np.hstack((allStars,stars.tolist()))
            allBMStars=np.hstack((allBMStars,BMstars.tolist()))
            allICStars=np.hstack((allICStars,ICStars.tolist()))
            
        thisFile.close()

    allStars = np.unique(allStars)
    allBMStars = np.unique(allBMStars)
    allICStars = np.unique(allICStars)
    allFields = np.unique(allFields)
    totalStars = len(allStars)
    totalBMStars = len(allBMStars)
    totalICStars = len(allICStars)
    totalFields = len(allFields)
    
    
    output_dict['Total Stars'] = totalStars
    output_dict['Total Benchmark Stars'] = totalBMStars
    output_dict['Total IC Stars'] = totalICStars
    output_dict['Total Fields'] = totalFields
    output_dict['Seeing Range'] = str(get_seeing_range())
    
#     print 'Total stars:',totalStars,'IC stars:', totalICStars

print 'Writing main.txt'
with open('main.txt','w') as f:
    for name, value in sorted(output_dict.items()):
        print ('%s : %s' % (name, value))
        f.write(name+': ')
        f.write(str(value))
        f.write('\n')
output_files.append('main.txt')

if totalICStars>0:
#     try:
    if const.IC_filename=='galahic_v2.0L.ebf':
        print 'Using ICv2'
        Kmag = ebf.read_ind(const.IC_folder+const.IC_filename, '/kmag',allICStars.astype(int))
        Vmag = ebf.read_ind(const.IC_folder+const.IC_filename, '/apass_vmag',allICStars.astype(int))
    else:
        print 'Using ICv1'
        Kmag = ebf.read_ind(const.IC_folder+const.IC_filename, '/data',allICStars.astype(int))['kmag']
        Vmag = ebf.read_ind(const.IC_folder+const.IC_filename, '/data',allICStars.astype(int))['vmag_jk']
        
        print 'Creating CMD'
    create_CMD(Kmag, Vmag)
#     except:
#         print 'Could not create CMD'
else:
    print 'No Input Catalogue stars found. CMD plot skipped'

print 'Creating fields map'
create_fields_map(RA, Dec)

