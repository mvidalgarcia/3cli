import boto.ec2
import boto.exception  # for handling exceptions


class Volumes:
    def __init__(self):
        """ Volumes Constructor """

    def list_volumes(self, conn):
        """ Lists volumes from an AWS account """
        # Get all volumes
        vols = conn.get_all_volumes()

        # If volumes found
        if vols:
            # Loop through volumes and print info
            for v in vols:
                print 'Volume Id:', v.id
                print 'Volume Status:', v.status
                print 'Volume Size:', v.size
                print 'Zone:', v.zone
                print 'Volume Type:', v.type

                # print attachment set object
                attachment_data = v.attach_data
                print 'Instance Id:', attachment_data.instance_id
                print 'Attached Time:', attachment_data.attach_time
                print 'Device:', attachment_data.device
                print '**********************************'
        else:
            print 'No volumes found'

    def attach_volume(self, conn, volume_id, instance_id):
        """ Attaches a volume to an EC2 instance """
        volumes = None
        try:
            # Get specific volume by id
            volumes = conn.get_all_volumes([volume_id])
        except boto.exception.EC2ResponseError as e:
            print "There is no volume", volume_id
            print e
        if volumes:
            # Attach volume to instance if it's 'available'
            if volumes[0].status == u'available':
                try:
                    conn.attach_volume(volume_id, instance_id, "/dev/sdh")
                except boto.exception.EC2ResponseError as e:
                    print "Error attaching volume", volume_id, "to instance", instance_id
                    print e
                print "Volume", volume_id, "attached successfully to instance", instance_id
            else:
                print "Volume", volume_id, "is in use."

    def detach_volume(self, conn, volume_id):
        """ Detaches a specific volume """
        volumes = None
        try:
            # Get specific volume by id
            volumes = conn.get_all_volumes([volume_id])
        except boto.exception.EC2ResponseError as e:
            print "There is no volume", volume_id
            print e
        if volumes:
            # Detach volume just if it is 'in use'
            if volumes[0].status == u'in-use':
                try:
                    conn.detach_volume(volume_id)
                except boto.exception.EC2ResponseError as e:
                    print "Error detaching volume", volume_id
                    print e
                print "Volume", volume_id, "detached successfully."
            else:
                print "Volume", volume_id, "is not attached to any instance."

