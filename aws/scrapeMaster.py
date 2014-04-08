import boto.ec2
import keys
from ec2 import getCrawlerInstance
from boto.manage.cmdshell import sshclient_from_instance
import os
import fnmatch

home_dir = '/home/ec2-user/bblio/'

ssh_client = sshclient_from_instance(getCrawlerInstance(), ssh_key_file=keys.aws_pem,user_name='ec2-user')


def crawl_site_id(site_id):
    status, stdin, stderr = ssh_client.run('python2.7 ' + home_dir + 'scraper/scrapeController.py ' + str(site_id))

def clear_schedule(site_id):
    status, stdin, stderr = ssh_client.run('python2.7 ' + home_dir + 'scraper/scrapeController.py clear ' + str(site_id))

def copy_files():
    copyList = []   
    copyList.append(home_dir + 'build/search/models.py')
    copyList.append(home_dir + 'build/manage.py')
    for root, dirnames, filenames in os.walk(home_dir + 'scraper'):
        for filename in fnmatch.filter(filenames, '*.py'):
            copyList.append(os.path.join(root, filename))

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


#ssh_client.close()


