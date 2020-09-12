debug=False
from flask import Flask, render_template ,abort,request,session,make_response
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import numpy as np
import cv2
import base64
import os
import json
import io
import time
import random,string
from backend.face import FaceRecognition,FaceMosaicAction
from azure_storage import cos5year_storage
from backend.Text import TextRecognize
from backend.util import DrawBOXes,DrawBOXes2
from faceAPI import cos5year_face
import backend.mosaic

import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
api = Api(app)
log_file_path = 'log/'
handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)
if(not debug):
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='NONE',
    )
app.config['SECRET_KEY']='Cos5year'

sessions =[]
class Test(Resource):
    def get(self):
       return 'Hello World'

class Json(Resource):#Resourceクラスを継承した新たなクラスを生成
    def get(self):#GET,POST,PUT,DELETEなど色々使える
        json = {'name':"Cos5Year",'id':-1}
        return json ##jsonも返せる
    def post(self):
        return None
    def put(self):
        return None
    def delete(self):
        return None

class Mosaic(Resource):
    def get(self):
        return None
    def post(self):
        return None

class Upload(Resource):
    def post(self):
        #try:
            timedate = time.time()
            session["sessionId"]= "".join(random.choices(string.ascii_letters + string.digits,k=8))
            sessions.append(session["sessionId"])
            json = request.json
            session['extent'] = json['extent']
            session['name'] = json['name']

            dec_data = base64.b64decode( json['image'].split(',')[1])
            # イメージの圧縮
            ##fastモードのときにやるようにしています.どっちやればいいかわからんけど
            if json['fastmode'] == True:
                img_array_before = np.frombuffer(dec_data, dtype=np.uint8)
                img_before = cv2.imdecode(img_array_before, cv2.IMREAD_ANYCOLOR)
                height,width,d = img_before.shape
                thr_value = 1000 # 画像サイズの閾値
                if height > thr_value or width > thr_value:
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30] # この４０の値を変更することで制度を変更可能
                    result, encimg = cv2.imencode('.'+json['extent'], img_before, encode_param)
                    decimg = cv2.imdecode(encimg, 3)
                    dec_data = cv2.imencode("."+json['extent'], decimg)[1].tostring()
                    print('圧縮後',time.time()-timedate)
            # イメージのリサイズ
            if json['fastmode'] == True: # 画像サイズの縮小を行う時
                img_array_before = np.frombuffer(dec_data, dtype=np.uint8)
                img_before = cv2.imdecode(img_array_before, cv2.IMREAD_ANYCOLOR)
                height,width,d = img_before.shape
                thr_value = 500 # 画像サイズの閾値
                if height > thr_value or width > thr_value:
                    if height >= width:
                        resize_rate = thr_value/height
                        height_resize = thr_value
                        width_resize = width * resize_rate
                    else:
                        resize_rate = thr_value/width
                        width_resize = thr_value
                        height_resize = height * resize_rate
                    img_after = cv2.resize(img_before,(int(width_resize),int(height_resize)))
                    dec_data = cv2.imencode("."+json['extent'], img_after)[1].tostring()
                    #print(type(dec_data),height_resize,width_resize)
                    print('サイズ変換後',time.time()-timedate)

            boxes_list = {'face':[],'text':[]}
            with  cos5year_storage() as st:
                st.UploadOriginal(session["sessionId"],json['name'],json['extent'],io.BytesIO(dec_data))
                img_array = np.fromstring(dec_data, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_ANYCOLOR)
                #print(type(img_array),type(img))
                print('アップロード',time.time()-timedate)
                if(json['face']==True):
                    boxes = FaceRecognition(img)
                    boxes_list['face']=boxes
                    img = DrawBOXes2(img,boxes,(0,0,255))
                if(json['text']==True):
                    boxes = TextRecognize(img,st.URLofOriginal(session['sessionId'],json['extent']))
                    boxes_list['text']=boxes
                    img = DrawBOXes2(img,boxes,(0,0,255))
                dec_img = cv2.imencode("."+json['extent'], img)[1].tostring()
                st.UploadFaceRecognized(session["sessionId"],json['extent'],io.BytesIO(dec_img))
                print('FaceRecognized',time.time()-timedate)
                print(time.time()-timedate)
                if len(boxes_list) == 0:
                    return {'message':'Error.There is no face.Please try again'}
                else:
                    print({'message':'Success','image': st.URLofFaceRecognized(session['sessionId'],json['extent']), 'list': boxes_list})
                    return {'message':'Success','image': st.URLofFaceRecognized(session['sessionId'],json['extent']), 'list': boxes_list}
        #except:
            #return {'message':'Error.Please try again'}

#モザイク処理の実行
class UploadMosaicAction(Resource):
    def post(self): # 引数：JSON{list,extent_data,}
        #try:
            #session["sessionId"]= "".join(random.choices(string.ascii_letters + string.digits,k=8))
            #sessions.append(session["sessionId"])
            #実験用のセッション
            json_data = request.json
            #dec_data = base64.b64decode( json['image'].split(',')[1])
            box_list = json_data['list_face'] + json_data['list_text']
            with  cos5year_storage() as st:
                dec_data = st.GetOriginal(session['sessionId'],session['extent']) # オリジナルイメージのダウンロード
                img_array = np.fromstring(dec_data, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_ANYCOLOR)
                img = backend.mosaic.MosaicAction(img,box_list,st.URLofOriginal(session['sessionId'],session['extent']))
                dec_img = cv2.imencode("."+session['extent'], img)[1].tostring()
                st.UploadEndProcessing(session['sessionId'],session['extent'],io.BytesIO(dec_img))
                #print({'message':'Success','image': st.URLofEndProcessing(sessions,json_data['extent'])})
                return {'message':'Success','image': st.URLofEndProcessing(session['sessionId'],session['extent'])}
        #except:
           # return {'message':'Error.Please try again'}

class UploadSmileAction(Resource):
    def post(self): # 引数：JSON{list,extent_data,}
            #実験用のセッション
            json_data = request.json
            box_list = json_data['list_face'] + json_data['list_text']
            with  cos5year_storage() as st:
                dec_data = st.GetOriginal(session['sessionId'],session['extent']) # オリジナルイメージのダウンロード
                img_array = np.fromstring(dec_data, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_ANYCOLOR)
                img = backend.mosaic.SmileAction(img,box_list,URLofOriginal(session['sessionId'],session['extent'])) # SmileActionの実行
                dec_img = cv2.imencode("."+session['extent'], img)[1].tostring()
                st.UploadEndProcessing(session['sessionId'],session['extent'],io.BytesIO(dec_img))
                #print({'message':'Success','image': st.URLofEndProcessing(sessions,json_data['extent'])})
                return {'message':'Success','image': st.URLofEndProcessing(session['sessionId'],session['extent'])}


@app.route('/mosaic')
def FaceMosaic():
    return render_template('test.html',img = "",result = "")

@app.route('/image', methods=['POST'])
def image2base64():
    if request.files['image']:
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img_base64 = base64.b64encode(img_array)
        return {'image':str(img_base64)}

@app.route('/api/mosaic/mosaicaction1', methods=['POST'])
def MosaicAction():
    try:
        if request.files['image']:
            # 画像として読み込み
            stream = request.files['image'].stream
            list = request.form['list'] #チェックボックスでやってほしい
            img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, 1)
            origin = img.copy()
            Result = FaceMosaicAction(origin,list)
            Result_base64 = base64.b64encode(origin)
            return {'message':'モザイク成功','image': str(Result_base64), 'list': list}
    except:
        return {'message':'処理が失敗しました。やり直してください'}


##以下ルーティング登録
api.add_resource(Test,'/api/test')
api.add_resource(Json,'/api/test/json')
api.add_resource(Upload,'/api/mosaic/upload')
api.add_resource(UploadMosaicAction,'/api/mosaic/mosaicaction')
api.add_resource(UploadSmileAction,'/api/mosaic/smileaction')

@app.after_request
def after_request(response):
    return response

##以下デフォルトルーティング設定
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
