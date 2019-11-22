import os
import boto3
from botocore.exceptions import ClientError

import logging
from .periodic import Periodic
from pathlib import Path

class S3Sync(Periodic):
    s3 = None
    
    def __init__(self,agent):
        self.s3 = boto3.client('s3')
        super().__init__(agent,"s3-sync")

    def step(self):
        data_path = self.get_data_path()
        print("> Walking "+str(data_path))
        for current_path in data_path.rglob('*'):
            if(current_path.is_file()):
                self.offer(data_path,current_path)

    def offer(self,data_path,current_path):
        relative_path =  current_path.relative_to(data_path)
        if (not self.in_sync(data_path,relative_path)):
            self.sync(data_path,relative_path)
    
    def in_sync(self,data_path,relative_path):
        sensor_path = self.get_module_path()
        sync_result_file = data_path / sensor_path / ".txt"
        return False

    def sync(self,data_path,relative_path):
        raula_uuid = self.config["raula_uuid"]
        bucket = self.config["aws_bucket_user_data"]
        file_path = data_path / relative_path
        file_name = str(file_path)
        key = "{}/{}".format(raula_uuid,str(relative_path))
        print("PutObject {} => {}/{}".format(file_name,bucket,key))
        try:
            response = self.s3.upload_file(file_name, bucket, key)
            print(response)
        except ClientError as e:
            logging.error(e)
