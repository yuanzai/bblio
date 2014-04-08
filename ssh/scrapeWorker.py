import paramiko
import sys
sys.path.append('/home/ec2-user/bblio/aws/')
import ec2


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ec2.getCrawlerIP(),username='ec2-user',key_filename='/home/ec2-user/bblio/aws/key.pem')

