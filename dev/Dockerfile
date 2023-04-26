# Base Image
FROM apache/airflow:2.5.1

ENV AIRFLOW_HOME=/opt/airflow

WORKDIR $AIRFLOW_HOME

# COPY airflow.cfg $AIRFLOW_HOME/airflow.cfg
RUN python -m pip install --upgrade pip
# RUN pip install -i https://test.pypi.org/simple/ pippi
RUN pip install boto3==1.26.109
RUN pip install -i https://test.pypi.org/simple/ pippi==0.20.19
# RUN pip install --upgrade --force-reinstall -i https://test.pypi.org/simple/ pippi
