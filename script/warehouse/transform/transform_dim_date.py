from pyspark.sql import functions as F

def transform_dim_date(dim_date_df_raw):
    dim_date_df = dim_date_df_raw \
        .withColumn("date_actual", F.to_date("date_actual", "yyyy-MM-dd")) \
        .withColumn("year", F.col("year").cast("int")) \
        .withColumn("month", F.col("month").cast("int")) \
        .withColumn("month_name", F.col("month_name")) \
        .withColumn("week", F.col("week").cast("int")) \
        .withColumn("quarter", F.col("quarter").cast("int")) \
        .withColumn("day", F.col("day").cast("int")) \
        .withColumn("day_of_week", F.col("day_of_week").cast("int")) \
        .withColumn("day_name", F.col("day_name"))

    return dim_date_df
