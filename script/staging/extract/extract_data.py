from utils.helper import logging_process, init_spark_session, load_log_msg
from datetime import datetime
import logging
import pyspark

logging_process()


def extract_data(data_name: str, format_data: str) -> pyspark.sql.DataFrame:
    spark = init_spark_session()

    DB_URL = "jdbc:postgresql://source_db:5432/startup_investments"
    DB_USER = "postgres"
    DB_PASS = "cobapassword"

    jdbc_url = DB_URL
    connection_properties = {
        "user": DB_USER,
        "password": DB_PASS,
        "driver": "org.postgresql.Driver"
    }

    current_timestamp = datetime.now()
    log_message = None

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
            "sources", "extract", "success", format_data, data_name, current_timestamp
        )]).toDF(["step", "process", "status", "source", "table_name", "etl_date"])

        return df

    except Exception as e:
        logging.error("====== Failed to Extract Data ======")
        logging.error(str(e))

        # Log failure
        log_message = spark.sparkContext.parallelize([(
            "sources", "extraction", "failed", format_data, data_name, current_timestamp, str(e)
        )]).toDF(["step", "process", "status", "source", "table_name", "etl_date", "error_msg"])

        raise

    finally:
        if log_message:
            try:
                load_log_msg(spark, log_message)
            except Exception as log_err:
                logging.error(f"Failed to write log to DB: {log_err}")
