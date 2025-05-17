from pyspark.sql import functions as F

def transform_dim_date(dim_date_df_raw):
    dim_date_df = dim_date_df_raw \
        .withColumn("date_id", F.col("date_id").cast("int")) \
        .withColumn("date_actual", F.to_date("date_actual", "yyyy-MM-dd")) \
        .withColumn("day_of_year", F.col("day_of_year").cast("int")) \
        .withColumn("week_of_month", F.col("week_of_month").cast("int")) \
        .withColumn("week_of_year", F.col("week_of_year").cast("int")) \
        .withColumn("month_actual", F.col("month_actual").cast("int")) \
        .withColumn("quarter_actual", F.col("quarter_actual").cast("int")) \
        .withColumn("year_actual", F.col("year_actual").cast("int")) \
        .withColumn("first_day_of_week", F.to_date("first_day_of_week", "yyyy-MM-dd")) \
        .withColumn("last_day_of_week", F.to_date("last_day_of_week", "yyyy-MM-dd")) \
        .withColumn("first_day_of_month", F.to_date("first_day_of_month", "yyyy-MM-dd")) \
        .withColumn("last_day_of_month", F.to_date("last_day_of_month", "yyyy-MM-dd")) \
        .withColumn("first_day_of_quarter", F.to_date("first_day_of_quarter", "yyyy-MM-dd")) \
        .withColumn("last_day_of_quarter", F.to_date("last_day_of_quarter", "yyyy-MM-dd")) \
        .withColumn("first_day_of_year", F.to_date("first_day_of_year", "yyyy-MM-dd")) \
        .withColumn("last_day_of_year", F.to_date("last_day_of_year", "yyyy-MM-dd"))

    return dim_date_df
