from libcloud.compute.types import Provider as ComputeProvider
from libcloud.compute.providers import get_driver as get_compute_driver
from libcloud.storage.providers import get_driver as get_storage_driver
from libcloud.storage.types import Provider as StorageProvider
import libcloud.security

# It's very important that you place your API key in a file called 'trystack_api_key.txt' in the project root
# Read api_key from file.
try:
    with open('trystack_api_key.txt') as f:
        key = f.readline()
except IOError as e:
    print 'Place a file called "trystack_api_key.txt" with the API Key in project root.'
    exit()

USER = 'marco.vidal-garcia'
API_KEY = key
AUTH_URL = 'http://128.136.179.2:5000'


class OpenStackConnection:
    def __init__(self):
        self.region = 'RegionOne'
        self.OpenStackCompute = get_compute_driver(ComputeProvider.OPENSTACK)
        self.OpenStackStorage = get_storage_driver(StorageProvider.OPENSTACK_SWIFT)
        libcloud.security.CA_CERTS_PATH = ['ca-bundle.crt']

    def openstack_compute_driver(self):
        driver = self.OpenStackCompute(USER, API_KEY, ex_force_auth_url=AUTH_URL,
                                       ex_force_auth_version='2.0_password',
                                       ex_tenant_name=USER,
                                       ex_force_service_region=self.region)
        return driver

    def openstack_storage_drive(self):

        driver = self.OpenStackStorage(USER, API_KEY, ex_force_auth_url=AUTH_URL,
                                       ex_force_auth_version='2.0_password',
                                       ex_tenant_name='marco.vidal-garcia',
                                       ex_force_service_region='RegionOne')
        return driver

