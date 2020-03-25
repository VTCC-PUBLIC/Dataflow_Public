from datetime import datetime
from airflow import DAG
from zuka_etl.custom.operator import EtlOperator
from zuka_etl.log import logger
from traceback import format_exc

"""
Import a iterator to spark dataframe
"""

dags = DAG(
    'aio_oracle_etl',
    'AIO database crawling',
    schedule_interval=None,
    start_date=datetime(2020, 1, 30),
    catchup=False
)


def extract():
    from zuka_etl.custom.oracle_hook import OracleHook
    oracle_hook = OracleHook(oracle_conn_id='oracle_aio_aiopdb')
    from zuka_etl.pipeline.extract.spark_utils import SparkDfFromDriver
    tables_iterator = oracle_hook.get_records_dicts(
        sql="SELECT table_name FROM user_tables"
    )
    tables = list(tables_iterator)
    number_of_table_no_content = 0
    if len(tables) > 0:
        for index, table in enumerate(tables):
            try:
                table_name = table.get('TABLE_NAME')
                if table_name is not None and table_name != '':

                    logger.info('processing table = %s,%s' % (index, table))
                    sql_query = "SELECT * FROM %s" % table_name
                    df = SparkDfFromDriver.from_jdbc(table=sql_query, auto_cast_field_id=True,
                                                     connection_id="oracle_aio_aiopdb_jdbc")
                    logger.info('insert to table %s done' % table_name)
                    df.write.mode('overwrite').format('parquet').saveAsTable("vcc_coms_raw.{}".format(table_name))

            except Exception as e:
                logger.error(format_exc())
    else:
        logger.info('there is no table in coms schema ')

    logger.info('number of tables = %s' % len(tables))
    logger.info('number of tables dont have data = %s' % number_of_table_no_content)
    logger.info('insert done!!!!')
    pass


def transform(df):
    pass


def load(value):
    pass


t1 = EtlOperator(task_id="etl_with_oracle_main_job_aio",
                 extract=extract,
                 transform=transform,
                 load=load,
                 dag=dags)
t1