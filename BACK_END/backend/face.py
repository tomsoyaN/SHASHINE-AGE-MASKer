import cv2
import numpy

def mosaic(src, ratio):
   print(src)
   small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
   return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def FaceRecognition(img): #入力:画像配列 出力:画像の顔検出
   height,width,d = img.shape
   # 顔領域の検出の準備と実行(長方形群が返る)
   cas = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
   faces = cas.detectMultiScale(img, minSize=(5, 5))
   id = 1
   face_list=[]
   for (x, y, w, h) in faces: # 見つかった顔に四角を表示
      face_list.append({'id':id,'box':[int(x),int(y),int(x+w),int(y),int(x+w),int(y+h),int(x),int(y+h)],'type':"mosaic"})
      id += 1
   return face_list

def FaceMosaicAction(img,cut_list): # モザイク処理の実行　入力：画像,モザイクする座標の配列
   for (x, y, w, h) in cut_list:
      cut = img[y:y+h, x:x+w]
      print(img[y:y+h, x:x+w])
      img[y:y+h, x:x+w] = mosaic(cut,GenerateMosaicRate(w))
      print(GenerateMosaicRate(w))
   return img

def GenerateCuttingList(list): # Jsonの中から枠の番号のみのリストを返答する関数（テスト用）
   result_list = []
   for i in range(len(list)):
      result_list.append(list[i]['box'])
   return result_list

def GenerateIndexSize(w_size):
   index_size = w_size / 50
   if index_size < 0.5:
      index_size = 0.5
   elif index_size >= 10:
      index_size = 10
   return index_size

def GenerateRecognitionSize(ImageSize_h,ImageSize_w): # 枠線の太さを規定する
   rate = int(ImageSize_h*ImageSize_w / 10000000)
   R_size = rate+1
   return R_size

def GenerateMosaicRate(width):
   rate = 5.0 / float(width)
   return rate
