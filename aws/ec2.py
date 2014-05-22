import boto.ec2
import sys
sys.path.append('/home/ec2-user/bblio/')
from boto.manage.cmdshell import sshclient_from_instance
import keys
from config_file import get_config


def conn():
    return boto.ec2.connect_to_region("us-west-2",
        aws_access_key_id=keys.aws_access_key_id,
        aws_secret_access_key=keys.aws_secret_access_key)

def startES():
    conn().start_instances(instance_ids=get_config().get('bblio','es_instance'))

def stopES():
    conn().stop_instances(instance_ids=get_config().get('bblio','es_instance'))

def getInstance(instance_name, attr=None):
    instance = conn().get_only_instances(instance_name)[0]
    if attr:
        try:
            instanceA = getattr(instance, attr)
            return instanceA
        except AttributeError:
            pass
    return instance

def getWebServerIP():
    return getInstance(get_config().get('bblio','web_server_instance'),'dns_name')

def getWebServerInstance():
    return getInstance(get_config().get('bblio','web_server_instance'))

def getESip():
    return getInstance(get_config().get('bblio','es_instance'),'dns_name')

def getCrawlerIP():
    return conn().get_all_instances(instance_ids=get_config().get('bblio','crawler_instance'))[0].instances[0].dns_name

def getInstanceFromInstanceName(instance_name):
    return conn().get_all_instances(instance_ids=instance_name)[0].instances[0]

def getCrawlerInstance():
    return conn().get_all_instances(instance_ids=get_config().get('bblio','crawler_instance').split(';')[0])[0].instances[0]

def getCrawlerInstances():
    return [getInstance(i) for i in get_config().get('bblio','crawler_instance').split(';')]


def copy_file_to_web_server(local_filepath,web_server_filepath):
    ssh_client = sshclient_from_instance(getWebServerInstance(),host_key_file = '/home/ec2-user/.ssh/known_hosts', ssh_key_file=keys.aws_pem,user_name='ec2-user')
    ssh_client.put_file(local_filepath, web_server_filepath)
