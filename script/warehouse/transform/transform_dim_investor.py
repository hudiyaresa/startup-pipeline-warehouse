def transform_dim_investor(investments_df):
    dim_investor = investments_df.select('investor_object_id').distinct() \
                                 .withColumnRenamed('investor_object_id', 'investor_nk') \
                                 .withColumn('investor_id', F.monotonically_increasing_id())

    return dim_investor