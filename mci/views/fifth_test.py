from flask import Blueprint, render_template
import sqlite3

bp = Blueprint('fifth', __name__, url_prefix='/')

# 5th test
import base64
import requests
from time import sleep
import urllib3
import json
import os, pyscreenshot, random, string
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import easyocr

@bp.route('/pygame')
def pygame():
    return render_template('5th_test.html')

@bp.route('/get_screenshot', methods=['POST'])
def get_screenshot():
    
    # 기억력 게임 점수에 대한 함수 정의 
    def get_score(level) :
        if level == 1:
            score = 0
        elif level == 2:
            score = 1
        elif 3 <= level <= 4:
            score = 2
        elif level == 5:
            score = 3
        else:
            score = 4
            
        return level, score

    # 기억력 게임을 완료한 이후 easyocr을 이용해 게임결과 이미지에서 텍스트추출
    im = pyscreenshot.grab()
    random_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    file_name = 'mci/static/5/img/{}.png'.format(random_id)
    im.save(file_name)
    reader = easyocr.Reader(['ko', 'en'])
    
    with open(file_name,'rb') as pf:
        img = pf.read()
        result = reader.readtext(img)
        for res in result:
            if res[1][0:10] == 'Your level':    
                level = res[1][-1]
                result = get_score(int(level))
    
    # 텍스트로 추출한 결과를 DB에 저장
    conn = sqlite3.connect('mci/ijm.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS remember (level TEXT, score TEXT)""")
    cursor.execute("""INSERT INTO remember(level, score) 
                    VALUES(?, ?)""", (result[0], result[1]))
    conn.commit()
    cursor.close()
    os.remove(file_name)