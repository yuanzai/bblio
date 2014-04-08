import boto.ec2
import keys

es_instance = 'i-cacff0c3'
crawler_instance = 'i-15fa081d'

conn = boto.ec2.connect_to_region("us-west-2",
        aws_access_key_id=keys.aws_access_key_id,
        aws_secret_access_key=keys.aws_secret_access_key)

def startES():
    conn.start_instances(instance_ids=es_instance)

def stopES():
    conn.stop_instances(instance_ids=es_instance)

def getESip():
    return conn.get_all_instances(instance_ids=es_instance)[0].instances[0].dns_name

def getCrawlerIP():
    return conn.get_all_instances(instance_ids=crawler_instance)[0].instances[0].dns_name

def getCrawlerInstance():
    return conn.get_all_instances(instance_ids=crawler_instance)[0].instances[0]

