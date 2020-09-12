from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from config import endpoint,subscription_key

import time

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
class cos5year_vision:
    computervision_client = None

    ##以下クラス内呼び出し専用
    def __enter__(self):
        self.computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.computervision_client = None
    
    def __image_read(self,image_url):
        recognize_results = self.computervision_client.read(image_url,  raw=True)
        operation_location_remote = recognize_results.headers["Operation-Location"]
        operation_id = operation_location_remote.split("/")[-1]
        return operation_id
        
    def __get_read_result(self,operation_id):
        ##ここの無限ループどうにかする
        while True:
            get_text_results = computervision_client.get_read_result(operation_id)
            if get_text_results.status not in ['notStarted', 'running']:
                break
            time.sleep(1)
        if get_text_results.status == OperationStatusCodes.succeeded:
            return get_text_results.analyze_result.read_results

    ##以下外部呼出し関数

    def DetectTexts(self,image_url):
        id = self.__image_read(image_url)
        res = self.__get_read_result(id)
        return [[{'text':line.text,'box':line.bounding_box} for line in text_result.lines] for text_result in res]
