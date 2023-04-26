import pendulum
from airflow import DAG
from airflow.datasets import Dataset
from airflow.operators.empty import EmptyOperator
from airflow.decorators import task
from airflow.configuration import conf
from airflow.lineage.entities import File
from pippi.stage_director import PippiStageDirector
from pippi.config import Config, InvokerConfig, Storage, DatasetType, DependencyConfig
from pippi.invoker import LambdaInvoker
from airflow.models.baseoperator import chain

start_date = pendulum.datetime(2021, 1, 1, tz="UTC")
# TODO: The dag id should be filled by pippi.deploy
dataset_id = "pippi-dev-silver_scififoods"
silver_dataset = Dataset(dataset_id)

dep1 = DependencyConfig(
    Storage.S3,
    DatasetType.BATCH,
    "invert-sbo-playground",
    "main-pippi-dev-bronze_scififoods",
)

# TODO: branch should be set by pippi.deploy
config = Config(
    branch="main",
    repository="pippi",
    project="dev",
    name="silver_scififoods",
    dataset_storage=Storage.S3,
    dataset_type=DatasetType.BATCH,
    dataset_base_container="invert-sbo-playground",
    dependencies=[dep1],
)

with DAG(
    dag_id=config.get_dataset_id(),
    start_date=start_date,
    catchup=False,
    schedule=[Dataset("main-pippi-dev-bronze_scififoods")],
) as parent_dag:
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
