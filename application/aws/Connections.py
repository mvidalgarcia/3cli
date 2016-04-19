import boto
import boto.ec2
import boto.ec2.cloudwatch


class AWSConnection:
    def __init__(self):
        """ Connection Instance """
        self.region = 'eu-west-1'

    def ec2Connection(self):
        """ Create and return an EC2 Connection """
        conn = boto.ec2.connect_to_region(self.region)
        return conn

    def cwConnection(self):
        """ Create and return an EC2 CloudWatch Connection """
        return boto.ec2.cloudwatch.connect_to_region(self.region)
