from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from zuka_etl.custom.operator import EtlOperator
from zuka_etl.log import logger

dags = DAG(
    'example_test_dataframe',
    'Testing example zuka etl',
    schedule_interval=None,
    start_date=datetime(2020, 1, 30)
)


def extract():
    # process business
    def gen():
        for k in range(0, 10000):
            yield {
                "id": 1,
                "phong": 1,
                "phong1": 1,
                "phong2": 1,
                "phong3": 1,
                "phong4": 1,
                "phong5": 1,
                "phong6": 1,
                "phong7": 1,
                "phong8": 1,
                "phong9": 1,
                "phong10": 1,
                "phong11": 1,
                "phong12": 1,
                "phong13": 1,
                "phong14": 1,
                "phong15": 1,
                "phong16": 1,
                "phong17": 1

            }

    from zuka_etl.pipeline.extract.spark_utils import SparkDfFromIterator
    return SparkDfFromIterator.from_iterator(iter=gen())


def transform(value):
    value.show()
    return value


def load(value):
    # save data into some data sources
    logger.info("done")


t1 = EtlOperator(task_id="test_performance", extract=extract, transform=transform, load=load, dag=dags)
t1
