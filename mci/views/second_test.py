from flask import Blueprint, render_template, request, session
import sqlite3

bp = Blueprint('second', __name__, url_prefix='/')

@bp.route('/stroop', methods=['GET', 'POST']) ## 여기에 들어가야하는거 넣어주세요~!!!1 지영
def stroop():
    return render_template('2nd_test.html')

OX = []

@bp.route("/save",methods=['POST']) #flask 웹 페이지 경로
def save(): # 경로에서 실행될 기능 선언
    correct = []
    my_correct=[]
    global OX
    print(type(OX))
    print(OX)
    result = request.form['result']
    correct.append(result[0:2])  # 문자열 슬라이싱해서 들고와야한다. 
    my_correct.append(result[3:5])
    OX.append(result[6:8])

    # # 확인용
    # check = request.form['check']
    # print(check)
    if len(OX) >= 8:
    # DB 생성 / 이미 있으면 나중에 주석처리하기.
    # isolation_level = None (auto commit)
        conn = sqlite3.connect('mci/ijm.db', isolation_level=None)
        # 커서
        cursor = conn.cursor()
        # 테이블 생성(데이터 타입 = TEST, NUMERIC, INTEGER, REAL, BLOB(image) 등)
        # 필드명(ex. name) -> 데이터 타입(ex. text) 순서로 입력 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stroop (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            game text,
            OX1 text,
            OX2 text,
            OX3 text,
            OX4 text,
            OX5 text,
            OX6 text,
            OX7 text,
            OX8 text,
            session integer)""")
    
    # db 에 정보 저장
        game = '스트루프'
        correct = correct[0]
        my_correct = my_correct[0]
        guest = session['guest']
        print('111111111')
        cursor.execute("""
            INSERT INTO stroop (game, OX1, OX2, OX3, OX4, OX5, OX6, OX7, OX8, session) VALUES (?,?,?,?,?,?,?,?,?,?)          
            """, (game, OX[0], OX[1], OX[2], OX[3], OX[4], OX[5], OX[6], OX[7], guest)
            )
        # cursor.execute("""
        #     INSERT INTO stroop (game, correct,my_correct, OX1, OX2, OX3, OX4, OX5, OX6, OX7, OX8) VALUES (?,?,?,?)          
        #     """, (game, correct,my_correct, OX[0], OX[1], OX[2], OX[3], OX[4], OX[5], OX[6], OX[7])
        #     )
        print('222222222')

        conn.commit()
        cursor.close()
        conn.close()
        OX = []
        return render_template('3rd_test.html')
    return render_template('2nd_test.html')