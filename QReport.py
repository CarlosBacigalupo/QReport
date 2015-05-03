# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

'''
QReport.py
Creates a summary of GALAH data quality for a given date. 
'''

#########################
#Globals

out_folder = 'curr_report/'
repModules_folder = 'modules/'
data_base_folder = ''
emails = '' #email list to send results
log_file = out_folder + 'report.log'
input_catalogue = ''

#End of globals
##########################


okGo = True

#tests imports
try:
    print 'Importing glob module'
    import glob
except:
    print 'Imports failed. Module missing.'
    okGo=False
    

#tests report modules
try:
    
    repModules = glob.glob(repModules_folder+'*.py')
    if len(repModules)<1:
        print 'No modules found in',repModules_folder
        okGo=False
except: 
    print 'No modules found in',repModules_folder
    okGo=False


#checks for data
try:
    pass
except:
    okGo=False


#open log
try:
    pass
except: 
    okGo=False
    

# okGo==True if:
# -- all python modules have been loaded
# -- repModules has the list of report templates and >0. 

if okGo==True:
    print 
    print 'All tests succeeded. Creating reports...'
    
    #creates reports
    for thisModule in repModules:
        try:
            import thisModule
        except:
            print thisModule,'import failed. Skipping it.'
            
        print thisModule


#emails results



else:
    print 'Initial checks failed. Report not created'

# <codecell>


