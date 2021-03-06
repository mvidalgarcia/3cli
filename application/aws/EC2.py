class EC2Instance:
    def __init__(self):
        """ EC2Instance Constructor """
        pass

    def list_instances(self, conn):
        """
        List EC2 Instances
        :param conn: EC2 connection
        """
        # Get all instance reservations associated with this AWS account
        reservations = conn.get_all_reservations()

        print "Running AWS EC2 instances:"
        # Loop through reservations and extract instance information
        for r in reservations:
            # Get all instances from the reservation
            instances = r.instances

            # Loop through instances and print instance information
            for i in instances:
                # Get instance name from the tags object
                tags = i.tags
                instancename = 'Default EC2 Instance Name'

                # Check for Name property in tags object
                if 'Name' in tags:
                    instancename = tags['Name']

                # Print instance information
                print '\tInstance Name:', instancename, ' Instance Id:', i.id, ' Instance type:', i.instance_type,\
                    ' State:', i.state, 'IP Address:', i.ip_address, 'Launch time:', i.launch_time,\
                    ' AMI id:', i.image_id, ' Region:', i._placement

    def show_instance_info(self, conn, instance_id):
        """
        Show info about EC2 instance
        :param conn: EC2 connection
        :param instance_id: EC2 instance id
        """
        # Get instance that matches with id provided
        try:
            reservations = conn.get_all_instances(instance_ids=[instance_id])
            # Print information
            i = reservations[0].instances[0]
            # Get instance name from the tags object
            tags = i.tags
            instancename = 'Default EC2 Instance Name'

            # Check for Name property in tags object
            if 'Name' in tags:
                instancename = tags['Name']
            print 'Instance Name:', instancename, ' Instance Id:', i.id, ' Instance type:', i.instance_type,\
                ' State:', i.state, 'IP Address:', i.ip_address, 'Launch time:', i.launch_time,\
                ' AMI id:', i.image_id, i.region
        except Exception:
            print "Instance id", instance_id, "doesn't exist."

    def start_new_instance(self, conn, ami_id, instance_name):
        """
        Starts a new EC2 instance
        :param conn: EC2 connection
        :param ami_id: AMI (Operative System)
        :param instance_name: Name of the new EC2 instance
        """
        # t2.micro by default (free tier)
        # Customize your key name!
        reservation = conn.run_instances(ami_id, key_name="cit-ec2-key", instance_type="t2.micro")
        instance = reservation.instances[0]
        # Add tag with
        conn.create_tags([instance.id], {"Name": instance_name})
        print "New instance id", instance.id, "called", instance_name, "was started."

    def start_instance(self, conn, instance_id):
        """
        Starts a stopped instance
        :param conn: EC2 connection
        :param instance_id: Stopped EC2 Instance id
        """
        try:
            # Get instance that matches with id provided
            reservations = conn.get_all_instances(instance_ids=[instance_id])
            instance = reservations[0].instances[0]
            # Start stopped instance
            instance.start()
            print "Instance id", instance.id, "was started."
        except Exception:
            print "Instance id", instance_id, "doesn't exist."

    def stop_instance(self, conn, instance_id):
        """
        Stops a running instance
        :param conn: EC2 connection
        :param instance_id: Running EC2 Instance id
        """
        try:
            reservations = conn.get_all_instances(instance_ids=[instance_id])
            instance = reservations[0].instances[0]
            if instance.state == u'running':
                # Stop instance just if it's running
                conn.stop_instances(instance_ids=[instance_id])
                print "Instance " + instance_id + " was stopped."
            elif instance.state == u'stopped':
                print "Instance " + instance_id + " is already stopped."
            else:
                print "Instance " + instance_id + " cannot be stopped, state: " + instance.state
        except Exception:
            print "Instance id", instance_id, "doesn't exist."

    def stop_all_instances(self, conn):
        """
        Stops all running instances
        :param conn: EC2 connection
        """
        for reservation in conn.get_all_instances():
            for instance in reservation.instances:
                if instance.state == u'running':
                    conn.stop_instances(instance_ids=[instance.id])
        print "All running instances were stopped"

    def terminate_instance(self, conn, instance_id):
        """
        Terminate an EC2 instance
        :param conn: EC2 connection
        :param instance_id: Running EC2 Instance id
        """
        try:
            reservations = conn.get_all_instances(instance_ids=[instance_id])
            instance = reservations[0].instances[0]
            if instance.state == u'terminated':
                print "Instance " + instance_id + " is already terminated."
            else:
                print "Terminating instance " + instance_id + "..."
                conn.terminate_instances(instance_ids=[instance_id])
        except Exception as e:
            print "Instance id", instance_id, "doesn't exist."

    def terminate_all_instances(self, conn):
        """ Terminate all instances """
        for reservation in conn.get_all_instances():
            for inst in reservation.instances:
                if inst.state != u'terminated':
                    conn.terminate_instances(instance_ids=[inst.id])
        print "All instances were terminated."
