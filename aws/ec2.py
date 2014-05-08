import boto.ec2
from boto.manage.cmdshell import sshclient_from_instance
import keys

es_instance = 'i-cacff0c3'
crawler_instance = 'i-15fa081d'
webserver_instance = 'i-2c5ff01a'


conn = boto.ec2.connect_to_region("us-west-2",
        aws_access_key_id=keys.aws_access_key_id,
        aws_secret_access_key=keys.aws_secret_access_key)

def startES():
    conn.start_instances(instance_ids=es_instance)

def stopES():
    conn.stop_instances(instance_ids=es_instance)

def getWebServerIP():
    return conn.get_all_instances(instance_ids=webserver_instance)[0].instances[0].dns_name

def getWebServerInstance():
    return conn.get_all_instances(instance_ids=webserver_instance)[0].instances[0]

def getESip():
    return conn.get_all_instances(instance_ids=es_instance)[0].instances[0].dns_name

def getCrawlerIP():
    return conn.get_all_instances(instance_ids=crawler_instance)[0].instances[0].dns_name

def getCrawlerInstance():
    return conn.get_all_instances(instance_ids=crawler_instance)[0].instances[0]

def copy_file_to_web_server(local_filepath,web_server_filepath):
    ssh_client = sshclient_from_instance(getWebServerInstance(),host_key_file = '/home/ec2-user/.ssh/known_hosts', ssh_key_file=keys.aws_aws_pem,user_name='ec2-user')
    ssh_client.put(local_filepath, web_server_filepath)

