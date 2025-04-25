def transform_fact_company_growth(acquisition_df, funding_rounds_df, ipos_df, company_df, dim_date_df):
    # Acquisition data
    acquisition_df = acquisition_df.withColumn('company_nk', F.col('acquired_object_id')) \
                                    .withColumn('date_actual', F.to_date('acquired_at', 'yyyy-MM-dd')) \
                                    .join(dim_date_df, acquisition_df.date_actual == dim_date_df.date_actual, 'left') \
                                    .drop('date_actual') \
                                    .withColumnRenamed('date_id', 'date_id') \
                                    .groupBy('company_nk', 'date_id') \
                                    .agg(F.count('acquisition_id').alias('acquisition_count'))

    # Funding rounds data
    funding_rounds_df = funding_rounds_df.withColumn('company_nk', F.col('object_id')) \
                                         .groupBy('company_nk') \
                                         .agg(F.sum('raised_amount_usd').alias('total_funding_usd'))

    # IPO data
    ipos_df = ipos_df.withColumn('company_nk', F.col('object_id')) \
                     .withColumn('ipo_valuation_usd', F.col('valuation_amount').cast('float')) \
                     .withColumn('ipo_raised_amount_usd', F.col('raised_amount').cast('float'))

    # Join all data for fact_company_growth
    fact_company_growth = acquisition_df.join(funding_rounds_df, 'company_nk', 'left') \
                                        .join(ipos_df, 'company_nk', 'left') \
                                        .join(company_df, 'company_nk', 'left') \
                                        .select('company_nk', 'date_id', 'acquisition_count', 
                                                'total_funding_usd', 'ipo_valuation_usd', 'ipo_raised_amount_usd')

    return fact_company_growth