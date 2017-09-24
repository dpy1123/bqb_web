### api doc
#### /uploads
Method: post  
Content-type: form-data  
response
```json
{
    "data": {
        "file_saved": [],
        "file_unsaved": [
            {
                "filename": "52520072_p0.png",
                "similar_imgs": [
                    {
                        "_id": "0ed81230a0ef11e7bbb5d050992c396a",
                        "create_time": "Sun, 24 Sep 2017 06:10:14 GMT",
                        "d_hash": "73e9f1c163737369",
                        "original_name": "52520072_p0.png",
                        "suffix": ".png",
                        "tags": "test, ok",
                        "url": "/get_file/0ed81230a0ef11e7bbb5d050992c396a"
                    }
                ]
            },
            {
                "filename": "bk.jpg",
                "similar_imgs": [
                    {
                        "_id": "0edd6b18a0ef11e7aa28d050992c396a",
                        "create_time": "Sun, 24 Sep 2017 06:10:14 GMT",
                        "d_hash": "0c4c4e4d47169633",
                        "original_name": "bk.jpg",
                        "suffix": ".jpg",
                        "tags": "",
                        "url": "/get_file/0edd6b18a0ef11e7aa28d050992c396a"
                    }
                ]
            }
        ]
    },
    "msg": "ok"
}
```
#### /imgs
Method: get  
query:

|query_param |  value    |  必填  |
| :--------: | :-----:   | :----: |
| q          | test      |   否    |
| p          | 0         |   否    |
| size       | 10        |   否    |

response
```json
{
    "data": {
        "list": [
            {
                "_id": "0ed81230a0ef11e7bbb5d050992c396a",
                "create_time": "Sun, 24 Sep 2017 06:10:14 GMT",
                "d_hash": "73e9f1c163737369",
                "original_name": "52520072_p0.png",
                "suffix": ".png",
                "tags": "test, ok",
                "url": "/get_file/0ed81230a0ef11e7bbb5d050992c396a"
            }
        ],
        "total": 1
    },
    "msg": "ok"
}
```
#### /imgs/<img_id>
Method: get  
response
```json
{
    "data": {
        "_id": "0ed81230a0ef11e7bbb5d050992c396a",
        "create_time": "Sun, 24 Sep 2017 06:10:14 GMT",
        "d_hash": "73e9f1c163737369",
        "original_name": "52520072_p0.png",
        "suffix": ".png",
        "tags": "test, ok",
        "url": "/get_file/0ed81230a0ef11e7bbb5d050992c396a"
    },
    "msg": "ok"
}
```

#### /imgs/<img_id>
Method: post  
request body:
```json
{
    "tags": ["test", "ok"]
}
```
response
```json
{
    "msg": "ok"
}
```
#### /get_file/<img_id>
Method: get  

