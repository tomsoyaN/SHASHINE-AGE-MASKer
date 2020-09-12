import sys
sys.path.append('../')
import cv2
import numpy as np
from backend.util import GetRotatedBOX
from backend.face import GenerateCuttingList
from faceAPI import cos5year_face
import ast

FaceAPI = cos5year_face()

def mosaic(src, ratio):
   small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
   return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def smile(src): # ニコちゃんマーク（スマイル）を合成する
    height,width = src.shape[:2]
    if height/width > 2 and height/width <= 0.5: # 横長とかのテキストのときはモザイクをかける
        src = mosaic(src,GenerateMosaicRate(width))
    else:
        smile_img = cv2.imread('backend/images/smile.png')
        smile_img = cv2.resize(smile_img,(int(height),int(width))) # 切り出し画像に合わせて画像をリサイズ
        src = cv2.add(src, smile_img) # 画像を合成
    return src

def AutoMark(src,index): # ニコちゃんマーク（スマイル）を合成する
    emotion_name = ['anger','contempt','disgust','fear','happiness','neutral','sadness','surprise','else']
    height,width = src.shape[:2]
    if height/width > 2 and height/width <= 0.5: # 横長とかのテキストのときはモザイクをかける
        src = mosaic(src,GenerateMosaicRate(width))
    else:
        # ここで色々判別する！！
        if emotion_name[index] == 'anger':
            smile_img = cv2.imread('backend/images/anger.png')
        elif emotion_name[index] == 'contempt':
            smile_img = cv2.imread('backend/images/yorokobu.png')
        elif emotion_name[index] == 'disgust':
            smile_img = cv2.imread('backend/images/nemui.png')
        elif emotion_name[index] == 'fear':
            smile_img = cv2.imread('backend/images/munk.png')
        elif emotion_name[index] == 'happiness':
            smile_img = cv2.imread('backend/images/smile.png')
        elif emotion_name[index] == 'neutral':
            smile_img = cv2.imread('backend/images/pero.png')
        elif emotion_name[index] == 'sadness':
            smile_img = cv2.imread('backend/images/komarigao.png')
        elif emotion_name[index] == 'surprise':
            smile_img = cv2.imread('backend/images/yorokobu.png')
        else:
            smile_img = cv2.imread('backend/images/mask.png')
        smile_img = cv2.resize(smile_img,(int(height),int(width))) # 切り出し画像に合わせて画像をリサイズ
        src = cv2.add(src, smile_img) # 画像を合成
    return src

#名前:関数名の辞書
def MosaicAction(img,cut_list,url): # モザイク処理の実行　入力：画像,モザイクする座標の配列
    for box in cut_list:
        cords,mosaic_type = (box['box'],box['type'])
        center,size,arg = GetRotatedBOX(cords)
        h,w = img.shape[:2]
        angle_rad = arg/180.0*np.pi
        w_rot = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
        h_rot = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
        size_rot = (w_rot, h_rot)
        # 元画像の中心を軸に回転する
        scale = 1.0
        rotation_matrix = cv2.getRotationMatrix2D((w/2,h/2), -arg, scale)
        # 平行移動を加える (rotation + translation)
        affine_matrix = rotation_matrix.copy()
        affine_matrix[0][2] = affine_matrix[0][2] -w/2 + w_rot/2
        affine_matrix[1][2] = affine_matrix[1][2] -h/2 + h_rot/2
        img_rot = cv2.warpAffine(img, affine_matrix, size_rot, flags=cv2.INTER_LANCZOS4)
        center = cv2.transform(np.array([[[center[0], center[1]]]]),affine_matrix)
        center=(center[0,0,0],center[0,0,1])
        cut = cv2.getRectSubPix(img_rot, size, (center[0],center[1]))
        P0 = (int(center[0]-size[0]/2),int(center[1]-size[1]/2))
        #----------同じようにモザイクの種類を増やしていく----------------------------------------
        if(mosaic_type=='mosaic'):
            cut = mosaic(cut,GenerateMosaicRate(size[1]))
        elif(mosaic_type=='smile'):
            cut = smile(cut)
        elif(mosaic_type=='auto'): #オートタイプの時
            with cos5year_face() as cos5face:
                emotion = cos5face.GetEmotionList([cords],url) # エモーションを取得
                if(len(emotion)>0):
                    emoes = emotion[0]['emotion']
                    xs = np.array([emoes.anger,emoes.contempt,emoes.disgust,emoes.fear,emoes.happiness,emoes.neutral,emoes.sadness,emoes.surprise])
                    max_index = np.argmax(xs)
                else:
                    max_index=8
                cut = AutoMark(cut,max_index) # ここで判別

        ##############################################################
        img_rot[P0[1]:P0[1]+size[1],P0[0]:P0[0]+size[0]] = cut
        rotation_matrix = cv2.getRotationMatrix2D((w/2,h/2), arg, scale)
        affine_matrix = rotation_matrix.copy()
        affine_matrix[0][2] = affine_matrix[0][2] +w/2 - w_rot/2
        affine_matrix[1][2] = affine_matrix[1][2] +h/2 - h_rot/2
        img = cv2.warpAffine(img_rot, affine_matrix, size_rot, flags=cv2.INTER_LANCZOS4)[0:h,0:w]
    return img

def SmileAction(img,cut_list): # モザイク処理の実行　入力：画像,モザイクする座標の配列
    for cords in cut_list:
        center,size,arg = GetRotatedBOX(cords)
        h,w = img.shape[:2]
        angle_rad = arg/180.0*np.pi
        w_rot = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
        h_rot = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
        size_rot = (w_rot, h_rot)
        # 元画像の中心を軸に回転する
        scale = 1.0
        rotation_matrix = cv2.getRotationMatrix2D((w/2,h/2), -arg, scale)
        # 平行移動を加える (rotation + translation)
        affine_matrix = rotation_matrix.copy()
        affine_matrix[0][2] = affine_matrix[0][2] -w/2 + w_rot/2
        affine_matrix[1][2] = affine_matrix[1][2] -h/2 + h_rot/2
        img_rot = cv2.warpAffine(img, affine_matrix, size_rot, flags=cv2.INTER_LANCZOS4)
        center = cv2.transform(np.array([[[center[0], center[1]]]]),affine_matrix)
        center=(center[0,0,0],center[0,0,1])
        cut = cv2.getRectSubPix(img_rot, size, (center[0],center[1]))
        P0 = (int(center[0]-size[0]/2),int(center[1]-size[1]/2))
        #img_rot[P0[1]:P0[1]+size[1],P0[0]:P0[0]+size[0]] = mosaic(cut,GenerateMosaicRate(size[1]))
        img_rot[P0[1]:P0[1]+size[1],P0[0]:P0[0]+size[0]] = smile(cut)
        rotation_matrix = cv2.getRotationMatrix2D((w/2,h/2), arg, scale)
        affine_matrix = rotation_matrix.copy()
        affine_matrix[0][2] = affine_matrix[0][2] +w/2 - w_rot/2
        affine_matrix[1][2] = affine_matrix[1][2] +h/2 - h_rot/2
        img = cv2.warpAffine(img_rot, affine_matrix, size_rot, flags=cv2.INTER_LANCZOS4)[0:h,0:w]
    return img

def GenerateMosaicRate(width):
   rate = 5.0 / float(width)
   return rate

"""
image = cv2.imread('hanzawa.png') # 画像の読み込み
origin = image.copy()
list = [{'id': 1, 'box': [99, 13, 122, 13, 122, 36, 99, 36]}, {'id': 2, 'box': [241, 11, 264, 11, 264, 34, 241, 34]}, {'id': 3, 'box': [26, 13, 49, 13, 49, 36, 26, 36]}, {'id': 4, 'box': [168, 13, 193, 13, 193, 38, 168, 38]}, {'id': 5, 'box': [23, 71, 48, 71, 48, 96, 23, 96]}, {'id': 6, 'box': [100, 73, 121, 73, 121, 94, 100, 94]}, {'id': 7, 'box': [169, 71, 193, 71, 193, 95, 169, 95]}, {'id': 8, 'box': [239, 71, 263, 71, 263, 95, 239, 95]}, {'id': 9, 'box': [24, 125, 48, 125, 48, 149, 24, 149]}, {'id': 10, 'box': [163, 127, 188, 127, 188, 152, 163, 152]}, {'id': 11, 'box': [92, 129, 116, 129, 116, 153, 92, 153]}, {'id': 12, 'box': [238, 129, 264, 129, 264, 155, 238, 155]}]
cutlist = GenerateCuttingList(list)
print(cutlist)
Result = SmileAction(image,cutlist)
cv2.imwrite('nikochan_hanzawa.png',Result)
cv2.imshow('image', Result) # 結果の表示
cv2.waitKey(0) # キー入力を待つ
cv2.destroyAllWindows() # ウインドウを破棄
"""
