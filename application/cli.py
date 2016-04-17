import os  # for clearing console
import re  # regexp for validation

from application.aws.Connections import Connection  # AWS global connections
from application.aws.EC2 import EC2Instance  # AWS EC2
from application.aws.Volumes import Volumes  # AWS EC2 Volumes

# AWS Global connection
aws_conn = Connection()

# AWS EC2 connection
ec2conn = aws_conn.ec2Connection()

# AWS EC2 Instance obj
ec2i = EC2Instance()

# AWS Volumes obj
vols = Volumes()


def welcome_menu():
    """
    Shows main menu
    :return: option chosen
    """
    options = {'1': 'Compute', '2': 'Storage', '3': 'Monitoring', '4': 'changeme1', '5': 'changeme2'}
    __cls()
    print "*** Welcome to 3cli ***"
    print "Choose an option:"
    print "\t1. Compute"
    print "\t2. Storage"
    print "\t3. Monitoring"
    print "\t4. Autoscaling/AmazonDB/Relational DB Service/Elastic Load Balancing"
    print "\t5. Another service (API reference only)"
    op = raw_input("Enter option: ")
    # Validating entered option
    op = __op_validation('^[1-5]$', op)
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
        op_vendor = __op_validation(r'^[12]|(\\q)$', op_vendor)
        if op_vendor == "\\q":
            welcome_menu()
        else:
            # Show submenu of category Compute/Storage of AWS/OpenStack vendor
            _process_compute_storage(vendors[op_vendor], op_category)


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
    op = __op_validation(r'^[1-4]|(\\q)$', op)
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

    op = raw_input("Enter option: ")
    # Validating entered option
    op = __op_validation(r'^[1]|(\\q)$', op)
    if op == "\\q":
        _process_options("Compute")
    else:
        print 'process options'


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
    print "\t4. Download an object"
    print "\t5. Delete an object"
    print "Enter \'\\q\' to go back"

    op = raw_input("Enter option: ")
    # Validating entered option
    op = __op_validation(r'^[1-5]|(\\q)$', op)
    if op == "\\q":
        _process_options("Storage")
    else:
        print 'process options'


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
