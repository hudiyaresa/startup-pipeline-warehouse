from utils.helper import logging_process, init_spark_session, load_log_msg
import logging
import pyspark
from datetime import datetime

logging_process()


def extract_data(data_name: str, format_data: str) -> pyspark.sql.DataFrame:
    spark = init_spark_session()
    current_timestamp = datetime.now()
    log_message = None

    # DB config
    DB_HOST = "pipeline_db"
    DB_PORT = "5432"
    DB_NAME = "staging"
    DB_USER = "postgres"
    DB_PASS = "cobapassword"

    jdbc_url = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"

    connection_properties = {
        "user": DB_USER,
        "password": DB_PASS,
        "driver": "org.postgresql.Driver"
    }

    try:
        logging.info(f"===== Start Extracting {data_name} data =====")

        if format_data.lower() == "csv":
            df = spark.read.csv(f"data/{data_name}.csv", header=True)

        elif format_data.lower() == "db":
            df = spark.read.jdbc(
                url=jdbc_url,
                table=data_name,
                properties=connection_properties
            )

        else:
            raise ValueError("Format data not supported yet")

        logging.info(f"===== Finish Extracting {data_name} data =====")

        # Log success
        log_message = spark.sparkContext.parallelize([(
            "staging", "extract", "success", format_data, data_name, current_timestamp
        )]).toDF(["step", "process", "status", "source", "table_name", "etl_date"])

        return df

    except Exception as e:
        logging.error("====== Failed to Extract Data ======")
        logging.error(str(e))

        # Log failure
        log_message = spark.sparkContext.parallelize([(
            "staging", "extract", "failed", format_data, data_name, current_timestamp, str(e)
        )]).toDF(["step", "process", "status", "source", "table_name", "etl_date", "error_msg"])

        raise

    finally:
        if log_message:
            try:
                load_log_msg(spark, log_message)
            except Exception as log_err:
                logging.error(f"Failed to write log to DB: {log_err}")
