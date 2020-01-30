import os
import shutil
import subprocess
from catherinemathey.wsgi import *
from django.core.management import call_command, ManagementUtility


this_memory = ''
PROJECT_NAME = 'catherinemathey'


def pprint(msg):
    global this_memory
    if this_memory != msg:
        this_memory = msg
        print(msg.ljust(60, '.'), end='', flush=True)
    else:
        print('Completed')


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
    pprint('Copying source code files')


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
    pprint('Dumping db into db.json')


def freeze_requirements():
    # freeze requirements in requirements.txt
    pprint('Freezing pip requirements')
    with open('requirements.txt', 'w') as file_:
        subprocess.call(['pip', 'freeze'], stdout=file_)
    pprint('Freezing pip requirements')


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
    pprint('Collecting static files')


def copy_statics():
    pprint('Copying static files')
    ignore_list = shutil.ignore_patterns('')
    shutil.copytree(os.path.join(current_path, 'static'), os.path.join(dist_path, 'source', 'static'))
    pprint('Copying static files')


def changing_settings():
    pprint('Applying prod settings.py')
    settings_path = os.path.join(dist_path, 'source', PROJECT_NAME)
    os.remove(os.path.join(settings_path, 'settings.py'))
    os.rename(os.path.join(settings_path, 'settings-prod.py'), os.path.join(settings_path,'settings.py'))
    pprint('Applying prod settings.py')


# Get current directory
current_path = os.getcwd()

# (Re)Create dist directory
dist_path = os.path.join(current_path, 'dist')
mk_dir(dist_path)

freeze_requirements()
copy_media_files()
copy_source_code()
collect_statics()
copy_statics()
dump_db()
changing_settings()

git config --global core.safecrlf false
git add -A
git remote add gandi git+ssh://1832840@git.sd6.gpaas.net/default.git
git push -f gandi d3

