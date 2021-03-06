import boto
import boto.ec2
import boto.ec2.cloudwatch
import boto.rds
import boto.beanstalk


class AWSConnection:
    def __init__(self):
        """ Connection Instance """
        self.region = 'eu-west-1'  # Region used, change it if appropriate

    def ec2Connection(self):
        """ Create and return an EC2 Connection """
        conn = boto.ec2.connect_to_region(self.region)
        return conn

    def cwConnection(self):
        """ Create and return an EC2 CloudWatch Connection """
        return boto.ec2.cloudwatch.connect_to_region(self.region)

    def rdsConnection(self):
        """ Create and return a Relational Database Service (AWS RDS) Connection """
        return boto.rds.connect_to_region(self.region)

    def beanstalkConnection(self):
        """ Create and return an Elastic Beanstalk Connection """
        return boto.beanstalk.connect_to_region(self.region)
