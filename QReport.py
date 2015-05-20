# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

'''
QReport.py
Creates a summary of GALAH data quality for a given date. 
'''

#########################
#Globals
fromaddr = 'galah@aao.gov.au'
emails = ['kalumbe@gmail.com','kalumbe@internode.on.net'] #email list to send results
out_folder = 'curr_report/'
repModules_folder = 'Rmodules/'
base_folder = '/Users/Carlos/Documents/QReport/'
IC_folder = 'IC/' #input catalogue folder
log_file = out_folder + 'report.log'
galah_dir = '/Users/Carlos/Documents/HERMES/data/'


############################################
#Functions
def sendEmail(fromaddr, toaddrs, files = None):
    #create MIME message
    msg = MIMEMultipart()
    msg['Subject'] = 'GALAH observing report'
    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddrs)
    msg['Date'] = formatdate(localtime=True)
#     msg.attach(MIMEText('Attached todays summary'))

    #add attachments
    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(f)
            ))        

    # Credentials (if needed)
    username = 'kalumbe'
    password = ''

    # The actual mail delivery
    server = smtplib.SMTP('mail.internode.on.net', 25 )
    # server.set_debuglevel(True)
    # server.ehlo()
    # server.starttls()
    # server.ehlo()
    # server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

def create_common():
    file = open(base_folder+repModules_folder+'common.py','w')
    file.write('galah_dir = \'' +galah_dir+'\' \n')
    file.write('d = '+str(d)+'\n')
    file.write('base_folder = \'' +base_folder+'\' \n')
    file.write('IC_folder = \'' +IC_folder+'\' \n')
    file.close()
    
    


############################################
#Script starts
############################################
print 'Starting script'
print 'Changing to base folder', base_folder

okGo = True

#tests imports
try:
    print 'Importing glob module'
    import glob
    print 'Importing importlib module'
    import importlib
    print 'Importing os module'
    import os
    from os.path import basename
    print 'Importing email module'
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate
    print 'Importing smtplib module'
    import smtplib
    print 'Importing datetime module'
    from datetime import datetime
    print 'Importing sys module'
    import sys
except:
    print 'Imports failed. Module missing.'
    okGo=False
    
    
#tests report modules
if os.path.isdir(base_folder+repModules_folder)==False: os.makedirs(base_folder+repModules_folder) #creates curr_report folder
try:
    repModules = glob.glob(base_folder+repModules_folder+'*.py')
    if len(repModules)<1:
        print 'No reports found in',base_folder+repModules_folder
        okGo=False
except: 
    print 'No reports found in',base_folder+repModules_folder
    okGo=False

    
#checks for data
if okGo==True:
    if len(sys.argv)>1:
        d = sys.argv[1]
    else:
        d = str(datetime.utcnow()).split()[0].replace('-','')[2:]

    
    if (d.isdigit() and (len(d)==6)):

        if os.path.isdir(base_folder+repModules_folder)!=True:
            print base_folder+repModules_folder, 'not found.'
            okGo=False

        if os.path.isdir(galah_dir+str(d))!=True:
            print galah_dir+str(d), 'not found.'
            okGo=False
    else:
        print 'Incorrect format in the data path:', d 
        okGo=False

#open log
try:
    pass
except: 
    okGo=False
    

# okGo==True if:
# -- all python modules have been loaded
# -- repModules has the list of report templates and len(repModules)>0. 
if okGo==True:
    all_files = [] #final array with file list. n tuples where n=number of reports 

    print
    print 'Creating',repModules_folder+'common.py'
    create_common()
    print 

#     print 'Changing folder to',repModules_folder
#     os.chdir(base_folder+repModules_folder)
#     print 
    
    #loops all reports. Runs and compiles results for each. 
    print 'Found',len(repModules)-1,'modules.' #common.py is counted but not a report module, hence -1.
    print 'All tests succeeded. Creating reports...'
    for i,thisModuleName in enumerate(repModules):
        thisModule = None
        
        #load/runs a module
        try:
            thisModuleName = thisModuleName.split('/')[-1][:-3] #parse module name without folder and .py bit.
            if thisModuleName not in ['common', '__init__']:
                print ''
                print '>>>>>Running',thisModuleName
                thisModule = importlib.import_module(repModules_folder[:-1]+'.'+thisModuleName)
        except:
            print thisModuleName,'report failed. Skipping it.'
            print 'Error:',
            print sys.exc_info()
            thisModule=None

        #checks returned data
        if thisModule!=None:
            try:
                if len(thisModule.output_files)==0:
                    print 'No file list returned by ',thisModuleName
                    print thisModuleName+'.output_files exists but it''s empty'
                    thisModule=None
                else:
                    output_files2 = [str(i)+'_'+e for e in thisModule.output_files]
                    print 'Report module finished'
            except:
                print 'No file list returned by ',thisModuleName
                print thisModuleName+'.output_files doesn''t exist'
                thisModule=None
            
        
        #moves result to final folder
        if thisModule!=None:
            print 'Moving files...'
            for thisFile, newFile in zip(thisModule.output_files,output_files2):
                
                try:    
                    print '   Moving',thisFile,'to', base_folder+out_folder+newFile
                    os.rename(thisFile,base_folder+out_folder+newFile) 
                except:
                    print thisFile, 'not found. Skipped.'

                all_files.append(output_files2)
                
        print 
        
    #After reports finish, check output
    if len(all_files)>0:

        #prepares files
        print
        os.chdir(base_folder+out_folder)
        print 'Compressing files'
        os.system('tar -cf'+str(d)+'.tar *.*  --exclude=*.tar --remove-files')
        print

        #emails results
        print 'Sending email'
        files = [str(d)+'.tar'] #files to attach to the email. 
#         sendEmail(fromaddr,emails,files)

        print 
    else:
        
        print 'No files returned by report modules. Report not created.'
    
else:
    print 'Initial checks failed. Report not created'

