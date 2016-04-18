from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
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
        self.OpenStack = get_driver(Provider.OPENSTACK)
        libcloud.security.CA_CERTS_PATH = ['ca-bundle.crt']

    def openstack_driver(self):
        driver = self.OpenStack(USER, API_KEY, ex_force_auth_url=AUTH_URL,
                                ex_force_auth_version='2.0_password',
                                ex_tenant_name=USER,
                                ex_force_service_region=self.region)
        return driver
