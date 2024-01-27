import os
from sys import argv

def specIndex(mst:str,array:list):
    for c,i in enumerate(array):
        if mst in i:
            return(c)
    return None  

#Local Vars
PROJ_PATH="C://Users//Mitesh//Documents//Python Projects//Django Projects"
STATIC=False
if '--static' in argv:
    STATIC=True
TEMPLATES=False
if '--templates' in argv:
    TEMPLATES=True

if specIndex('--port',argv):
    PORT=argv[specIndex('--port',argv)].split('=')[1]
else:
    PORT=8000
    
#Snippets Vars
RUN_BAT="python manage.py runserver 0.0.0.0:{PORT}"
MIGRATE_BAT="python manage.py makemigrations\npython manage.py migrate"
CMD_SHELL="start cmd.exe"
IPY_SHELL="manage.py shell"

os.chdir(PROJ_PATH)
sett={}

def createProj():
    name=input('Enter Project\'s Name: ')
    os.system(f'django-admin.exe startproject {name}')
    sett['Name']=name
    createSnippets(name)

def createSnippets(name):
    os.chdir(f'{PROJ_PATH}\{name}')
    print('Creating Snippets')
    #for run.bat
    createFile('run.bat',RUN_BAT.format(PORT=PORT))
    #for migrate.bat
    createFile('migrate.bat',MIGRATE_BAT)
    #for IPy shell
    createFile('django shell.bat',IPY_SHELL)
    #for cmd shell
    createFile('cmd.bat',CMD_SHELL)
    if STATIC==True:
        sett['Static']=True
        print('Creating Static')
        os.mkdir('static')

    if TEMPLATES==True:
        sett['Templates']='templates'
        print('Creating Templates...')
        os.mkdir('templates')
    createApp()

def createFile(name,snippet):
    o=open(name,'w')
    o.write(snippet)
    o.close()

def createApp():
    appN=input('Enter App Name: ')
    sett['AppName']=appN
    os.system(f'django-admin startapp {appN}')
    print("App Created...")
    settings()

#Mitesh's Snippets
#to find out Index no. if matching string is in element.


def settings():
    print('Configuring Settings...')
    os.chdir(sett["Name"])
    setf=open(f'settings.py','r').readlines()
    p=sett['AppName']
    
    if specIndex('INSTALLED_APPS',setf):
        setf.insert(specIndex('INSTALLED_APPS',setf)+1,f'    "{p}",\n')

    if specIndex('STATIC_URL',setf) and 'Static' in sett.keys():
        setf.insert(specIndex('STATIC_URL',setf)+1,'STATICFILES_DIRS = [BASE_DIR / "static"]')

    if specIndex('DIRS',setf) and 'Templates' in sett.keys():
        setf[specIndex('DIRS',setf)]=f"        'DIRS': [BASE_DIR / 'templates'],\n"

    os.rename(f'settings.py','settings.py.bak')
    with open('settings.py','w') as wfile:
        for i in setf: wfile.write(i)
    wfile.close()
    print('Done...')
    print('Project Successfully Created. You can now start Working...')
    
createProj()
#Author - Mitesh Vaid
