import datetime
# bucket = []


class BucketModal(object):
    bucket = []
    """
    This class handle all model operations on th bucket
    """
    def __init__(self, name, desc):

        """
        This Constructor initialises all the parameter required
        :param name: 
        :param desc: 
        """
        self.bucket_id = len(BucketModal.bucket)+1
        self.name = name
        self.desc = desc
        self.date_created = datetime.datetime.utcnow()
        self.modify_date = None

    #-----------------------------------------------------------------------

    def create_bucket(self):
        """ 
        This methods adds the bucket 
        """
        BucketModal.bucket.append(self)
        return self.bucket_id

    #-----------------------------------------------------------------------

    @staticmethod
    def check_for_buckets_available():
        if len(BucketModal.bucket) >=1:
            return len(BucketModal.bucket)

    @staticmethod
    def get_buckets():
        """ 
        This method gets all the buckets
        """
        buckets_list = []

        for item in BucketModal.bucket:

            buckets_list.append({'id': item.bucket_id,
                             'name': item.name,
                             'desc': item.desc,
                             'date_created': item.date_created,
                             'date_modified': item.modify_date,
                             })
        return buckets_list



    #-----------------------------------------------------------------------

    @staticmethod
    def get_bucket(bucket_id):
        """
        This method gets a specific bucket using the id
        :param bucket_id: 
        :return: 
        """
        response = []
        for item in BucketModal.bucket:
            if item.bucket_id == bucket_id:
                response.append({'id': item.bucket_id,
                                 'name': item.name,
                                 'description': item.desc,
                                 'date_created': item.date_created,
                                 'date modified': item.modify_date
                                 })
                return response



    # ----------------------------------------------------------------------
    @staticmethod
    def modify_bucket(modify_id, name, desc):
        """
        This method modifies a an existing bucket 
        :param modify_id: 
        :param name: 
        :param desc: 
        :return: 
        """
        for this_bucket in BucketModal.bucket:
            if this_bucket.bucket_id == modify_id:
                if this_bucket.name == name:
                    return None
                this_bucket.name = name
                this_bucket.desc = desc
                this_bucket.modify_date = datetime.datetime.utcnow()
                return this_bucket.bucket_id
    #-----------------------------------------------------------------------

    @staticmethod
    def delete_bucket(del_id):
        """
        This method deletes a bucket from the system
        :param del_id: 
        :return: 
        """
        for this_bucket in BucketModal.bucket:
            if this_bucket.bucket_id == del_id:
                BucketModal.bucket.remove(this_bucket)
                deleted = 1
                return deleted

    #---------------------------------------------------------------------
    @staticmethod
    def get_bucket_by_name(bucket_name):
        for item in BucketModal.bucket:
            if item.name == bucket_name:
                return item.name

