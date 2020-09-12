
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
from config import face_endpoint,face_key
from backend.util import GetRotatedBOX

class cos5year_face:
    face_client = None
    def __enter__(self):
        self.face_client = FaceClient(face_endpoint, CognitiveServicesCredentials(face_key))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.face_client = None

    #入力画像URL,出力:{box:4点のリスト(jsonとかに格納されてるのと同じ),emotion:感情リスと}のリスト
    #感情リスト例{'additional_properties': {}, 'anger': 0.0, 'contempt': 0.002, 'disgust': 0.0, 'fear': 0.0, 'happiness': 0.0, 'neutral': 0.997, 'sadness': 0.001, 'surprise': 0.0}

    def __getEmotionList(self,imgURL):
        res = []
        detected_faces = self.face_client.face.detect_with_url(url=imgURL,return_face_attributes=['emotion'])
        for face in detected_faces:
            w=face.face_rectangle.width
            h=face.face_rectangle.height
            P0 = (face.face_rectangle.left,face.face_rectangle.top)
            P1 = (P0[0] + w,P0[1])
            P2 = (P0[0] + w,P0[1]+h)
            P3 = (P0[0] ,P0[1]+h)
            res.append({'box':[P0[0],P0[1],P1[0],P1[1],P2[0],P2[1],P3[0],P3[1]],'emotion':face.face_attributes.emotion})
        return res

    def __coordinateBOXID(self,boxes1,boxes2):
        print(boxes1,boxes2)
        res = []
        for i,box1 in enumerate(boxes1):
            P1 = (box1[0],box1[1])
            size1 = GetRotatedBOX(box1)[1]
            for j,box2 in enumerate(boxes2):
                P2 = (box2[0],box2[1])
                size2 = GetRotatedBOX(box2)[1]
                x = P2[0] - P1[0]
                y = P2[1] - P1[1]
                if(-size2[1] < x and x < size1[1] and -size2[0] < y and y < size1[0]):
                    res.append((i,j))
                    break
        return res

    def __setEmotionToBOX(self,boxlist,emotionlist):
        print("setEMOTIONTOBOX",boxlist,emotionlist)
        lis = self.__coordinateBOXID([emotion['box'] for emotion in emotionlist],boxlist)
        return [{'box':boxlist[j],'emotion':emotionlist[i]['emotion']}for i,j in lis]

    def GetEmotionList(self,boxlist,imgURL): #こいつを使う
        emolist = self.__getEmotionList(imgURL)
        res = self.__setEmotionToBOX(boxlist,emolist)
        return res # 座標(json)+emotion

'''
#テスト用のやつ
with cos5year_face() as cos5face:
    boxlist = [[117, 109, 169, 109, 169, 161, 117, 161]]
    imgURL = "https://cos5yearstorage.blob.core.windows.net/testcontainer/jng4ymLz-boxed.png"
    after = cos5face.GetEmotionList(boxlist,imgURL)
    print(after[0]['emotion'])
'''