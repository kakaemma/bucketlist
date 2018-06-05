import datetime


class BucketItems(object):
    """
    This class handles all models operations for the Bucket items
    """
    items = []

    def __init__(self, user_id, bucket_id, name, status):
        """
        Initialises all parameters required to create an item
        :param user_id: 
        :param bucket_id: 
        :param name: 
        :param status: 
        """
        self.id = len(BucketItems.items)+1
        self.user_id = user_id
        self.name = name
        self.status = status
        self.date = datetime.datetime.utcnow()
        self.bucket_id = bucket_id

    #-----------------------------------------------------------------------

    def add_item(self):
        """ 
        This adds an item to the model
        """
        BucketItems.items.append(self)

    #-----------------------------------------------------------------------

    def update_item(cls, bucket_id, item_id, new_name, new_status):
        """
        This method updates an item
        :param bucket_id: 
        :param item_id: 
        :param new_name: 
        :param new_status: 
        :return: 
        """
        for each_item in BucketItems.items:
            if each_item.bucket_id == bucket_id and each_item.id == item_id:
                each_item.name = new_name
                each_item.status = new_status
                return each_item.id

    #-----------------------------------------------------------------------

    def delete_item(cls, item_id):
        """
        This method deletes an item
        :param item_id: 
        :return: 
        """
        for this_item in BucketItems.items:
            if this_item.id == item_id:
                BucketItems.items.remove(this_item)

    #-----------------------------------------------------------------------

    @classmethod
    def check_item_with_id(cls,item_id):
        for this_item in BucketItems.items:
            if this_item.id == item_id:
                return item_id
