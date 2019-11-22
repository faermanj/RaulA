import os
import boto3
import json
from botocore.exceptions import ClientError

import logging
from .periodic import Periodic
from pathlib import Path

class S3Sync(Periodic):
    s3 = boto3.client('s3')
    
    def step(self):
        data_path = self.get_data_path()
        for current_path in data_path.rglob('*'):
            if(current_path.is_file()):
                self.offer(data_path,current_path)

    def offer(self,data_path,current_path):
        relative_path =  current_path.relative_to(data_path)
        if (not self.in_sync(relative_path)):
            self.sync(data_path,relative_path)
    
    def in_sync(self,relative_path):
        key = self.key_of(relative_path)
        sync_result_file = self.get_results_filename(relative_path)
        sync_result_exists = sync_result_file.exists()
        return sync_result_exists
    
    def get_results_filename(self,relative_path):
        sensor_path = self.get_module_log_path()
        key = self.key_of(relative_path)
        sync_result_file = (sensor_path / key).with_suffix(".json.txt")
        return sync_result_file

    def key_of(self,relative_path):
        raula_uuid = self.agent.get_default("uuid")
        key = "{}/{}".format(raula_uuid,str(relative_path))
        return key

    def sync(self,data_path,relative_path):
        bucket = self.get_config("bucket")
        logging.info("Syncing to [{}]".format(bucket))
        file_path = data_path / relative_path
        file_name = str(file_path)
        key = self.key_of(relative_path)
        try:
            response = self.s3.upload_file(file_name, bucket, key)
            logging.debug("Uploaded [{}] => [s3://{}/{}]".format(file_name,bucket,key))
            response_json = json.dumps(response, indent=4, sort_keys=True)
            sync_result_file = self.get_results_filename(relative_path)
            sync_result_file.parent.mkdir(parents=True, exist_ok=True)
            with open(str(sync_result_file), "w") as f:
                f.write(response_json) 
        except ClientError as e:
            logging.error(e)
