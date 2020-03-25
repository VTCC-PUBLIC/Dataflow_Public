from datetime import datetime
from airflow import DAG
from zuka_etl.custom.operator import EtlOperator
from zuka_etl.log import logger
from traceback import format_exc

"""
Import a iterator to spark dataframe
"""

dags = DAG(
    'sync_all_oracle_vcc',
    'AIO database crawling',
    schedule_interval=None,
    start_date=datetime(2020, 1, 30),
    catchup=False
)

config = {
    # "vcc_ams_raw": "oracle_ams_aiopdb_jdbc",
    # "vcc_wms_raw": "oracle_wms_aiopdb_jdbc",
    # "vcc_aio_raw": "oracle_aio_aiopdb_jdbc",
    "vcc_coms_raw": "oracle_coms_aiopdb_jdbc",
    "vcc_ims_raw": "oracle_ims_aiopdb_jdbc",
    "vcc_hcqt_raw": "oracle_hcqt_aiopdb_jdbc",
}


def extract():
    from zuka_etl.custom.jdbc_hook import JdbcHook
    for database, conf in config.items():
        oracle_hook = JdbcHook(conf)
        logger.info("RUN DATABASE: %s" % database)
        from contextlib import closing

        from zuka_etl.pipeline.extract.spark_utils import SparkDfFromDriver
        from zuka_etl.custom.spark_hook import SparkHook
        tables_iterator = oracle_hook.get_records_dicts(
            sql="SELECT table_name FROM user_tables"
        )
        tables = list(tables_iterator)
        logger.info(tables)
        number_of_table_no_content = 0
        if len(tables) > 0:
            n = 0
            for index, table in enumerate(tables):
                try:
                    table_name = table.get('TABLE_NAME')
                    if table_name is not None and table_name != '':
                        n += 1
                        logger.info(n)
                        logger.info('processing table = %s,%s' % (index, table))
                        sql_query = "SELECT * FROM %s" % table_name
                        df = SparkDfFromDriver.from_jdbc(table=sql_query, auto_cast_field_id=True,
                                                         connection_id=conf)
                        logger.info('insert to table %s done' % table_name)
                        df.write.mode('overwrite').format('parquet').saveAsTable("%s.%s" % (database, table_name))
                        if n % 5 == 0:
                            logger.info("Stop context......")
                            SparkHook().stop()
                except Exception as e:
                    logger.error(format_exc())
            SparkHook().stop()
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


t1 = EtlOperator(task_id="etl_with_oracle_main_job",
                 extract=extract,
                 dag=dags)
t1
