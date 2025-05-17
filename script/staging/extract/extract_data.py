from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DateType, IntegerType
from utils.helper import logging_process, init_spark_session, load_log_msg
from datetime import datetime
import logging
import pyspark
import requests

logging_process()
spark = init_spark_session()

def extract_data(data_name: str, format_data: str) -> pyspark.sql.DataFrame:

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
            "sources", "extract", "failed", format_data, data_name, current_timestamp, str(e)
        )]).toDF(["step", "process", "status", "source", "table_name", "etl_date", "error_msg"])

        raise

    finally:
        if log_message:
            try:
                load_log_msg(spark, log_message)
            except Exception as log_err:
                logging.error(f"Failed to write log to DB: {log_err}")

spark = init_spark_session()
logging_process()

def extract_api_per_year(spark: pyspark.sql.SparkSession, url: str, start_date: str, end_date: str) -> pyspark.sql.DataFrame:
    current_timestamp = datetime.now()
    log_message = None

    try:
        start_year = datetime.strptime(start_date, "%Y-%m-%d").year
        end_year = datetime.strptime(end_date, "%Y-%m-%d").year

        all_dataframes = []
        logging.info(f"===== Start Extracting data from API: {url} for the period {start_date} to {end_date} =====")

        for year in range(start_year, end_year + 1):
            year_start_date = f"{year}-01-01"
            year_end_date = f"{year + 1}-01-01"

            year_url = f"{url}?start_date={year_start_date}&end_date={year_end_date}"

            try:
                response = requests.get(year_url)
                response.raise_for_status()
                data_json = response.json()

                if isinstance(data_json, list) and data_json:
                    # Convert list of dict directly to RDD then to DataFrame
                    rdd = spark.sparkContext.parallelize(data_json)

                    schema = StructType([
                        StructField("created_at", StringType(), True),
                        StructField("description", StringType(), True),
                        StructField("milestone_at", StringType(), True),
                        StructField("milestone_code", StringType(), True),
                        StructField("milestone_id", IntegerType(), True),
                        StructField("object_id", StringType(), True),
                        StructField("source_description", StringType(), True),
                        StructField("source_url", StringType(), True),
                        StructField("updated_at", StringType(), True),
                    ])

                    df = spark.createDataFrame(rdd, schema=schema)

                    # Cast string datetime to proper Spark types
                    df = df.select(
                        F.col("milestone_id").cast(IntegerType()).alias("milestone_id"),
                        F.to_timestamp("created_at").alias("created_at"),
                        F.col("description"),
                        F.to_date("milestone_at").alias("milestone_at"),
                        F.col("milestone_code"),
                        F.col("object_id"),
                        F.col("source_description"),
                        F.col("source_url"),
                        F.to_timestamp("updated_at").alias("updated_at")
                    )

                    all_dataframes.append(df)
                else:
                    logging.warning(f"No data returned for the year {year}")

            except Exception as e:
                logging.error(f"Failed to fetch data for {year}: {e}")

        if not all_dataframes:
            raise ValueError("No data was successfully fetched from the API.")

        final_df = all_dataframes[0]
        for df in all_dataframes[1:]:
            final_df = final_df.unionByName(df)

        log_message = spark.sparkContext.parallelize([(
            "api", "extract", "success", "api", "data", current_timestamp
        )]).toDF(["step", "process", "status", "source", "table_name", "etl_date"])

        logging.info(f"===== Finished Extracting data from API =====")
        return final_df

    except Exception as e:
        logging.error("===== Failed to Extract Data from API =====")
        logging.error(str(e))
        log_message = spark.sparkContext.parallelize([(
            "api", "extract", "failed", "api", "data", current_timestamp, str(e)
        )]).toDF(["step", "process", "status", "source", "table_name", "etl_date", "error_msg"])
        raise

    finally:
        if log_message:
            try:
                load_log_msg(spark, log_message)
            except Exception as log_err:
                logging.error(f"Failed to write log to DB: {log_err}")
