class BeanstalkInstance:
    def __init__(self):
        pass

    def create_application(self, conn, name, description):
        """
        Create a new Beanstalk application
        :param conn: Elastic Beanstalk connection
        :param name: Application name
        :param description: Application description
        """
        conn.create_application(name, description)
        print 'New Beanstalk application created'

    def delete_application(self, conn, name):
        """
        Delete an existing Beanstalk application
        :param conn: Elastic Beanstalk connection
        :param name: Application name to delete
        """
        a = conn.delete_application(name, terminate_env_by_force=True)
        print 'Beanstalk application called', name, 'was deleted'
