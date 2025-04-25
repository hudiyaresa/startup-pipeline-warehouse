from warehouse.extract.extract_data import extract_data
from warehouse.transform.transform_dim_company import transform_dim_company
from warehouse.transform.transform_dim_funding_round import transform_dim_funding_round
from warehouse.transform.transform_dim_investor import transform_dim_investor
from warehouse.transform.transform_dim_date import transform_dim_date
from warehouse.transform.transform_fact_company_growth import transform_fact_company_growth
from warehouse.transform.transform_fact_investments import transform_fact_investments


def warehouse_pipeline():
    fact_company_growth = transform_fact_company_growth(acquisition_df, funding_rounds_df, ipos_df, company_df, dim_date_df)
    fact_investments = transform_fact_investments(investments_df, funding_rounds_df, dim_date_df)
    dim_company = transform_dim_company(company_df)
    dim_investor = transform_dim_investor(investments_df)
    dim_funding_round = transform_dim_funding_round(funding_rounds_df)
    dim_date = transform_dim_date(dim_date_df)

    # Now load these DataFrames to your warehouse (e.g., PostgreSQL, etc.)
    # Here we would write the DataFrames to tables using Spark's JDBC connector or any other method
    fact_company_growth.write.jdbc(url="jdbc:postgresql://host:port/db", table="fact_company_growth", mode="overwrite")
    fact_investments.write.jdbc(url="jdbc:postgresql://host:port/db", table="fact_investments", mode="overwrite")
    dim_company.write.jdbc(url="jdbc:postgresql://host:port/db", table="dim_company", mode="overwrite")
    dim_investor.write.jdbc(url="jdbc:postgresql://host:port/db", table="dim_investor", mode="overwrite")
    dim_funding_round.write.jdbc(url="jdbc:postgresql://host:port/db", table="dim_funding_round", mode="overwrite")
    dim_date.write.jdbc(url="jdbc:postgresql://host:port/db", table="dim_date", mode="overwrite")

# Running the warehouse pipeline process
warehouse_pipeline()