from warehouse.extract.extract_data import extract_data
from warehouse.transform.transform_dim_company import transform_dim_company
from warehouse.transform.transform_dim_funding_round import transform_dim_funding_round
from warehouse.transform.transform_dim_investor import transform_dim_investor
from warehouse.transform.transform_dim_date import transform_dim_date
from warehouse.transform.transform_fact_company_growth import transform_fact_company_growth
from warehouse.transform.transform_fact_investments import transform_fact_investments

if __name__ == "__main__":

    # Initialize logging
    logging_process()

    def warehouse_pipeline():
        dim_date_df = extract_data("dim_date", "csv")
        acquisition_df = extract_data("acquisition", "db")
        funding_rounds_df = extract_data("funding_rounds", "db")
        ipos_df = extract_data("ipos", "db")
        company_df = extract_data("company", "db")
        investments_df = extract_data("investments", "db")
        milestones_df = extract_data("milestones", "db")

        fact_company_growth = transform_fact_company_growth(acquisition_df, funding_rounds_df, ipos_df, company_df, dim_date_df)
        fact_investments = transform_fact_investments(investments_df, funding_rounds_df, dim_date_df)
        dim_company = transform_dim_company(company_df)
        dim_investor = transform_dim_investor(investments_df)
        dim_funding_round = transform_dim_funding_round(funding_rounds_df)
        dim_date = transform_dim_date(dim_date_df)

        # Load DataFrames to warehouse
        load_data(dim_date, table_name="dim_date")
        load_data(dim_company, table_name="dim_company")
        load_data(dim_investor, table_name="dim_investor")
        load_data(dim_funding_round, table_name="dim_funding_round")
        load_data(fact_investments, table_name="fact_investments")
        load_data(fact_company_growth, table_name="fact_company_growth")

    # Running the warehouse pipeline process
    warehouse_pipeline()