from locust import HttpUser, task, between
from requests.auth import HTTPBasicAuth
import random

class User(HttpUser):
    WEBDAV_BASE_PATH = "/remote.php/dav/files/"
    wait_time = between(1, 5)  # Simulate wait time between 1 and 5 seconds

    def on_start(self):
        self.user = "testuser00" + str(random.randint(1, 100000))
        self.password = self.user
        headers = {
            "OCS-APIRequest": "true",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            "userid": self.user,
            "password": self.password
        }
        self.client.post(
            "/ocs/v1.php/cloud/users",
            data=payload,
            headers=headers,
            auth=HTTPBasicAuth("admin", "admin")
        )
       
    @task(3)
    def task_read_files(self):
        self.client.request("PROPFIND", f"{self.WEBDAV_BASE_PATH}{self.user}/", auth=(self.user, self.password), name="read_files")
       
    @task(8)
    def task_download(self):
        url = self.WEBDAV_BASE_PATH + self.user + "/Readme.md"
        self.client.get(url, auth=(self.user, self.password), name="download")

    @task(10)
    def task_upload_small_file(self):
        files = ["/locust/kb", "/locust/mb"]
        filesize = ["kilobyte", "megabyte"]
        random_idx = random.randint(0, 1)
        with open(files[random_idx], "rb") as file:
            remote_path = self.WEBDAV_BASE_PATH + self.user + "/locust_file_" + str(random.randint(1, 100000))
            self.client.put(remote_path, data=file, auth=(self.user, self.password), name=f"upload_file_{filesize[random_idx]}")
    
    @task(2)
    def task_upload_big_file(self):
        with open("/locust/gb", "rb") as file:
            remote_path = self.WEBDAV_BASE_PATH + self.user + "/locust_file_" + str(random.randint(1, 100000))
            self.client.put(remote_path, data=file, auth=(self.user, self.password), name="upload_file_gigabyte")