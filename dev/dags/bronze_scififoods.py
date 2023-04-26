import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from pippi.stage_director import PippiStageDirector
from pippi.config import Config, InvokerConfig, Storage, DatasetType
from pippi.invoker import LambdaInvoker
from airflow.models.baseoperator import chain

start_date = pendulum.datetime(2021, 1, 1, tz="UTC")

config = Config(
    # TODO: branch should be set by pippi.deployer
    branch="main",
    repository="pippi",
    project="dev",
    name="bronze_scififoods",
    dataset_storage=Storage.S3,
    dataset_type=DatasetType.BATCH,
    dataset_base_container="invert-sbo-playground",
)

default_args = {
    "owner": "airflow",
    "start_date": start_date,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id=config.get_dataset_id(),
    schedule_interval="@hourly",
    default_args=default_args,
    catchup=False,
) as dag:
    p = PippiStageDirector(
        config=config,
        invoker_config=InvokerConfig(
            invoker=LambdaInvoker(dataset_id=config.get_dataset_id()),
            num_invokers=3,
        ),
    )
    invokers, waiter, committer = p.get_operators()
    task_2 = EmptyOperator(task_id="dummy_task_2")

    invokers >> waiter >> committer >> task_2
