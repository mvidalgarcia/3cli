from libcloud.compute.types import Provider as ComputeProvider
from libcloud.compute.providers import get_driver as get_compute_driver
from libcloud.storage.providers import get_driver as get_storage_driver
from libcloud.storage.types import Provider as StorageProvider
import libcloud.security

# It's very important that you place your Openstack API key and user
# in a file called 'trystack_api_key.cfg' in the project root

# Read api_key from file.
os_config_file = dict()
try:
    with open('trystack_api_key.cfg') as f:
        lines = f.readlines()
    for line in lines:
        os_config_file[line.split('=')[0]] = line.split('=')[1].strip()
except IOError as e:
    print 'Place a file called "trystack_api_key.cfg" with the API Key and user in project root.'
    exit()

USER = os_config_file['USER']
API_KEY = os_config_file['API_KEY']
AUTH_URL = 'http://128.136.179.2:5000'


class OpenStackConnection:
    def __init__(self):
        """
        OpenStack global connection constructor
        """
        self.region = 'RegionOne'
        self.OpenStackCompute = get_compute_driver(ComputeProvider.OPENSTACK)
        self.OpenStackStorage = get_storage_driver(StorageProvider.OPENSTACK_SWIFT)
        libcloud.security.CA_CERTS_PATH = ['ca-bundle.crt']

    def openstack_compute_driver(self):
        """
        :return: Openstack Compute Driver
        """
        driver = self.OpenStackCompute(USER, API_KEY, ex_force_auth_url=AUTH_URL,
                                       ex_force_auth_version='2.0_password',
                                       ex_tenant_name=USER,
                                       ex_force_service_region=self.region)
        return driver

    def openstack_storage_drive(self):
        """
        :return: OpenStack Storage Driver
        """
        driver = self.OpenStackStorage(USER, API_KEY, ex_force_auth_url=AUTH_URL,
                                       ex_force_auth_version='2.0_password',
                                       ex_tenant_name=USER,
                                       ex_force_service_region=self.region)
        return driver

