import boto.exception
from boto.s3.key import Key


class S3Instance:
    def __init__(self):
        """ S3Instance Constructor """

    def list_buckets(self, conn):
        """
        List S3 buckets
        :param conn: S3 connection
        """
        buckets = conn.get_all_buckets()
        print "Current AWS S3 buckets:"
        # Loop through buckets and print information
        for b in buckets:
            print "\tName:", b.name, "Creation date:", b.creation_date
            # print b.__dict__

    def create_bucket(self, conn, bucket_name):
        """
        Create new S3 bucket
        :param conn: S3 connection
        :param bucket_name: New bucket name
        :return: bucket instance
        """
        try:
            bucket = conn.create_bucket(bucket_name)
        except boto.exception.S3CreateError as e:
            print "Error creating S3 bucket."
            print e
        print "New S3 bucket", bucket_name, "was created."
        return bucket

    def upload_file_to_bucket(self, conn, bucket_name, filename):
        """
        Upload local file to S3 bucket
        :param conn: S3 conenction
        :param bucket_name: Bucket name to upload file to
        :param filename: File path to upload
        """
        try:
            b = conn.get_bucket(bucket_name)
            k = Key(b)
            # Delete the path to get name in S3 equals name in OS
            k.key = filename.split('/')[-1]
            k.set_contents_from_filename(filename)
            print "File", filename, "uploaded to S3 bucket", bucket_name
        except boto.exception.S3ResponseError as e:
            print "No S3 bucket called", bucket_name
            # print e
        except IOError as e:
            print e
        except Exception as e:
            print "Error uploading", filename, 'to bucket', bucket_name
            print e

    def list_bucket_files(self, conn, bucket_name):
        """
        List all files from a specific bucket
        :param conn: S3 conenction
        :param bucket_name: Bucket which upload file to
        """
        try:
            # Get bucket handler
            bucket = conn.get_bucket(bucket_name)
            print bucket_name, "files:"
            # Loop through bucket files an print name
            for key in bucket.list():
                print '\t', key.name.encode('utf-8')
        except boto.exception.S3ResponseError as e:
            print "No S3 bucket called", bucket_name

    def download_file_from_bucket(self, conn, bucket_name, filename):
        """
        Download a bucket object to the root of application folder
        :param conn: S3 connection
        :param bucket_name: Name of the bucket
        :param filename: Name of the file to download
        """
        try:
            # Obtain bucket by name
            bucket = conn.get_bucket(bucket_name)
            key = bucket.get_key(filename)
            if key is None:
                print "No file called", filename, "in bucket", bucket_name
            else:
                # Download contents to a local file
                key.get_contents_to_filename(key.name)
                print "File downloaded in project root."
        except boto.exception.S3ResponseError as e:
            print "No S3 bucket called", bucket_name

    def delete_file_from_bucket(self, conn, bucket_name, filename):
        """
        Delete an object from a bucket
        :param conn:  S3 connection
        :param bucket_name: Name of the bucket
        :param filename: Name of the file to delete
        """
        try:
            # Obtain bucket by name
            bucket = conn.get_bucket(bucket_name)
            key = bucket.get_key(filename)
            if key is None:
                print "No file called", filename, "in bucket", bucket_name
            else:
                # Delete file/bucket object
                key.delete()
                print 'File', filename, 'was deleted from bucket', bucket_name
        except boto.exception.S3ResponseError as e:
            print "No S3 bucket called", bucket_name
