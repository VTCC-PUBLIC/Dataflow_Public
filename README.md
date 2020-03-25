### Installing
Goto airflow whl_package
```bash
cd ${AIRFLOW_HOME}
```
Using virtualenv
```bash
virtualenv -p python3 venv
source venv/bin/active
python3 -m pip install /path/your_name_package.whl
```
Using user env
```bash
python3 -m pip install /path/your_name_package.whl --user
```
# configuration
Config Spark on airflow connection. Define name of connection and add config on extras field
-  Config SparkClient. Default config name is: spark_connection_default
```buildoutcfg
{
                    "master": "local[*]",
                    "app_name": "etl_operator_spark",
                    "mode": "client",
                    "conf": {
                        "spark.jars.packages": "mysql:mysql-connector-java:5.1.47,org.elasticsearch:elasticsearch-hadoop:6.4.2",
                        "spark.dynamicAllocation.enabled": "true",
                        "spark.dynamicAllocation.maxExecutors": 5,
                        "spark.executor.cores": 4,
                        "spark.executor.memory": "2G",
                        "spark.shuffle.service.enabled": "true",
                        "spark.files.overwrite": "true",
                        "spark.sql.warehouse.dir": "/apps/spark/warehouse",
                        "spark.sql.catalogImplementation": "hive",
                        "spark.sql.sources.partitionOverwriteMode": "dynamic",
                        "hive.exec.dynamic.partition.mode": "nonstrict",
                        "spark.sql.caseSensitive": "true"
                    },
                    "env_vars": {
                        "SPARK_HOME": ""
                    },
                    "py_files": ["test.py"]
                }
```

-  Config SparkSubmit. Default config name is: spark_connection_default_submit.

```
{
                    "master": "yarn",
                    "app_name": "etl_operator_spark",
                    "queue": "default",
                    "deploy_mode": "yarn-cluster",
                    "conf": {
                        "spark.jars.packages": "mysql:mysql-connector-java:5.1.47,org.elasticsearch:elasticsearch-hadoop:6.4.2",
                        "spark.dynamicAllocation.enabled": "true",
                        "spark.dynamicAllocation.maxExecutors": 5,
                        "spark.executor.cores": 4,
                        "spark.executor.memory": "2G",
                        "spark.shuffle.service.enabled": "true",
                        "spark.files.overwrite": "true",
                        "spark.sql.warehouse.dir": "/apps/spark/warehouse",
                        "spark.sql.catalogImplementation": "hive",
                        "spark.sql.sources.partitionOverwriteMode": "dynamic",
                        "hive.exec.dynamic.partition.mode": "nonstrict",
                        "spark.sql.caseSensitive": "true"
                    },
                    "env_vars": {
                        "SPARK_HOME": "<path>"
                    }
                }
```
# Features
## Airflow hook
Support multiple hook:
-	MySQL, Oracle, PostgreSQL, Redis, FTP, MongoDB, ...
## Custom hook
-	Spark, HDFS client, JDBC, ...
# examples
- Example etl with spark and oracle hook:
```python
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
 # df.write.mode("overwrite").format("parquet").save("<path>")  logger.info("done")  
  
  
t1 = EtlOperator(task_id="main_job", extract=extract, transform=transform, load=load, dags=dags)  
t1
```
-	Example with pandas and Jdbc
```python
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
 # df.to_csv("<path>")  logger.info("done")  
  
  
t1 = EtlOperator(task_id="main_job", extract=extract, transform=transform, load=load, dags=dags)  
t1
```

-	Example with spark and jdbc
```python
from airflow import DAG  
from airflow.operators.bash_operator import BashOperator  
from datetime import datetime, timedelta  
from airflow.models import Variable  
from zuka_etl.custom.operator import EtlOperator  
from zuka_etl.log import logger  
  
dags = DAG(  
    'example_etl_with_spark_jdbc',  
  'Testing with spark',  
  schedule_interval=None,  
  start_date=datetime(2020, 1, 30)  
)  
  
  
def extract():  
    # process business  
    from zuka_etl.pipeline.extract.spark_utils import SparkDfFromDriver
    df = SparkDfFromDriver.from_jdbc(  
        table="select {columns} from database.table where {name} = 1",  
         connection_id="<connection jdbc that defined on airflow>",    
          )  
    return df  
  
  
def transform(df):  
    print(df.show())  
    return df  
  
  
def load(value):  
    # save data into some data sources  
    df.write.mode("overwrite").format("parquet").saveAsTable("test")  
  
  
t1 = EtlOperator(task_id="main_job", extract=extract, transform=transform, load=load, dags=dags)  
t1
```