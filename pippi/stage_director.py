from pippi.config import Config, InvokerConfig
from datetime import timedelta
from airflow.models.baseoperator import BaseOperator
from airflow.triggers.temporal import TimeDeltaTrigger
from airflow.utils.context import Context
from airflow.datasets import Dataset
from pippi.invoker import Invoker


class PippiInvokerOperator(BaseOperator):
    def __init__(
        self,
        config: Config,
        invoker_config: InvokerConfig,
        invoker_id: int,
        *args,
        **kwargs
    ):
        super(PippiInvokerOperator, self).__init__(*args, **kwargs)
        self.config = config
        self.invoker_config = invoker_config
        self.invoker_id = invoker_id

    def _get_environment_variables(self) -> dict:
        # TODO: The rest of the env vars
        return {
            "PIPPI_VAR_INVOKER_ID": self.invoker_id,
            "PIPPI_VAR_BRANCH": self.config.branch,
        }

    def execute(self, context: Context):
        self.invoker_config.invoker.invoke_async(self._get_environment_variables())


class PippiWaiterOperator(BaseOperator):
    def __init__(self, config: Config, invoker_config: InvokerConfig, *args, **kwargs):
        super(PippiWaiterOperator, self).__init__(*args, **kwargs)
        self.config = config
        self.invoker_config = invoker_config

    def execute(self, context: Context):
        self.is_done(context)

    def is_done(self, context: Context, event=None):
        # TODO: Implement
        # The dataset will produce num_invokers * job.pippi files on s3.
        # The path will, for dataset_storage s3, be:
        # s3://dataset_base_container/!datasetstate/dataset_name/branch/dataset_type/${timestamp}/job_n.pippi
        # This is how we can know it is done
        return

        self.defer(
            trigger=TimeDeltaTrigger(timedelta(seconds=30)),
            method_name="is_done",
        )


class PippiCommitterOperator(BaseOperator):
    def __init__(self, config: Config, invoker_config: InvokerConfig, *args, **kwargs):
        super(PippiCommitterOperator, self).__init__(*args, **kwargs)
        self.config = config
        self.invoker_config = invoker_config

        ds = config.get_dataset_id()
        if ds is not None:
            self.add_outlets([Dataset(ds)])

        if self.config.dependencies is not None:
            for dependency in self.config.dependencies:
                self.add_inlets([Dataset(dependency.get_dataset_id())])

    def execute(self, context: Context):
        # TODO: Implement
        return


class PippiStageDirector:
    def __init__(self, config: Config, invoker_config: InvokerConfig):
        self.config = config
        self.invoker_config = invoker_config

    def get_operators(self):
        invokers = []
        for invoker_id in range(self.invoker_config.num_invokers):
            invokers.append(
                PippiInvokerOperator(
                    config=self.config,
                    invoker_config=self.invoker_config,
                    invoker_id=invoker_id,
                    task_id="pippi_invoker_" + str(invoker_id),
                )
            )

        waiter = PippiWaiterOperator(
            config=self.config,
            invoker_config=self.invoker_config,
            task_id="pippi_waiter",
        )

        committer = PippiCommitterOperator(
            config=self.config,
            invoker_config=self.invoker_config,
            task_id="pippi_committer",
        )

        return invokers, waiter, committer
