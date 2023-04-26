from abc import ABC
from airflow.models import Variable
import boto3
import os
import json


class Invoker(ABC):
    def invoke(self, payload: dict):
        pass

    def invoke_async(self, payload: dict):
        pass


class LambdaInvoker(Invoker):
    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id

    def _get_function_payload(self, partition_id: int):
        return str(partition_id)

    def invoke(self, payload: dict):
        # hacking just for test
        os.environ["AWS_ACCESS_KEY_ID"] = Variable.get("AWS_ACCESS_KEY_ID")
        os.environ["AWS_SECRET_ACCESS_KEY"] = Variable.get("AWS_SECRET_ACCESS_KEY")
        os.environ["AWS_SESSION_TOKEN"] = Variable.get("AWS_SESSION_TOKEN")
        client = boto3.client("lambda", region_name="eu-west-1")
        client.invoke(FunctionName=self.dataset_id, InvocationType="RequestResponse")

    # TODO: there should be a dead letter queue for async invocation
    def invoke_async(self, payload: dict):
        os.environ["AWS_ACCESS_KEY_ID"] = Variable.get("AWS_ACCESS_KEY_ID")
        os.environ["AWS_SECRET_ACCESS_KEY"] = Variable.get("AWS_SECRET_ACCESS_KEY")
        os.environ["AWS_SESSION_TOKEN"] = Variable.get("AWS_SESSION_TOKEN")
        client = boto3.client("lambda", region_name="eu-west-1")
        client.invoke(
            FunctionName=self.dataset_id,
            InvocationType="Event",
            Payload=json.dumps(payload),
        )
