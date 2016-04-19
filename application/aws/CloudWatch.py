import boto
from boto.sns import connect_to_region  # for SNS notifications
import datetime  # for retrieving periodical metrics


class CloudWatch:
    def __init__(self):
        """ CloudWatch Constructor """

    def enable_cw(self, cw_conn):
        """
        Enable CloudWatch monitoring on all running instances. This could be changed so you enable monitoring on
        a specific Instance ID
        :param cw_conn: AWS CloudWatch connection
        :return:
        """
        # Create list of instance IDs
        list_inst_ids = []
        # Get information on currently running instances
        reservations = cw_conn.get_all_instances()
        # Create list of instances
        instances = [i for r in reservations for i in r.instances]
        # For loop checks for instance in list of instances
        for instance in instances:
            # If instance state is equals to running
            if instance.state == u'running':
                # Append instance ID to the list of instance IDs
                list_inst_ids.append(instance.id)

        # If there are running instances, start monitoring them
        if list_inst_ids:
            cw_conn.monitor_instances(list_inst_ids)
            print "Enabling CloudWatch in all running instances."
        else:
            print "No instances to monitor"

    def query_cw(self, instance_id, cw_conn):
        """
        Query CloudWatch for data about your instance
        :param instance_id: Instance which we want to get metrics from
        :param cw_conn: AWS CloudWatch Connection
        :return:
        """
        # Get all available metrics
        metrics = cw_conn.list_metrics()
        my_metrics = []
        for metric in metrics:
            if 'InstanceId' in metric.dimensions:
                # Filter by instance id provided
                if instance_id in metric.dimensions['InstanceId']:
                    my_metrics.append(metric)
                    # Select interval
                    end = datetime.datetime.utcnow()
                    start = end - datetime.timedelta(hours=1)
                    # Custom type of metric
                    datapoints = metric.query(start, end, 'Average', 'Percent')
                    if len(datapoints) > 0:
                        print metric
                        # Print metrics datapoints
                        for datapoint in datapoints:
                            print '\t', datapoint

    def cw_alarm(self, cw_conn, instance_id, email_address):
        """
        Setup a CW alarm to send a notification - Assume you have CW enabled, you want to be notified
        when certain conditions arise. This make use of the Simple Notification Service (SNS) to send
        an email of CW events using alarms
        :param instance: Instance id which the alarm will be activated in
        :param email: Email address to notify the user when the alarm is raised
        """
        # SNS instance
        sns = connect_to_region('eu-west-1')
        # Creating new topic in SNS
        topic = sns.create_topic('cpu_alarm')
        # Get topic ARN
        topic_arn = topic['CreateTopicResponse']['CreateTopicResult']['TopicArn']
        # Subscribing provided email to notify when alarm is raised
        try:
            sns.subscribe(topic_arn, 'email', email_address)
        except boto.exception.BotoServerError:
            print "Invalid email address"
            return
        # Select CPU utilisation metric from provided instance id
        try:
            metric = cw_conn.list_metrics(dimensions={'InstanceId': instance_id},
                                          metric_name="CPUUtilization")[0]
        except IndexError:
            print "Instance id", instance_id, "does not exist"
            return
        # Create alarm and set topic action
        # Alarm will trigger if 2 checks fail after 5 min, so if it was 10 min under 40% CPU utilisation
        metric.create_alarm(name='CPU alarm', comparison='<', threshold=40,
                            period=300, evaluation_periods=2, statistic='Average',
                            alarm_actions=[topic_arn], unit='Percent')
        print 'Alarm for instance', instance_id, 'created'

