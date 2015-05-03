# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

'''
QReport.py
Creates a summary of GALAH data quality for a given date. 
'''

#########################
#Globals
fromaddr = 'kalumbe@internode.on.net'
emails = ['kalumbe@gmail.com','kalumbe@internode.on.net'] #email list to send results
out_folder = 'curr_report/'
repModules_folder = 'modules/'
base_folder = '/Users/Carlos/Documents/QReport/'
IC_folder = 'IC/' #input catalogue folder
log_file = out_folder + 'report.log'
files = [out_folder + 'dataReport.tar'] #files to attach to the email. 





############################################
#Functions

def sendEmail(fromaddr,toaddrs, files = None):
    
    #create MIME object
    msg = MIMEMultipart()
    msg['Subject'] = 'GALAH observing report'
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText('Attached todays summary'))

    #add attachments
    for f in files or []:
    with open(f, "rb") as fil:
        msg.attach(MIMEApplication(
            fil.read(),
            Content_Disposition='attachment; filename="%s"' % basename(f)
        ))
        print Content_Disposition='attachment; filename="%s"' % basename(f)
        

    # Credentials (if needed)
    # username = 'kalumbe'
    # password = ''

    # The actual mail deliver
    server = smtplib.SMTP('mail.internode.on.net', 25 )
    # server.set_debuglevel(True)
    # server.ehlo()
    # server.starttls()
    # server.ehlo()
    # server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()


    



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
except:
    print 'Imports failed. Module missing.'
    okGo=False
    
os.chdir(base_folder)
    
#tests report modules
if os.path.isdir(base_folder+repModules_folder)==False: os.makedirs(base_folder+repModules_folder) #creates curr_report folder
try:

    repModules = glob.glob(repModules_folder+'*.py')
    if len(repModules)<1:
        print 'No reports found in',repModules_folder
        okGo=False
except: 
    print 'No reports found in',repModules_folder
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
# -- repModules has the list of report templates and len(repModules)>0. 

if okGo==True:
    all_files = [] #final array with file list. n tuples 
    print 
    print 'Changing folder to',repModules_folder
    print 'All tests succeeded. Creating reports...'
    os.chdir(base_folder+repModules_folder)

    #loops all reports. Runs and compiles results for each. 
    for i,thisModuleName in enumerate(repModules):
        thisModule = None
        
        #load/runs a module
        try:
            thisModuleName = thisModuleName.split('/')[-1][:-3] #parse module name without folder and .py bit.
            print ''
            print '>>>>>Running',thisModuleName
            thisModule = importlib.import_module(thisModuleName)
            if thisModule!=None: reload(thisModule)
        except:
            print thisModule,' failed. Skipping it.'
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
                    print os.getcwd()
                    os.rename(thisFile,base_folder+out_folder+newFile) 
                except:
                    print thisFile, 'not found. Skipped.'

                all_files.append(output_files2)
                
    #prepares files
    print
    print 'Compressing files'
    os.chdir(base_folder+out_folder)
    os.system('tar -cf dataReport.tar *.*  --exclude=*.tar --remove-files')
             
    #emails results
    sendEmail(fromaddr,emails,files)
        
    print 

else:
    print 'Initial checks failed. Report not created'

# <codecell>

basename(f)

# <codecell>

f

# <codecell>

os.path.isdir("/home/el")

# <codecell>


