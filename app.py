from flask import Flask, render_template, request, flash, g, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import sqlite3 as sql
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #tensorflow warning 끄는 용
import ssl

# 1st test
import keras.applications as kapp
import keras.preprocessing.image as kimage
import keras.models as kmodels
import numpy as np
import keras.utils as utils
from anchor import *
import PIL

# 3rd test
import pandas
import torch
import sqlite3

# 4th test
import random

# 5th test
import base64
import requests
from time import sleep
import urllib3
import json
import os, pyscreenshot, random, string
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import easyocr

# 6st test


 # flask name 선언
app = Flask(__name__)



# HTML 렌더링
################### 홈페이지 ###################
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/intro')
def intro():
    return render_template('0_intro.html')


################### 1번째 게임 : 유사도게임 ###################
vgg_model = kapp.VGG16(weights='imagenet', include_top=False)
model = kmodels.Model(inputs=vgg_model.input, outputs=vgg_model.get_layer('block5_pool').output)
anch = ''

# img_path: 
def get_image_feature(image):
    img = utils.load_img(image, target_size=(224, 224))
    img = utils.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = kapp.vgg16.preprocess_input(img)
    features = model.predict(img)
    features = features.flatten()
    return features

@app.route("/vgg")
def similarity_image():
    q, p_path, h_path, sim = random_sim()
    global anch
    anch = q
    print(anch)
    return render_template('1st_test.html', h_path=h_path)


@app.route("/image_similarity", methods=["POST"])
def image_similarity():
 
    print('1111111111111111')
    # 이미지 받기(blob)
    if request.method == 'POST':
        image = request.files["image"]
        # Save image_binary to a file or a variable
        image.save('유사도image.png')
        image = '유사도image.png'
        print('222222222222222222')
        global anch
        print(anch)
        global anchor
        p_path = anchor[anch][0]
        sim = anchor[anch][2]


    print('333333333333333')
    

    features1 = get_image_feature(p_path)
    features2 = get_image_feature(image)
    print('44444444444444')
    cosine_similarity = np.dot(features1, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))
    print(cosine_similarity)
    print(sim)
   
    # db 저장하기
    OX = []
    if cosine_similarity >= sim:
        OX.append('정답')
    else: OX.append('오답') 
    print(OX)
   

    # DB 생성 / 이미 있으면 나중에 주석처리하기.
    # isolation_level = None (auto commit)
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    # 커서
    cursor = conn.cursor()
    # 테이블 생성(데이터 타입 = TEST, NUMERIC, INTEGER, REAL, BLOB(image) 등)
    # 필드명(ex. name) -> 데이터 타입(ex. text) 순서로 입력 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sim (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        game text,
        point float,
        OX text)""")

    # db 에 정보 저장
    game = '유사도 검사'
    point = float(cosine_similarity)
    OX = OX[0]

    cursor.execute("""
        INSERT INTO sim (game, point, OX) VALUES (?,?,?)          
        """, (game, point, OX)
        )

    conn.commit()
    cursor.close()
    conn.close()    
    return render_template('2nd_test.html')


################### 2번째 게임 : 스트루프 ###################
@app.route('/stroop', methods=['GET', 'POST']) ## 여기에 들어가야하는거 넣어주세요~!!!1 지영
def stroop():
    return render_template('2nd_test.html')

OX = []

@app.route("/save",methods=['POST']) #flask 웹 페이지 경로
def save(): # 경로에서 실행될 기능 선언
    correct = []
    my_correct=[]
    global OX
    result = request.form['result']
    correct.append(result[0:2])  # 문자열 슬라이싱해서 들고와야한다. 
    my_correct.append(result[3:5])
    OX.append(result[6:8])

    # # 확인용
    # check = request.form['check']
    # print(check)
    
    # DB 생성 / 이미 있으면 나중에 주석처리하기.
    # isolation_level = None (auto commit)
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    # 커서
    cursor = conn.cursor()
    # 테이블 생성(데이터 타입 = TEST, NUMERIC, INTEGER, REAL, BLOB(image) 등)
    # 필드명(ex. name) -> 데이터 타입(ex. text) 순서로 입력 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stroop (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        game text,
        correct text,
        my_correct text,
        OX text)""")

    # db 에 정보 저장
    game = '스트루프'
    correct = correct[0]
    my_correct = my_correct[0]
    OX = OX[0]
    print('111111111')
    cursor.execute("""
        INSERT INTO stroop (game, correct,my_correct, OX) VALUES (?,?,?,?)          
        """, (game, correct,my_correct, OX)
        )
    print('222222222')

    conn.commit()
    cursor.close()
    conn.close()    
    return render_template('2nd_test.html')

################### 3번째 게임 : 글->그림 ###################
@app.route('/text_to_img')
def text_to_img():
    return render_template('3rd_test.html')

yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'best.pt', force_reload =True)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    print('1111111111111111')
    # 이미지 받기(blob)
    if request.method == 'POST':
        image = request.files["image"]
        # Save image_binary to a file or a variable
        image.save('image.png')



    # with open("image.png", "wb") as f:
    #     f.write(image)
    
    print('22222222222222')
    
    # e=open('Base64_dec.png','wb') 
    # e.write(image_binary)
    # e.save(image_binary)
    # e.close()
    
    
    
    # Model(YOLOv5 종속 항목 설치)

    # Image
    print('asdadasdasdasdas')
    img = PIL.Image.open('image.png')
    print('ㅁㄴㅇㅁㄴㅇㅁㄴㅇㅁㅁㄴㅇㅁㄴㅇㅁㄴㅇ')
    ########## 이 사진을 어떻게 가지고 올지에 대해서 알아봐야한다. !!
    global yolo_model
    # 추론
    results = yolo_model(img)


    # 결과
    #results.print()
    #results.show()
    #results.save() # Save image to 'runs\detect\exp'
    #results.xyxy[0]  # 예측 (tensor)
    # results.pandas().xyxy[0]  # 예측 (pandas)
    conf = results.pandas().xyxy[0]
    print(conf)
   
    # 오답 여부
    OX = []
    if conf.name[0] == 'rabbit':
        OX.append('정답')
    else : OX.append('오답')
    print(OX)
    

    # DB 생성 / 이미 있으면 나중에 주석처리하기.
    # isolation_level = None (auto commit)
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    # 커서
    cursor = conn.cursor()
    # 테이블 생성(데이터 타입 = TEST, NUMERIC, INTEGER, REAL, BLOB(image) 등)
    # 필드명(ex. name) -> 데이터 타입(ex. text) 순서로 입력 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS text_write (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        game text,
        point float,
        OX text)""")

    # db 에 정보 저장
    game = '글->그림'
    point = float(conf.confidence)
    OX = OX[0]

    cursor.execute("""
        INSERT INTO text_write (game, point, OX) VALUES (?,?,?)          
        """, (game, point, OX)
        )

    conn.commit()
    cursor.close()
    conn.close()    
    return render_template('3rd_test.html')

################ 4번째게임 : 틀린그림찾기 ###############

@app.route('/find_diff')
def find_diff():
    return render_template('4th_test.html')

#globla 변수
count = 0
test_class = ['나비','지렁이','컴퓨터']
# 밑에 next를 안 넣고 count>=3 을 하면 오류남 (인덱스 에러)/ 왜인진 모르겠지만 맨 마지막 인덱스는 안 나온다.-># 해결 
wrong_ox = list() #db 저장용 
# html 렌더링
@app.route('/wrong_img',  methods=['POST','GET'])
def wrong_img():
    # OX list에 결과값 저장
    global wrong_ox
    if request.method == 'POST':
        image = str(request.form['button'])
        if 'X' in image:
            wrong_ox.append('정답')
        else: wrong_ox.append('오답')
    # 이미지 불러오기
    global count
    global test_class
    if len(test_class) == 0:
        test_class.append('나비')
        test_class.append('지렁이')
        test_class.append('컴퓨터')
    if count >=3 :
        count = 0 # 전역변수 횟수 0으로 바꿔주기
        return redirect(url_for('end')) # redirect를 할때는 route 옆에 오는 글자를 넣어줘야함(함수이름이 아님) 
    
    else:
        # 변수에 이미지 이름 넣기
        random.shuffle(test_class)
        img1 =test_class[0] + '1'
        img2=test_class[0] + '2'
        img3= test_class[0] + '3'
        img4= test_class[0] + 'X'
        # 랜덤으로 텍스트 보내기
        random_class =[img1,img2,img3,img4 ]
        random.shuffle(random_class)
        img1 = random_class[0]
        img2 = random_class[1]
        img3 = random_class[2]
        img4 = random_class[3]
        
        # 처음엔 for문으로 작성하려고 했으나 렌더링 될 때는 마지막 것만 되기 때문에 필요가 없음    
        # for i in test_class :   
        #     # str = test_class[i]    
        #     random_list = [i+'1', i+'2',i+'3',i+'X']
        #     random_list_2 = []
        #     random.shuffle(random_list)
        #     for  j in random_list:
        #         random_list_2.append(j)
        #     img1 = random_list_2[0]
        #     img2 = random_list_2[1]
        #     img3 = random_list_2[2]
        #     img4 = random_list_2[3]
            
        # 누른 버튼의 text 를 받아서 정답인지 오답인지 판별하기
        
        test_class.remove(test_class[0]) #  사용한 str 은 삭제해서 test_class 가 중복이 안되게 함.
        count += 1
        return render_template('4th_test.html',img1 = img1, img2=img2,img3=img3,img4=img4) 
   

@app.route('/end',  methods=['POST','GET'])
def end():
    # DB 저장 
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    # 커서
    cursor = conn.cursor()
    # 테이블 생성(데이터 타입 = TEST, NUMERIC, INTEGER, REAL, BLOB(image) 등)
    # 필드명(ex. name) -> 데이터 타입(ex. text) 순서로 입력 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wrong_test (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        game text,
        OX1 text,
        OX2 text,
        OX3 text)""")
    
    # db 에 정보 저장
    game = '틀린그림찾기'
    OX1 = wrong_ox[0]
    OX2 = wrong_ox[1]
    OX3 = wrong_ox[2]
    
    cursor.execute("""
        INSERT INTO wrong_test (game, OX1,OX2,OX3) VALUES (?,?,?,?)          
        """, (game, OX1,OX2,OX3)
        )
    conn.commit()
    cursor.close()
    conn.close() 
    return render_template('4-2_test.html')
    


################### 5번째 게임 : 파이게임(기억력) ###################

@app.route('/pygame')
def pygame():
    return render_template('5th_test.html')

@app.route('/get_screenshot', methods=['POST'])
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
    file_name = 'static/5/img/{}.png'.format(random_id)
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
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS remember (level TEXT, score TEXT)""")
    cursor.execute("""INSERT INTO remember(level, score) 
                    VALUES(?, ?)""", (result[0], result[1]))
    conn.commit()
    cursor.close()
    os.remove(file_name)
    


################### 6번째 게임 : STT ###################


DATABASE_URI = 'sttdb.db'

conn = sql.connect(DATABASE_URI, isolation_level=None)
cur = conn.cursor()

cur.execute("SELECT target FROM STT")
db_text = str(cur.fetchmany(size=1))

# 경로와 정답Text만 추출하기 위한 처리
db_List = db_text.split("'")

global sound_target
sound_target = db_List[1] # 정답Text
print(sound_target)

dic = {'1' : sound_target} # 정답 Text


@app.route('/sound')
def sound():
    return render_template('6th_test.html', target=dic['1'])

@app.route('/STT', methods=['POST', 'GET'])
def STT():
    print('1111111111111111111111')
    String_sound = ''  # 녹음파일 Text
    print('22222222222222222222')
    String_target = '' # 정답 Text
    print('333333333333333333')
    sleep(5)
    count = 1
    print('4444444444444444')
    
    #---------------------------------------------------------------------------
    #      STT Open API
    #---------------------------------------------------------------------------
    print('여기까지는 되는거?')
    if request.method == 'POST':
        openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
        print('5555555')
        accessKey = "f0f9fd15-daef-4655-b516-d7a9711c696a" 
        print('6666666')
        audioFilePath = request.files['recode'] # 다운로드한 음성파일을 여기에 넣어서 Text로 바꾸기

        print('777777777')
        # audioFilePath.save('녹음파일.wav')
        print('888888888')
        languageCode = "korean"
        print('999999999999')
        #file = open('nefile', "rb")
        #audioContents= wavfile.read("녹음파일.wav") ## !!
        #print(audioContents)
        #audio_binary = tf.io.read_file(audioFilePath)
        # audioFile = request.files['recode']
        data = audioFilePath.read()
        audioContents = base64.b64encode(data).decode("utf8")
        # inMemoryFile = BytesIO(audioContents)


        print('ㄱㄱㄱㄱㄱㄱㄱㄱㄱㄱ')
        #audioContents = base64.b64encode(file.read()).decode("utf8")
        # audioContents = base64.b64encode(inMemoryFile.getvalue()).decode("utf8")
        print('ㄴㄴㄴㄴㄴㄴ')
        #file.close()
        
        requestJson = {    
            "argument": {
                "language_code": languageCode,
                "audio": audioContents
            }
        }
        
        http = urllib3.PoolManager()
        response = http.request(
        "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
            body=json.dumps(requestJson)
        )
        
        print("[responseCode] " + str(response.status))
        print("[responBody]")
        print("===== 결과 확인 ====")

        # 출력결과는 쓸때없는 내용이 들어가기 때문에 필요한 부분만 가져오기
        string = str(response.data,"utf-8")
        List = string.split('"')
        List = List[-2]
        List = List[:-1]
        print(List)
        # 녹음한 음성을 처리한 결과를 List변수에 담는다.
        
        
        # dic = {'1' : "안녕하세요. 오늘도 멋진 하루 되세요"}
        
        
        # NLP 유사도검사를 위해 정답Text와 녹음하고 Text로 바꾼 결과를 변수에 담에서 NLP모델에 넘긴다.
        # 녹음파일 Text
        String_sound = List
        
        # 정답Text
        String_target = sound_target
        
        
        
        #---------------------------------------------------------------------------
        #       유사도 검사 NLP Open API
        #---------------------------------------------------------------------------
        
        openApiURL = "http://aiopen.etri.re.kr:8000/ParaphraseQA"
        accessKey = "f0f9fd15-daef-4655-b516-d7a9711c696a"
        sentence1 = String_sound
        sentence2 = String_target
        
        requestJson = {
        "argument": {
            "sentence1": sentence1,
            "sentence2": sentence2
            }
        }
        
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8","Authorization" :  accessKey},
            body=json.dumps(requestJson)
        )
        
        print("[responseCode] " + str(response.status))
        print("[responBody]")
        print(str(response.data,"utf-8"))

        NLP_String = str(response.data,"utf-8")
        NLP_List = NLP_String.split('"')
        print(NLP_List)
        
        NLP_reuslt = NLP_List[-2]
        # NLP_reuslt = NLP_target[:-1]
        print(NLP_reuslt)
        
        #--------------------------------------------------------------------------
        #     검증 결과 추출 및 전송
        #--------------------------------------------------------------------------
        
        String = ''
        Score = 0
        if NLP_reuslt == 'paraphrase' :
            String += 'O'
            Score = 1
        else:
            String += 'X'
            
        # os.remove(audioFilePath)
        print(sentence2)
        print(sentence1)
        print(String)
        
        conn = sql.connect(DATABASE_URI, isolation_level=None)
        cur = conn.cursor()

        cur.execute("UPDATE STT SET user_sound = '%s' WHERE id = '%s'" %(sentence1, 1))
        cur.execute("UPDATE STT SET ck = '%s' WHERE id = '%s'" %(String, 1))
        cur.execute("UPDATE STT SET score = '%s' WHERE id = '%s'" %(Score, 1))
        
        conn.commit()
        cur.close()
        
        #-----------------------------------------------------------------------------
        
        conn = sql.connect(DATABASE_URI, isolation_level=None)
        cur = conn.cursor()
                
        cur.execute("SELECT * FROM STT")
        STT_Data = str(cur.fetchmany(size=1))
        STT_Data = STT_Data.split("'")
        cur.close()
        
        stt_id = STT_Data[1]
        stt_target = STT_Data[3]
        stt_user_sound = STT_Data[5]
        stt_ck = STT_Data[7]
        stt_score = STT_Data[9]
        
        #                                             정답문장          TTS        체크 결과
    # return render_template('6th_test.html', target = sentence2, sound = sentence1, ck=String)
    return jsonify({'sound':sentence2})



################## 결과페이지 : 대시보드 ###################

@app.route('/result')
def result():
    return render_template('dashboardd.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/abouttest')
def abouttest():
    return render_template('abouttest.html')




if __name__ == '__main__':
    # https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.run
    # https://snacky.tistory.com/9
     # host주소와 port number 선언
    app.run(host='0.0.0.0', debug=True)  
    