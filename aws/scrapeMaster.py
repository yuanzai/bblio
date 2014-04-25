import boto.ec2
import keys
import sys
from ec2 import getCrawlerInstance
from boto.manage.cmdshell import sshclient_from_instance
import os
import fnmatch

home_dir = '/home/ec2-user/bblio/'

def get_ssh_client():
    return sshclient_from_instance(getCrawlerInstance(), host_key_file = '/home/ec2-user/.ssh/known_hosts', ssh_key_file=keys.aws_pem,user_name='ec2-user')

def process_crawl(site_id):
    get_ssh_client().run('python2.7 ' + home_dir + 'scraper/scrapeController.py ' + str(site_id))

def crawl_site_id(site_id):
    import threading

    t = threading.Thread(target=process_crawl,args=(site_id,))

    t.setDaemon(True)
    t.start()

def clear_schedule(site_id):
    status, stdin, stderr = get_ssh_client().run('python2.7 ' + home_dir + 'scraper/scrapeController.py clear ' + str(site_id))

def copy_files():
    copyList = []   
    copyList.append(home_dir + 'build/search/models.py')
    copyList.append(home_dir + 'build/manage.py')
    for root, dirnames, filenames in os.walk(home_dir + 'scraper'):
        for filename in fnmatch.filter(filenames, '*.py'):
            copyList.append(os.path.join(root, filename))
    ssh_client = get_ssh_client()
    dirList = []

    for c in copyList:
        c_dir = os.path.dirname(c)
        prev_dir = ''
        while c_dir != prev_dir and c_dir not in home_dir:
            if c_dir not in dirList:
                dirList.append(c_dir)
            prev_dir = c_dir
            c_dir = os.path.dirname(c_dir)
    
    dirList.sort(lambda x,y: cmp(len(x), len(y)))

    for d in dirList:
        ssh_client.run('mkdir %s' % d)

    for c in copyList:
        ssh_client.put_file(c,c)


if __name__ == '__main__':
    arg = sys.argv
    if len(sys.argv) > 1:
        if arg[1] == 'copy':
            copy_files()


