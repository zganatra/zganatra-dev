from google.cloud import secretmanager
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

class SecretManager:
    def __init__(self,project_id):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def _get_secret_version_name(self,project_id_number,secret_name,version_number):
        version_name = "projects/"+project_id_number+"/secrets/"+secret_name+"/versions/"+version_number
        return version_name

    def _get_project_number(self,project_id):
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
        request = service.projects().get(projectId=project_id)
        project_details = request.execute()
        return project_details['projectNumber']

    def store_api_key(self, secret_id, api_key):
        parent = "projects/{self.project_id}"
        secret = self.client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        version = self.client.add_secret_version(
            request={"parent": secret.name, "payload": {"data": str.encode(api_key)}}
        )
        return version.name

    def get_api_key(self, secret_name, version_number):
        project_id_number= self._get_project_number(self.project_id)
        version_name = self._get_secret_version_name(project_id_number,secret_name,version_number)
        response = self.client.access_secret_version(request={"name": version_name})
        api_key = response.payload.data.decode("UTF-8")
        return api_key


    def _create_new_version(self,secret_id, api_key):
        name = self.client.secret_path(self.project_id, secret_id)
        version = self.client.add_secret_version(
            request={"parent": name, "payload": {"data": str.encode(api_key)}}
        )
        return version.name

    def _disable_previous_version(self):
        //TODO
        return

    def update_api_key(self,secret_id, api_key):
        version_name = self.create_new_version(secret_id,api_key)
        self._disable_previous_versions()
