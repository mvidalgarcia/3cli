import os  # for clearing console
import re  # regexp for validation


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
        if op_vendor == "\\q":
            _welcome_menu()
        else:
            # Validating entered option
            op_vendor = __op_validation('^[12]$', op_vendor)
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
    print "Show AWS menu of", category


def _menu_openstack(category):
    print "Show OpenStack menu of", category


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
