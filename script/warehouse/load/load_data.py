from utils.helper import logging_process, init_spark_session, load_log_msg
import logging
import pyspark
from sqlalchemy import create_engine, text
from datetime import datetime

logging_process()


def load_data(df_result: pyspark.sql.DataFrame, table_name: str) -> None:
    """
    Function to truncate a table using SQLAlchemy and then load data into it using PySpark,
    while logging success/failure ETL events into a log table.
    """
    spark = init_spark_session()
    current_timestamp = datetime.now()
    log_message = None

    # DB config
    DB_HOST = "pipeline_db"
    DB_PORT = "5432"
    DB_NAME = "warehouse"
    DB_USER = "postgres"
    DB_PASS = "cobapassword"

    jdbc_url = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
    sqlalchemy_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    connection_properties = {
        "user": DB_USER,
        "password": DB_PASS,
        "driver": "org.postgresql.Driver"
    }

    try:
        logging.info(f"===== Start Load {table_name} to the database =====")

        # TRUNCATE TABLE using SQLAlchemy
        engine = create_engine(sqlalchemy_url)
        with engine.connect() as connection:
            connection.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))
            logging.info(f"===== Truncated table {table_name} successfully =====")

        # Load data using PySpark
        df_result.write.jdbc(
            url=jdbc_url,
            table=table_name,
            mode="append",
            properties=connection_properties,
        )

        logging.info("===== Finish Load data to the database =====")

        # SUCCESS log
        log_message = spark.sparkContext.parallelize([(
            "warehouse", "load", "success", "db", table_name, current_timestamp
        )]).toDF(["step", "process", "status", "source", "table_name", "etl_date"])

    except Exception as e:
        logging.error(f"===== Failed Load {table_name} to the database =====")
        logging.error(str(e))

        # FAILURE log
        log_message = spark.sparkContext.parallelize([(
            "warehouse", "load", "failed", "db", table_name, current_timestamp, str(e)
        )]).toDF(["step", "process", "status", "source", "table_name", "etl_date", "error_msg"])

        raise

    finally:
        if log_message is not None:
            try:
                load_log_msg(spark, log_message)
                logging.info("ETL log inserted successfully")
            except Exception as log_err:
                logging.error(f"Failed to write log to DB: {log_err}")
