def transform_dim_company(company_df):
    dim_company = company_df.select('object_id', 'region', 'city', 'country_code', 'latitude', 'longitude') \
                            .withColumnRenamed('object_id', 'company_nk') \
                            .withColumn('company_id', F.monotonically_increasing_id())

    return dim_company