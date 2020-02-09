import os
import shutil
import subprocess



from catherinemathey.wsgi import *
from django.core.management import call_command, ManagementUtility
import stat


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)



"""
User data to define manually
"""
PROJECT_NAME = 'catherinemathey'
GANDI_URL = 'd90e5820744144abb46bcbff3efd5424.testing-url.ws'
GANDI_USER = '2090221'
GANDI_GIT_REMOTE = 'git remote add gandiAuto git+ssh://2090221@git.sd6.gpaas.net/default.git'
GANDI_DEPLOY = 'ssh 2090221@git.sd6.gpaas.net deploy default.git'
GANDI_DB_ROOT = 'hosting_db'

"""
User data prompted (mostly passwords)
"""
GANDI_DB_PSW = ''
GANDI_PSW = ''


def pprint(msg):
    if msg == 'Completed':
        print('Completed')
    else:
        print(msg.ljust(60, '.'), end='', flush=True)


def mk_dir(dir_path):
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        print("Deleted directory : %s " % dir_path)
    try:
        os.mkdir(dir_path)
    except OSError:
        print("Creation of the directory %s failed" % dir_path)


def copy_source_code():
    # Create source sub-directory
    pprint('Copying source code files')
    source_path = os.path.join(dist_path, 'source')
    ignore_list = shutil.ignore_patterns('pipenv', 'venv', 'db.sqlite3', 'deploy.py', '.gitignore', '.git',
                                         '__pycache__', 'dist', 'media', '.idea')
    shutil.copytree(current_path, source_path, ignore=ignore_list)
    pprint('Completed')


def copy_media_files():
    # Create media sub-directory
    media_path = os.path.join(dist_path, 'media')
    shutil.copytree(os.path.join(current_path, 'media'), media_path, ignore=shutil.ignore_patterns('CACHE'))


def dump_db():
    # Create db sub-directory
    db_path = os.path.join(dist_path, 'db')
    mk_dir(db_path)
    pprint('Dumping db into db.json')
    output = open(os.path.join(db_path,'db.json'), 'w')
    call_command('dumpdata', '--exclude', 'auth.permission', '--exclude', 'contenttypes', format='json', indent=4, stdout=output)
    output.close()
    pprint('Completed')


def freeze_requirements():
    # freeze requirements in requirements.txt
    pprint('Freezing pip requirements')
    with open('requirements.txt', 'w') as file_:
        subprocess.call(['pip', 'freeze'], stdout=file_)
    pprint('Completed')


def collect_statics():
    # clean static files
    pprint('Collecting static files')
    utility_args = [
        'django-admin.py',
        'collectstatic',
        '--noinput',
        '--clear',
        '-v 0',
        '--settings=catherinemathey.settings']
    utility = ManagementUtility(utility_args)
    utility.execute()
    pprint('Completed')


def remove_statics():
    pprint('Deleting collected static files')
    ignore_list = shutil.ignore_patterns('')
    shutil.rmtree(os.path.join(current_path,'dist', 'source', 'static'))
    pprint('Completed')

def remove_git():
    pprint('Remove git link')
    ignore_list = shutil.ignore_patterns('')
    shutil.rmtree(os.path.join(current_path, 'dist', 'source', '.git'))
    pprint('Completed')


def changing_settings():
    pprint('Applying prod settings.py')
    settings_path = os.path.join(dist_path, 'source', PROJECT_NAME)
    os.remove(os.path.join(settings_path, 'settings.py'))
    os.rename(os.path.join(settings_path, 'settings-prod.py'), os.path.join(settings_path,'settings.py'))
    pprint('Completed')


def init_local_git():
    commands = '''cd dist
    cd source
    git init
    git add -A
    git commit -m "release test"
    git remote add gandiShell git+ssh://2090221@git.sd6.gpaas.net/default.git
    git push gandiShell master
    Geakxepo2!g
    '''
    process = subprocess.Popen("cmd.exe", shell=False, universal_newlines=True,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate(commands)
    print(out)

# Get current directory
current_path = os.getcwd()

# (Re)Create dist directory
shutil.rmtree(os.path.join(current_path,'dist'), onerror=remove_readonly)

dist_path = os.path.join(current_path, 'dist')
#remove_git()
mk_dir(dist_path)

freeze_requirements()
copy_media_files()
copy_source_code()
remove_statics()
dump_db()
changing_settings()
init_local_git()
"""
git config --global core.safecrlf false
git add -A
git remote add gandi git+ssh://1832840@git.sd6.gpaas.net/default.git
git push -f gandi d3
"""
