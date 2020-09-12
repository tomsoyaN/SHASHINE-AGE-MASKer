import sys
import numpy as np
sys.path.append('../')
import cv2
from visionAPI import cos5year_vision
from backend.util import sortCords
from azure_storage import cos5year_storage

def TextRecognize(img,img_url):
    with cos5year_vision() as vi:
        res = vi.DetectTexts(img_url)
        id = 1
        text_list =[]
        for o in res[0]:
            o['box'] = [int(e) for e in o['box']]
            p_lL = np.array([o['box'][6],o['box'][7]])#左下の座標
            p_tR = np.array([o['box'][2],o['box'][3]])#右上の座標
            (x,y,w,h) = (int(p_lL[0]),int(p_lL[1]),int(p_tR[0]-p_lL[0]),int(p_tR[1]-p_lL[1]))
            text_list.append({'id':id,'box':sortCords(o['box']),'type':"mosaic"})
            id += 1
        return text_list