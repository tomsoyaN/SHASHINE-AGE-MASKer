from config import connect_str,container_name
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient,BlobProperties,StorageStreamDownloader

class cos5year_storage:
    blob_service_client = None
    blob_client = None

    def __enter__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.blob_client = None
        self.blob_service_client = None
    ##以下基板用##
    def get_blob(self,name):
        self.blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=name)
    def blob_upload(self,name,data):
        self.get_blob(name)
        self.blob_client.upload_blob(data)
    def delete_blob(self,name):
        self.get_blob(name)
        self.blob_client.delete_blob()
    def download_blob(self,name):
        self.get_blob(name)
        self.blob_client.get_blob_properties
        return self.blob_client.download_blob().readall()

    def get_metadata(self,name):
        self.get_blob(name)
        return self.blob_client.get_blob_properties().metadata
    ##以下実際に呼び出す用##
    def UploadOriginal(self,sessionId,origin_name,origin_extent,data):
        self.blob_upload(sessionId+"."+origin_extent,data)

    def UploadFaceRecognized(self,sessionId,origin_extent,data):
        self.blob_upload(sessionId+"-boxed."+origin_extent,data)

    def UploadEndProcessing(self,sessionId,origin_extent,data):
        self.blob_upload(sessionId+"-processed."+origin_extent,data)

    def GetOriginal(self,sessionId,origin_extent):
        return self.download_blob(sessionId + "." + origin_extent)

    def URLofOriginal(self,sessionId,origin_extent):
        return "https://cos5yearstorage.blob.core.windows.net/" + container_name + "/" + sessionId + "." + origin_extent

    def URLofFaceRecognized(self,sessionId,origin_extent):
        return "https://cos5yearstorage.blob.core.windows.net/" + container_name + "/" + sessionId + "-boxed." + origin_extent

    def URLofEndProcessing(self,sessionId,origin_extent):
        return "https://cos5yearstorage.blob.core.windows.net/" + container_name + "/" + sessionId + "-processed." + origin_extent

    def URLofMosaiced():
        return None
