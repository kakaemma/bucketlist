import datetime
bucket = []


class BucketModal(object):
    """
    This class handle all model operations on th bucket
    """
    def __init__(self, name, desc):
        """
        This Constructor initialises all the parameter required
        :param name: 
        :param desc: 
        """
        self.id = len(bucket)+1
        self.name = name
        self.desc = desc
        self.date = datetime.datetime.utcnow()
        self.modify_date = None

    #-----------------------------------------------------------------------

    def create_bucket(self):
        """ 
        This methods adds the bucket 
        """
        bucket.append(self)

    #-----------------------------------------------------------------------

    @staticmethod
    def get_buckets():
        """ 
        This method gets all the buckets
        """
        response = []
        for each_bucket in bucket:
            response.append({'id': each_bucket.id,
                             'name': each_bucket.name,
                             'description': each_bucket.desc,
                             'date_created': each_bucket.date,
                             'date_modified': each_bucket.modify_date
                             })
            return response

    #-----------------------------------------------------------------------

    @staticmethod
    def get_bucket(bucket_id):
        """
        This method gets a specific bucket using the id
        :param bucket_id: 
        :return: 
        """
        response = []
        for this_bucket in bucket:
            if this_bucket.id == bucket_id:
                response.append({'id': this_bucket.id,
                                 'name': this_bucket.name,
                                 'description': this_bucket.desc,
                                 'date_created': this_bucket.date,
                                 'date modified': this_bucket.modify_date
                                 })
                return response
            return None

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
        for this_bucket in bucket:
            if this_bucket.id == modify_id:
                this_bucket.name = name
                this_bucket.desc = desc
                this_bucket.modify_date = datetime.datetime.utcnow()
                return this_bucket.id
            return None
    #-----------------------------------------------------------------------

    def delete_bucket(cls, del_id):
        """
        This method deletes a bucket from the system
        :param del_id: 
        :return: 
        """
        for this_bucket in bucket:
            if this_bucket.id == del_id:
                bucket.remove(this_bucket)