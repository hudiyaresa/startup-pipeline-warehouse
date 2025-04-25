def transform_dim_funding_round(funding_rounds_df):
    dim_funding_round = funding_rounds_df.select('funding_round_code', 'funding_round_type', 
                                                'is_first_round', 'is_last_round') \
                                         .withColumnRenamed('funding_round_code', 'funding_code') \
                                         .withColumn('funding_round_id', F.monotonically_increasing_id()) \
                                         .withColumn('is_first_round', F.col('is_first_round').cast('boolean')) \
                                         .withColumn('is_last_round', F.col('is_last_round').cast('boolean'))

    return dim_funding_round