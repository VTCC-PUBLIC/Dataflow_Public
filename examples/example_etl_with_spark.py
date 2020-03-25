from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from zuka_etl.custom.operator import EtlOperator
from zuka_etl.log import logger
"""
Example: import a iterator to spark dataframe
"""
dags = DAG(
    'example_etl_with_spark',
    'Testing with spark',
    schedule_interval=None,
    start_date=datetime(2020, 1, 30)
)


def extract():
    from zuka_etl.pipeline.extract.spark_utils import SparkDfFromIterator
    from zuka_etl.custom.oracle_hook import OracleHook
    # process business
    data = OracleHook(oracle_conn_id="<airflow_connection_id>").get_records_dicts(

    )
    df = SparkDfFromIterator.from_iterator(iter=data, batch_size=50000)
    return df


def transform(df):
    df.show()
    return df


def load(value):
    # save data into some data sources
    # df.write.mode("overwrite").format("parquet").save("<path>")
    logger.info("done")


t1 = EtlOperator(task_id="main_job", extract=extract, transform=transform, load=load, dags=dags)
t1
