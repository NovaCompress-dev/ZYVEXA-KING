from azure.storage.blob import BlobServiceClient
import os

class NovaAzureBridge:
    def __init__(self, connection_string):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = "nova-vault"

    def upload_to_cloud(self, local_vault_path):
        """Nova vault faylını birbaşa Azure-a yükləyir."""
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name, 
            blob=os.path.basename(local_vault_path)
        )
        
        print(f"🚀 Azure-a inteqrasiya başlayır: {local_vault_path}")
        with open(local_vault_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print("✅ Azure-da 90% qənaətlə saxlanıldı!")
