import os  # for clearing console
import re  # regexp for validation

from application.aws.Connections import AWSConnection  # AWS global connections
from application.aws.EC2 import EC2Instance  # AWS EC2
from application.aws.Volumes import Volumes  # AWS EC2 Volumes
from application.aws.S3 import S3Instance    # AWS S3
from boto.s3.connection import S3Connection  # AWS connection
from application.aws.CloudWatch import CloudWatch  # AWS CloudWatch
from application.aws.RDS import RDSInstance  # AWS RDS

from application.openstack.Connections import OpenStackConnection # OpenStack global connection
from application.openstack.Compute import ComputeInstance  # OpenStack Compute
from application.openstack.Storage import StorageInstance  # OpenStack Storage


# *** AWS - boto ***

# AWS Global connection
aws_conn = AWSConnection()
# AWS EC2 connection
ec2conn = aws_conn.ec2Connection()
# AWS EC2 Instance obj
ec2i = EC2Instance()
# AWS Volumes obj
vols = Volumes()
# AWS S3 connection
s3conn = S3Connection()
# AWS S3 object
s3i = S3Instance()
# AWS CloudWatch connection
cwconn = aws_conn.cwConnection()
# AWS CloudWatch obj
cwi = CloudWatch()
# AWS RDS connection
rdsconn = aws_conn.rdsConnection()
# AWS RDS obj
rdsi = RDSInstance()

# *** OpenStack - LibCloud ***

# OpenStack global connection
os_conn = OpenStackConnection()
# OpenStack Compute driver
os_compute_driver = os_conn.openstack_compute_driver()
# OpenStack Compute obj
os_compi = ComputeInstance(os_compute_driver)
# OpenStack Storage driver
os_storage_driver = os_conn.openstack_storage_drive()
# OpenStack Compute obj
os_stori = StorageInstance(os_storage_driver)


def welcome_menu():
    """
    Shows main menu
    :return: option chosen
    """
    options = {'1': 'Compute', '2': 'Storage', '3': 'Monitoring', '4': 'RDS', '5': 'changeme2', '6': 'exit'}
    __cls()
    print "*** Welcome to 3cli ***"
    print "Choose an option:"
    print "\t1. Compute"
    print "\t2. Storage"
    print "\t3. Monitoring"
    print "\t4. Relational Database Service"
    print "\t5. Another service (API reference only)"
    print "\t6. Exit"
    op = raw_input("Enter option: ")
    # Validating entered option
    op = __op_validation('^[1-6]$', op)
    _process_options(options[op])


def _process_options(op):
    """
    Shows submenu based on main menu chosen option
    :param op: option chosen ny user in main menu
    :return:
    """
    __cls()
    if op == 'Compute' or op == 'Storage':
        vendors = {'1': 'AWS', '2': 'OpenStack'}
        print op, "menu:"
        print "\t1. AWS"
        print "\t2. OpenStack"
        print "Enter \'\\q\' to go back"

        op_category = op
        op_vendor = raw_input("Enter option: ")
        # Validating entered option
        op_vendor = __op_validation(r'^([12]|\\q)$', op_vendor)
        if op_vendor == "\\q":
            welcome_menu()
        else:
            # Show submenu of category Compute/Storage of AWS/OpenStack vendor
            _process_compute_storage(vendors[op_vendor], op_category)
    elif op == 'Monitoring':
        _process_monitoring()

    elif op == 'RDS':
        _process_rds()

    elif op == 'exit':
        # Exit program
        exit()


def _process_compute_storage(vendor, category):
    """
    Shows submenu for Compute and Storage category
    :param vendor: selected vendor name (AWS, OpenStack)
    :param category: selected category name (Compute, Storage)
    :return:
    """
    if vendor == 'AWS':
        _menu_aws(category)
    elif vendor == 'OpenStack':
        _menu_openstack(category)


def _menu_aws(category):
    __cls()
    if category == "Compute":
        _menu_aws_compute()
    elif category == "Storage":
        _menu_aws_openstack_storage("AWS")


def _menu_openstack(category):
    __cls()
    if category == "Compute":
        _menu_openstack_compute()
    elif category == "Storage":
        _menu_aws_openstack_storage("OpenStack")


def _menu_aws_compute():
    __cls()
    print "AWS Compute menu"
    print "\t1. List all running instances"
    print "\t2. Show instance info"
    print "\t3. Start an stopped instance"
    print "\t4. Stop all instances"
    print "\t5. Stop a specific instance"
    print "\t6. Terminate all instances"
    print "\t7. Terminate a specific instance"
    print "\t8. List all volumes"
    print "\t9. Attach an existing volume to an instance"
    print "\t10. Detach a volume from an instance"
    print "\t11. Start a new instance (not previously addressed)"
    print "Enter \'\\q\' to go back"

    while True:
        op = raw_input("Enter option: ")
        # Validating entered option
        op = __op_validation(r'^([1-9]|1[01]|\\q)$', op)
        if op == "\\q":
            _process_options("Compute")
            break
        else:
            if op == '1':
                # List all running instances and associated info
                ec2i.list_instances(ec2conn)
            elif op == '2':
                # Ask user to enter instance id
                i_id = raw_input("Enter instance id: ")
                # Show info of instance
                ec2i.show_instance_info(ec2conn, i_id)
            elif op == '3':
                # Ask user to enter instance id
                i_id = raw_input("Enter instance id: ")
                # Star the selected instance
                ec2i.start_instance(ec2conn, i_id)
            elif op == '4':
                # Stop all running instances
                ec2i.stop_all_instances(ec2conn)
            elif op == '5':
                # Ask user to enter instance id
                i_id = raw_input("Enter instance id: ")
                # Stop instance
                ec2i.stop_instance(ec2conn, i_id)
            elif op == '6':
                # Terminate all instances
                ec2i.terminate_all_instances(ec2conn)
            elif op == '7':
                # Ask user to enter instance id
                i_id = raw_input("Enter instance id: ")
                # Terminate instance
                ec2i.terminate_instance(ec2conn, i_id)
            elif op == '8':
                # List all volumes
                vols.list_volumes(ec2conn)
            elif op == '9':
                # Ask user for instance id
                i_id = raw_input("Enter instance id: ")
                # Ask user for volume id
                vol_id = raw_input("Enter volume id: ")
                # Attach volume to instance.
                vols.attach_volume(ec2conn, vol_id, i_id)
            elif op == '10':
                # Ask user for volume id
                vol_id = raw_input("Enter volume id: ")
                # Detach volume from instance.
                vols.detach_volume(ec2conn, vol_id)
            elif op == '11':
                _menu_aws_compute_new_instance()


def _menu_aws_compute_new_instance():
    # AMIs dict
    amis = {'1': 'ami-31328842', '2': 'ami-8b8c57f8', '3': 'ami-f95ef58a', '4': 'ami-c6972fb5'}
    # Ask user to enter instance name
    i_name = raw_input("Enter instance name: ")
    # Ask user to choose OS
    print "Creating new instance.. Choose OS:"
    print "\t1. Amazon Linux"
    print "\t2. Red Hat Enterprise Linux 7.2"
    print "\t3. Ubuntu Server 14.04 LTS"
    print "\t4. Microsoft Windows Server 2012 R2 Base"
    op = raw_input("Enter option: ")
    # Validating entered option
    op = __op_validation(r'^([1-4]|\\q)$', op)
    if op == "\\q":
        _menu_aws_compute()
    else:
        # Create new fresh instance
        ec2i.start_new_instance(ec2conn, amis[op], i_name)


def _menu_openstack_compute():
    __cls()
    print "OpenStack Compute menu"
    print "\t1. List all running instances"
    print "Enter \'\\q\' to go back"

    while True:
        op = raw_input("Enter option: ")
        # Validating entered option
        op = __op_validation(r'^(1|\\q)$', op)
        if op == "\\q":
            _process_options("Compute")
        else:
            if op == '1':
                # List OpenStack instances
                os_compi.list_instances()


def _menu_aws_openstack_storage(vendor):
    """
    Common menu for both AWS and OpenStack storage
    :return:
    """
    __cls()
    print vendor, "Storage menu"
    print "\t1. List all buckets"
    print "\t2. List all objects in a bucket"
    print "\t3. Upload an object"
    print "\t4. Download an object from bucket"
    print "\t5. Delete an object from bucket"
    print "Enter \'\\q\' to go back"

    while True:
        op = raw_input("Enter option: ")
        # Validating entered option
        op = __op_validation(r'^([1-5]|\\q)$', op)
        if op == "\\q":
            _process_options("Storage")
            break
        else:
            if vendor == 'AWS':
                _process_aws_storage(op)
            elif vendor == 'OpenStack':
                _process_openstack_storage(op)


def _process_aws_storage(op):
    """
    Process AWS storage functions
    :param op: Storage option selected by user
    """
    if op == '1':
        s3i.list_buckets(s3conn)
    if op == '2':
        # Ask user for bucket name
        bucket_name = raw_input("Enter bucket name: ")
        # List its files
        s3i.list_bucket_files(s3conn, bucket_name)
    if op == '3':
        # Ask user for bucket name
        bucket_name = raw_input("Enter bucket name: ")
        # Ask user for file name
        file_name = raw_input("Enter file name (path): ")
        # Upload file to bucket
        s3i.upload_file_to_bucket(s3conn, bucket_name, file_name)
    if op == '4':
        # Ask user for bucket name
        bucket_name = raw_input("Enter bucket name: ")
        # Ask user for file name
        file_name = raw_input("Enter object name: ")
        # Download file from bucket
        s3i.download_file_from_bucket(s3conn, bucket_name, file_name)
    if op == '5':
        # Ask user for bucket name
        bucket_name = raw_input("Enter bucket name: ")
        # Ask user for file name
        file_name = raw_input("Enter object name: ")
        # Delete file from bucket
        s3i.delete_file_from_bucket(s3conn, bucket_name, file_name)


def _process_openstack_storage(op):
    """
    Process OpenStack storage functions
    :param op: Storage option selected by user
    """
    if op == '1':
        # List containers
        os_stori.list_containers()
    if op == '2':
        # Ask user for container name
        container_name = raw_input("Enter container name: ")
        # List its files
        os_stori.list_container_files(container_name)
    if op == '3':
        # Ask user for container name
        container_name = raw_input("Enter container name: ")
        # Ask user for file name
        file_name = raw_input("Enter file name (path): ")
        # Upload file to container
        os_stori.upload_file_to_container(container_name, file_name)
    if op == '4':
        # Ask user for container name
        container_name = raw_input("Enter container name: ")
        # Ask user for file name
        file_name = raw_input("Enter object name: ")
        # Download file from container
        os_stori.download_file_from_container(container_name, file_name)
    if op == '5':
        # Ask user for container name
        container_name = raw_input("Enter container name: ")
        # Ask user for file name
        file_name = raw_input("Enter object name: ")
        # Delete file from container
        os_stori.delele_file_from_container(container_name, file_name)


def _process_monitoring():
    """
    Process monitoring menu
    """
    print "Monitoring menu:"
    print "\t1. Display AWS EC2 instance metrics"
    print "\t2. Set alarm (<40% CPU utilisation)"
    print "Enter \'\\q\' to go back"
    while True:
        op = raw_input("Enter option: ")
        # Validating entered option
        op_vendor = __op_validation(r'^([12]|\\q)$', op)
        if op_vendor == "\\q":
            welcome_menu()
            break
        else:
            if op == '1':
                # List instances to select ID
                ec2i.list_instances(ec2conn)
                # Ask user for instance id
                instance_id = raw_input("Enter instance id: ")
                # Enable CloudWatch
                cwi.enable_cw(ec2conn)
                # Query CloudWatch metrics
                cwi.query_cw(instance_id, cwconn)
            elif op == '2':
                ec2i.list_instances(ec2conn)
                # Ask user for instance id
                instance_id = raw_input("Enter instance id: ")
                # Ask user for email address to notifify
                email_address = raw_input("Enter email address of notification alarm: ")
                cwi.cw_alarm(cwconn, instance_id, email_address)

def _process_rds():
    """
    Process Relational Database Service menu
    """
    print "Relational Database Service menu:"
    print "\t1. List DB instances"
    print "\t2. Show DB info"
    print "\t3. Create DB instance"
    print "\t4. Delete DB instance"
    print "Enter \'\\q\' to go back"
    while True:
        op = raw_input("Enter option: ")
        # Validating entered option
        op_vendor = __op_validation(r'^([1-4]|\\q)$', op)
        if op_vendor == "\\q":
            welcome_menu()
            break
        else:
            if op == '1':
                # List DB instances
                rdsi.list_dbs(rdsconn)
            elif op == '2':
                # Ask user for dbinstance name
                dbinstance_name = raw_input("Enter DB instance name: ")
                # Show info
                rdsi.show_dbinstance_info(rdsconn, dbinstance_name)
            elif op == '3':
                # Ask user for dbinstance name
                dbinstance_name = raw_input("Enter DB instance name: ")
                # Ask user for db size
                size = raw_input("Enter DB instance size (in GB): ")
                # Ask user for dbinstance engine
                engine = raw_input("Enter DB instance engine (MySQL/oracle-ee/postgres): ")
                # Ask user for dbinstance user name
                username = raw_input("Enter DB user name: ")
                # Ask user for dbinstance password
                password = raw_input("Enter DB instance password: ")
                rdsi.create_dbinstance(rdsconn, dbinstance_name, size, engine, username, password)
            elif op == '4':
                # Ask user for dbinstance name
                dbinstance_name = raw_input("Enter DB instance name: ")
                rdsi.delete_dbinstance(rdsconn, dbinstance_name)



# Utils

def __op_validation(regex, op):
    """
    Input option validation
    :param regex: Regular expresion to match
    :return: valid option
    """
    while not re.match(regex, op):
        op = raw_input("Invalid option, try again: ")
    return op


def __cls():
    """
    Clear the console (cross-platform).
    """
    os.system('cls' if os.name == 'nt' else 'clear')
