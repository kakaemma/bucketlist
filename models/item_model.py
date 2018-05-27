import datetime
items = []


class BucketItems(object):

    def __init__(self, user_id, bucket_id, name, status):
        self.id = len(items)+1
        self.user_id = user_id
        self.name = name
        self.status = status
        self.date = datetime.datetime.utcnow()
        self.bucket_id = bucket_id

    def add_item(self):
        items.append(self)

    def update_item(cls, bucket_id, item_id, new_name, new_status):
        for each_item in items:
            if each_item.bucket_id == bucket_id and each_item.id == item_id:
                each_item.name = new_name
                each_item.status = new_status
                return each_item.id

    def delete_item(cls, item_id):
        for this_item in items:
            if this_item.id == item_id:
                items.remove(this_item)
