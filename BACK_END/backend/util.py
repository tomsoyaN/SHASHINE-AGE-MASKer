#faceとtextに共通して使えそうなものたち
import cv2
import numpy as np

def DrawBOXes(img,boxes_list,color): #入力:画像,idとbox座標の辞書リスト,色(タプル)　出力:img
    height,width,d = img.shape
    for box in boxes_list:
        (x, y, w, h)=box['box']
        id = box['id']
        cv2.rectangle(img, (x, y), (x + w, y + h), color,GenerateRecognitionSize(height,width))
        cv2.putText(img, str(id),(x-1,y-1), cv2.FONT_HERSHEY_SIMPLEX, GenerateIndexSize(w),(0,255,0),GenerateRecognitionSize(height,width),cv2.LINE_AA)
    return img

def DrawBOXes2(img,boxes_list,color): #入力:画像,idとbox座標の辞書リスト,色(タプル)　出力:img
    height,width,d = img.shape
    for box in boxes_list:
      cords = box['box']
      (w,h) = (cords[2] -cords[0],cords[1] - cords[7])
      id = box['id']
      cv2.line(img, (cords[0],cords[1]), (cords[2],cords[3]),color,GenerateRecognitionSize(height,width))
      cv2.line(img, (cords[2],cords[3]), (cords[4],cords[5]),color,GenerateRecognitionSize(height,width))
      cv2.line(img, (cords[4],cords[5]), (cords[6],cords[7]),color,GenerateRecognitionSize(height,width))
      cv2.line(img, (cords[6],cords[7]), (cords[0],cords[1]),color,GenerateRecognitionSize(height,width))
      cv2.drawMarker(img, (cords[0],cords[1]), (255, 0, 0))
      cv2.putText(img, str(id),(cords[0]-1,cords[1]-1), cv2.FONT_HERSHEY_SIMPLEX, GenerateIndexSize(w),(0,255,0),GenerateRecognitionSize(height,width),cv2.LINE_AA)
    return img

def sortCords(list):#短形の座標リストを左上が原点とし時計回りになるよう並べ替える
   list_x =[list[i] for i in range(0,7,2)]
   list_y =[list[i] for i in range(1,8,2)]

   y_min = min(list_y)
   if(list_y.count(y_min)== 1):#y座標が同率でない場合
      idx = list_y.index(y_min)
      P0 = (list_x[idx],list_y[idx])
   else:#y座標が同率な場合
      tmp = [(list_x[i],i )for i in range(len(list_y)) if list_y[i] == y_min]
      if(tmp[0][0] < tmp[1][0]) :
         idx = tmp[0][1]
         P0 = (list_x[idx],list_y[idx])
      else:
         idx = tmp[1][1]
         P0 = (list_x[idx],list_y[idx])
   list_x.pop(idx)
   list_y.pop(idx)

   V0 = np.array([1,0])
   V1 = np.array([list_x[0] - P0[0],list_y[0] - P0[1]])
   V2 = np.array([list_x[1] - P0[0],list_y[1] - P0[1]])
   V3 = np.array([list_x[2] - P0[0],list_y[2] - P0[1]])
   I01 = np.inner(V0,V1)
   I02 = np.inner(V0,V2)
   I03 = np.inner(V0,V3)
   N1 = np.linalg.norm(V1)
   N2 = np.linalg.norm(V2)
   N3 = np.linalg.norm(V3)
   args = [np.arccos(I01/N1),np.arccos(I02/N2),np.arccos(I03/N3)]
   idx = args.index(min(args))
   P1 = (list_x[idx],list_y[idx])
   list_x.pop(idx)
   list_y.pop(idx)
   args.pop(idx)
   idx = args.index(max(args))
   P3 = (list_x[idx],list_y[idx])
   list_x.pop(idx)
   list_y.pop(idx)
   P2 = (list_x[0],list_y[0])
   t=GetRotatedBOX([P0[0],P0[1],P1[0],P1[1],P2[0],P2[1],P3[0],P3[1]])
   return [P0[0],P0[1],P1[0],P1[1],P2[0],P2[1],P3[0],P3[1]]

def GetRotatedBOX(cords):
   print(cords)
   P0 = np.array([cords[0],cords[1]])
   P1 = np.array([cords[2],cords[3]])
   P2 = np.array([cords[4],cords[5]])
   P3 = np.array([cords[6],cords[7]])
   center = (int((cords[0]+cords[2]+cords[4]+cords[6])/4),int((cords[1]+cords[3]+cords[5]+cords[7])/4))
   V0 = np.array([1,0])
   I02 = np.inner(V0,P2-P0)
   N02 = np.linalg.norm(P2-P0)
   if(np.arccos(I02/N02)  <=np.pi/2):
      size = (int(abs(np.linalg.norm(P1-P0))),int(abs(np.linalg.norm(P3-P0))))
   else:
      size = (int(abs(np.linalg.norm(P3-P0))),int(abs(np.linalg.norm(P1-P0))))
   O = np.array([1,0])
   arg = np.arccos(np.inner(O,P1-P0)/np.linalg.norm(P1-P0))
   return (center,size,arg)#size=(height,width)

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
   rate = 5 / width
   return rate
