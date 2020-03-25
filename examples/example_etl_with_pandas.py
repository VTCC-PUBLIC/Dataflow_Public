from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from zuka_etl.custom.operator import EtlOperator
from zuka_etl.log import logger

dags = DAG(
    'example_etl_with_spark',
    'Testing with spark',
    schedule_interval=None,
    start_date=datetime(2020, 1, 30)
)


def extract():
    from zuka_etl.pipeline.extract.pandas_utils import PandasDfFromSQL
    # process business
    df = PandasDfFromSQL.from_sql(
        table="select {columns} from database.table where {name} = 1",
        connection_id="<connection that defined on airflow>",
        params={
            "columns": "id, name",
            "name": "id"
        }
    )
    return df


def transform(df):
    print(df.head())
    return df


def load(value):
    # save data into some data sources
    # df.to_csv("<path>")
    logger.info("done")


t1 = EtlOperator(task_id="main_job", extract=extract, transform=transform, load=load, dags=dags)
t1
