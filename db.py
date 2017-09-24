import datetime
import uuid
from pymongo import MongoClient


class DB:
    def __init__(self, mongo_url, db_name):
        client = MongoClient(mongo_url)
        self.db = client[db_name]
        self.img = self.db['img']
        self.tag = self.db['tag']
        self.img_tag = self.db['img_tag']

    @staticmethod
    def uuid():
        return str(uuid.uuid1()).replace("-", "")

    def find_img_by_id(self, id):
        return self.img.find_one({'_id': id})

    def find_imgs_by_dhash(self, d_hash):
        return list(self.img.find({'d_hash': d_hash}))

    def save_img(self, original_name, save_path, d_hash, suffix, create_time=datetime.datetime.utcnow()):
        return self.img.insert_one({'_id': DB.uuid(), 'original_name': original_name, 'save_path': save_path,
                                    'd_hash': d_hash, 'suffix': suffix, 'create_time': create_time}).inserted_id

    def save_tag(self, tag_name, create_time=datetime.datetime.utcnow()):
        return self.tag.insert_one({'_id': DB.uuid(), 'name': tag_name, 'create_time': create_time}).inserted_id

    def save_img_tag(self, img_id, tag_id, create_time=datetime.datetime.utcnow()):
        return self.img_tag.insert_one({'_id': DB.uuid(), 'img_id': img_id, 'tag_id': tag_id, 'create_time': create_time}).inserted_id

    def find_tag_by_name(self, tag_name):
        return self.tag.find_one({'name': tag_name})

    def update_img_tags(self, img_id, tags):
        new_tag_ids = []
        for t in tags:
            tag = self.find_tag_by_name(t)
            if tag is None:
                new_tag_ids.append(self.save_tag(t))
            else:
                new_tag_ids.append(tag['_id'])

        self.img_tag.delete_many({'img_id': img_id})
        return [self.save_img_tag(img_id, t_id) for t_id in new_tag_ids]

    def find_tags_by_img_id(self, img_id):
        tag_ids = [img_tag['tag_id'] for img_tag in list(self.img_tag.find({'img_id': img_id}))]
        tags = list(self.tag.find({'_id': {'$in': tag_ids}}))
        return tags

    def query_img(self, query, page_no, page_size):
        if query == '':
            return self.img.count({}), self.img.find({}).skip(page_no*page_size).limit(page_size)
        else:
            tag_ids = [tag['_id'] for tag in list(self.tag.find({'name': {'$regex': query}}))]
            img_ids = [img_tag['img_id'] for img_tag in self.img_tag.find({'tag_id': {'$in': tag_ids}})]
            return self.img.count({'_id': {'$in': img_ids}}), self.img.find({'_id': {'$in': img_ids}}).skip(page_no * page_size).limit(page_size)


if __name__ == "__main__":
    db = DB('mongodb://localhost:27017/', 'bqb')
