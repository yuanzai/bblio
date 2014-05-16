import boto.ec2
import sys
sys.path.append('/home/ec2-user/bblio/')
from boto.manage.cmdshell import sshclient_from_instance
import keys
from config_file import get_config

es_instance = 'i-cacff0c3'
crawler_instance = 'i-15fa081d'
webserver_instance = 'i-2c5ff01a'


def conn():
    return boto.ec2.connect_to_region("us-west-2",
        aws_access_key_id=keys.aws_access_key_id,
        aws_secret_access_key=keys.aws_secret_access_key)

def startES():
    conn().start_instances(instance_ids=get_config().get('bblio','es_instance'))

def stopES():
    conn().stop_instances(instance_ids=get_config().get('bblio','es_instance'))

def getWebServerIP():
    return conn().get_all_instances(instance_ids=get_config().get('bblio','web_server_instance'))[0].instances[0].dns_name

def getWebServerInstance():
    return conn().get_all_instances(instance_ids=get_config().get('bblio','web_server_instance'))[0].instances[0]

def getESip():
    return conn().get_all_instances(instance_ids=get_config().get('bblio','es_instance'))[0].instances[0].dns_name

def getCrawlerIP():
    return conn().get_all_instances(instance_ids=get_config().get('bblio','crawler_instance'))[0].instances[0].dns_name

def getCrawlerInstance():
    return conn().get_all_instances(instance_ids=get_config().get('bblio','crawler_instance').split(';')[0])[0].instances[0]

def getCrawlerInstances():
    return [conn().get_all_instances(instance_ids=i)[0].instances[0] for i in get_config().get('bblio','crawler_instance').split(';')]


def copy_file_to_web_server(local_filepath,web_server_filepath):
    ssh_client = sshclient_from_instance(getWebServerInstance(),host_key_file = '/home/ec2-user/.ssh/known_hosts', ssh_key_file=keys.aws_pem,user_name='ec2-user')
    ssh_client.put_file(local_filepath, web_server_filepath)
