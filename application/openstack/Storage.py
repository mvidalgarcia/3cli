import libcloud.storage.types


class StorageInstance:
    def __init__(self, driver):
        """ OpenStack Storage Instance Constructor """
        self.driver = driver

    def list_containers(self):
        """
        List all containers and associated info
        """
        containers = self.driver.list_containers()
        print "All OpenStack containers:"
        for c in containers:
            print "\tName:", c.name, "Number of objects:", c.extra['object_count']
        print

    def list_container_files(self, container_name):
        """
        List all files associated to a specific container
        :param container_name: Name of specific container
        """
        try:
            # Get container handler
            container = self.driver.get_container(container_name)
            # Retrieve objects from container
            objects = self.driver.list_container_objects(container)
            # Print info about objects
            print container_name, "objects:"
            for obj in objects:
                print '\tObject name:', obj.name, 'last modification on', obj.extra['last_modified'], 'Content type:', obj.extra['content_type']
            print
        except libcloud.storage.types.ContainerDoesNotExistError as e:
            print 'Container', container_name, 'does not exist.'

    def upload_file_to_container(self, container_name, filepath):
        """
        Upload a local file to OpenStack container
        :param container_name: Name of the container where file will be uploaded
        :param filepath: Local filepath of the file to upload
        """
        try:
            container = self.driver.get_container(container_name=container_name)
        except libcloud.storage.types.ContainerDoesNotExistError:
            print 'Container', container_name, 'does not exist.'
            return
        # Delete the path to get name in container equals name in OS
        filename = filepath.split('/')[-1]
        try:
            self.driver.upload_object(file_path=filepath, container=container, object_name=filename)
        except OSError:
            print 'File', filepath, 'does not exist'
            return
        print "File", filename, "uploaded to container", container_name
        print

    def download_file_from_container(self, container_name, filename):
        """
        Download locally a file from OpenStack container
        :param container_name: Name of the container
        :param filename: Name of the file to download
        """
        try:
            obj = self.driver.get_object(container_name=container_name, object_name=filename)
        except libcloud.storage.types.ContainerDoesNotExistError:
            print 'Container', container_name, 'does not exist.'
            return
        except libcloud.storage.types.ObjectDoesNotExistError:
            print 'File', filename, 'does not exist in container', container_name
            return
        self.driver.download_object(obj, './'+filename, overwrite_existing=True)
        print "File", filename, "downloaded to project root folder"
        print

    def delele_file_from_container(self, container_name, filename):
        """
        Delete file from OpenStack container
        :param container_name: Name of the container
        :param filename: Name of the file to delete
        """
        try:
            obj = self.driver.get_object(container_name=container_name, object_name=filename)
        except libcloud.storage.types.ContainerDoesNotExistError:
            print 'Container', container_name, 'does not exist.'
            return
        except libcloud.storage.types.ObjectDoesNotExistError:
            print 'File', filename, 'does not exist in container', container_name
            return
        self.driver.delete_object(obj)
        print "File", filename, "deleted from container", container_name
        print

    def create_container(self, container_name):
        bucket = self.driver.create_container(container_name)
        print "New container", container_name, "was created."
        print
        return bucket


