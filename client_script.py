from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import requests


TMP_FOLDER = '/var/tmp/bqb/'


def img2clipboard(img_id):
    resp = requests.get("http://127.0.0.1:8009/get_file/"+img_id, stream=True)
    if resp.status_code == 200:
        filename = img_id + '.' + resp.headers.get('Content-Type').split('/')[1]
        with open(os.path.join(TMP_FOLDER, filename), 'wb') as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
        write2clipboard('file://'+TMP_FOLDER+filename)


def write2clipboard(local_file_url):
    app = QApplication([])
    clipboard = app.clipboard()
    mine_data = QMimeData()
    mine_data.setUrls([QUrl(local_file_url)])
    clipboard.setMimeData(mine_data)
    # sys.exit(app.exec())


if __name__ == '__main__':
    os.makedirs(TMP_FOLDER, exist_ok=True)
    img2clipboard('e06ad7dea1e611e7b8dc784f438bc4be')
    # write2clipboard('file:///Users/dd/PycharmProjects/bqb_web/imgs/e069b692a1e611e78bee784f438bc4be.gif')
