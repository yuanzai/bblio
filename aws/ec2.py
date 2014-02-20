import boto.ec2
import keys

es_instance = 'i-cacff0c3'
conn = boto.ec2.connect_to_region("us-west-2",
        aws_access_key_id=keys.aws_access_key_id,
        aws_secret_access_key=keys.aws_secret_access_key)

def startES():
    conn.start_instances(instance_ids=es_instance)

def stopES():
    conn.stop_instances(instance_ids=es_instance)

def getESip():
    return conn.get_all_instances(instance_ids=es_instance)[0].instances[0].dns_name

