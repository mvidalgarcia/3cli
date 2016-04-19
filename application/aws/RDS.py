import boto


class RDSInstance:
    """
    AWS Relational Database Service (Amazon RDS) allows tu create, manage and scale
    up or down relational databases. It supports well-known relational DB vendors such
    us MySQL, MariaDB, PostgreSQL, Oracle, Microsoft SQL Server.
    It also offers the possibility to have your DB replicated in different zones and
    regions, providing fault tolerance and failover.
    Source: https://aws.amazon.com/rds/

    This scrips allows to perform 4 different functionalities of Amazon RDS:
        - List all existing RDS instances and some associated info
        - View detailed info about in RDS instance
        - Create a new custom RDS instance from scratch
        - Delete an existing RDS instance
    """
    def __init__(self):
        pass

    def list_dbs(self, conn):
        """
        List RDS instances and associated info
        :param conn:
        """
        # Get all DBs
        dbs = conn.get_all_dbinstances()
        # Print information about DBs
        print "All RDS Databases:"
        for db in dbs:
            print '\tDatabase', db.id, 'Status:', db.status, 'Type:',\
                db.instance_class, 'Engine:', db.engine, 'Creation time:', db.create_time

    def show_dbinstance_info(self, conn, dbinstance_name):
        """
        Show detailed info about RDS instance
        :param conn: RDS connection
        :param dbinstance_name: RDS instance name
        """
        try:
            # Get specific instance
            instances = conn.get_all_dbinstances(dbinstance_name)
        except boto.exception.BotoServerError:
            print "No DB instance called", dbinstance_name
            return
        db = instances[0]
        # Show extended info
        print '\tDatabase', db.id, 'Status:', db.status, 'Type:',\
            db.instance_class, 'Engine:', db.engine, 'Creation time:',\
            db.create_time, '\n\tAZ:', db.availability_zone, 'Master username:',\
            db.master_username, 'Allocated storage:', str(db.allocated_storage)+'GB',\
            'Endpoint:', db.endpoint

    def create_dbinstance(self, conn, dbinstance_name, size, engine, username, password):
        """
        Create new DB instance
        :param conn: RDS connection
        :param dbinstance_name: Name of DB instance
        :param size: Storage allocation in Gigabytes
        :param engine: DB Engine (MySQL, Oracle, SQL Server...)
        :param username: User of DB
        :param password: Pass of DB
        """
        # Instance class: 'db.m1.small' by default
        try:
            conn.create_dbinstance(dbinstance_name, size, 'db.m1.small', username, password, engine=engine)
            print "New database created."
        except Exception as e:
            print e

    def delete_dbinstance(self, conn, dbinstance_name):
        """
        Delete DB instance
        :param conn: RDS connection
        :param dbinstance_name: Name of DB instance to delete
        """
        try:
            conn.delete_dbinstance(dbinstance_name, skip_final_snapshot=True)
            print 'Deleting DB instance', dbinstance_name
        except boto.exception.BotoServerError:
            print "No DB instance called", dbinstance_name
