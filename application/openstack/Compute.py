class ComputeInstance:
    def __init__(self, driver):
        self.driver = driver

    def list_instances(self):
        """ List OpenStack Instances and associated info """
        # Get all nodes info associated with this OpenStack account
        nodes = self.driver.list_nodes()

        print "All OpenStack instances:"
        # Loop through nodes and extract instance information
        for node in nodes:
            print '\tInstance Name:', node.name, ' Instance Id:', node.id, ' State:', node.extra['vm_state'],\
                'IP Address:', node.public_ips[0] if node.public_ips else None, 'Launch time:', node.extra['created']
        print

    def create_instance(self, ami_id, key_name, instance_name, instance_size):
        """ Creates an instance """
        print "Trying to create new instance..."
        sizes = self.driver.list_sizes()
        images = self.driver.list_images()
        size = [s for s in sizes if s.id == instance_size][0]
        image = [i for i in images if i.id == ami_id][0]
        node = self.driver.create_node(name=instance_name, image=image, size=size, ex_keyname=key_name)
        print "New instance id", node.id, "called", node.name, "was created.\n"

    def stop_instance(self, instance_id):
        """ Stops a running instance"""
        nodes = self.driver.list_nodes()
        node = [n for n in nodes if n.id == instance_id][0]
        if node.extra['status'] == u'running':
            self.driver.ex_stop_node(node)
            print "Instance id", instance_id, "now is stopped"
        elif node.extra['status'] == u'stopped':
            print "Instance " + instance_id + " is already stopped."
        else:
            print "Instance " + instance_id + " cannot be stopped, state: " + node.extra['status']
        print

    def terminate_instance(self, instance_id):
        """ Terminate an instance"""
        nodes = self.driver.list_nodes()
        node = [n for n in nodes if n.id == instance_id][0]

        if node.extra['status'] == u'terminated':
            print "Instance " + instance_id + " is already terminated."
        else:
            print "Terminating instance " + instance_id + "..."
            self.driver.destroy_node(node)
        print

    def terminate_all_instances(self):
        """ Terminate all instances """
        nodes = self.driver.list_nodes()
        for node in nodes:
            if node.extra['status'] != u'terminated':
                self.driver.destroy_node(node)
        print "All instances were terminated."
