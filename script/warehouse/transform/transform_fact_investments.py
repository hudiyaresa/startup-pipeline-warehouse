def transform_fact_investments(investments_df, funding_rounds_df, dim_date_df):
    # Investment data
    investments_df = investments_df.withColumn('investment_nk', F.col('investment_id')) \
                                   .withColumn('date_actual', F.to_date('created_at', 'yyyy-MM-dd')) \
                                   .join(dim_date_df, investments_df.date_actual == dim_date_df.date_actual, 'left') \
                                   .drop('date_actual') \
                                   .withColumnRenamed('date_id', 'date_id')

    # Join with funding rounds
    investments_df = investments_df.join(funding_rounds_df, investments_df.funding_round_id == funding_rounds_df.funding_round_id, 'left') \
                                   .select('investment_nk', 'investor_object_id', 'funded_object_id', 'funding_round_id', 
                                           'date_id', 'investment_amount_usd')

    return investments_df