from typing import Iterable
from pippi.invoker import Invoker

from enum import Enum


class Storage(str, Enum):
    S3 = "S3"
    MongoDB = "MongoDB"


class DatasetType(str, Enum):
    BATCH = "BATCH"
    INCREMENTAL = "INCREMENTAL"


class DependencyStrategy(str, Enum):
    ALL = "RUN_WHEN_ALL_DEPENDENCIES_ARE_UPDATED_AT_LEAST_ONCE"
    ANY = "RUN_WHEN_ANY_DEPENDENCY_IS_UPDATED_AT_LEAST_ONCE"


class DependencyConfig:
    def __init__(
        self,
        dataset_storage: Storage,
        dataset_type: DatasetType,
        dataset_base_container: str,
        dataset_id: str,
        exclude_from_strategy: bool = False,
    ):
        self.dataset_storage = dataset_storage
        self.dataset_type = dataset_type
        self.dataset_base_container = dataset_base_container
        self.dataset_id = dataset_id
        self.exclude_from_strategy = exclude_from_strategy

    def get_dataset_id(self):
        return self.dataset_id


class Config:
    def __init__(
        self,
        branch: str,
        repository: str,
        project: str,
        name: str,
        dataset_storage: Storage,
        dataset_type: DatasetType,
        dataset_base_container: str,
        dependency_strategy: DependencyStrategy = DependencyStrategy.ANY,
        dependencies: Iterable[DependencyConfig] = None,
    ):
        # branch represents which git branch we are running on
        self.branch = branch
        self.repository = repository
        self.project = project
        self.name = name
        # dataset_storage represents the place where data is stored, e.g. a filesystem or S3
        self.dataset_storage = dataset_storage
        # dataset_type
        self.dataset_type = dataset_type
        # dataset_base_container for S3 is the name of the 'bucket', and for e.g. Azure it is the name of the 'container'
        self.dataset_base_container = dataset_base_container
        # dependency_strategy dictates how we determine whether it is time to run or not
        self.dependency_strategy = dependency_strategy
        # dependencies represents other datasets that we depend on
        self.dependencies = dependencies

    def validate(self):
        pass

    def get_dataset_id(self):
        ds = f"{self.branch}-{self.repository}-{self.project}-{self.name}"

        return ds


class InvokerConfig:
    def __init__(
        self,
        invoker: Invoker,
        num_invokers: int = 1,
    ):
        # invoker represents the entity that will actually start the job
        self.invoker = invoker
        # This represents the number of activations of the invoker.
        # For a lambda invoker, this means we invoke n lambdas concurrently
        self.num_invokers = num_invokers
