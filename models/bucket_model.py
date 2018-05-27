import datetime
bucket =[]


class BucketModal(object):
    def __init__(self, name, desc):
        self.id = len(bucket)+1
        self.name = name
        self.desc = desc
        self.date = datetime.datetime.utcnow()
        self.modify_date = None

    def create_bucket(self):
        bucket.append(self)

    def get_buckets(cls):
        response =[]
        for each_bucket in bucket:
            response.append({'id': each_bucket.id,
                             'name': each_bucket.name,
                             'description': each_bucket.desc,
                             'date_created': each_bucket.date,
                             'date_modified':each_bucket.modify_date
                             })
            return response

    def get_bucket(cls,bucket_id):
        response = []
        for this_bucket in bucket:
            if this_bucket.id == bucket_id:
                response.append({'id': this_bucket.id,
                                 'name':this_bucket.name,
                                 'description':this_bucket.desc,
                                 'date_created': this_bucket.date,
                                 'date modified': this_bucket.modify_date
                                 })
                return response
            return None


    def modify_bucket(cls, modify_id, name, desc):
        for this_bucket in bucket:
            if this_bucket.id == modify_id:
                this_bucket.name = name
                this_bucket.desc = desc
                this_bucket.modify_date = datetime.datetime.utcnow()
                return this_bucket.id
            return None


    def delete_bucket(cls, del_id):
        for this_bucket in bucket:
            if this_bucket.id == del_id:
                bucket.remove(this_bucket)







