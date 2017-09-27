import os
import uuid
from io import BytesIO
from PIL import Image
import imagehash
from flask import Flask, request, make_response, jsonify, url_for, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from db import DB


ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg', 'gif'])
# FS_ROOT = 'E:\\PycharmProjects\\bqb_web\\imgs'
FS_ROOT = '/Users/dd/PycharmProjects/bqb_web/imgs'
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 10 # 16m * 10
# db = DB('mongodb://localhost:27017/', 'bqb')
db = DB('mongodb://172.16.6.218:27017/', 'bqb')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_suffix(filename):
    return os.path.splitext(filename)[1].lower()


def save_file(save_path, img_buf):
    with open(save_path, 'wb+') as fw:
        fw.write(img_buf.getvalue())
        fw.flush()


def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route("/uploads", methods=['GET', 'POST'])
def uploads():
    if request.method == 'POST':
        file_saved = []
        file_unsaved = []
        for _, file in request.files.to_dict().items():
            if file.filename == '':
                print('No selected file')
                return make_response(jsonify({'msg': '喵喵喵？'}), 400)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                with BytesIO(file.stream.read()) as img_buf:
                    d_hash = str(imagehash.dhash(Image.open(img_buf)))  # gif 按第一帧处理
                    similar_imgs = db.find_imgs_by_dhash(d_hash)
                    if len(similar_imgs) == 0:  # 新图
                        suffix = get_file_suffix(filename)
                        file_name = str(uuid.uuid1()).replace("-", "") + suffix
                        save_path = os.path.join(FS_ROOT, file_name)
                        save_file(save_path, img_buf)
                        db.save_img(filename, save_path, d_hash, suffix)
                        file_saved.append({'filename': filename})
                    else:  # 旧图
                        file_unsaved.append({'filename': filename, 'similar_imgs': [build_img_vo(img) for img in similar_imgs]})
        return make_response(jsonify({'msg': 'ok', 'data': {'file_saved': file_saved, 'file_unsaved': file_unsaved}}), 200)
    else:
        return make_response(jsonify({'msg': '喵喵喵？'}), 405)


@app.route("/imgs")
def list_imgs():
    page_no = int(request.args.get('p', 0))
    page_size = int(request.args.get('size', 10))
    query = request.args.get('q', '')
    total, imgs = db.query_img(query, page_no, page_size)
    return make_response(jsonify({'msg': 'ok', 'data': {'total': total, 'list': [build_img_vo(img) for img in imgs]}}), 200)


@app.route('/get_file/<file_id>')
def get_file(file_id):
    data = db.find_img_by_id(file_id)
    return send_file(data['save_path'], conditional=True)


def build_img_vo(data):
    data['tags'] = ', '.join([tag['name'] for tag in db.find_tags_by_img_id(data['_id'])])
    data['url'] = url_for('get_file', file_id=data['_id'])
    del data['save_path']
    return data


@app.route("/imgs/<img_id>", methods=['GET', 'POST'])
def get_img(img_id):
    if request.method == 'POST':
        req_body = request.get_json(force=True)
        tags = req_body['tags']
        db.update_img_tags(img_id, tags)
        return make_response(jsonify({'msg': 'ok'}), 200)
    else:
        data = db.find_img_by_id(img_id)
        return make_response(jsonify({'msg': 'ok', 'data': build_img_vo(data)}), 200)


@app.route("/")
def index():
    return "home page"


if __name__ == "__main__":
    app.run(port=8009)
