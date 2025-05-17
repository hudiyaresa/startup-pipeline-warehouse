import logging

# Initialize logging
logging_process()

if __name__ == "__main__":
    logging.info("===== Start Banking Data Pipeline =====")

    try:
        # Extract data from CSV and database
        df_people = extract_data(data_name="people", format_data="csv")
        df_relationships = extract_data(data_name="relationships", format_data="csv")
        df_acquisition = extract_data(data_name="acquisition", format_data="db")
        df_funds = extract_data(data_name="funds", format_data="db")
        df_funding_rounds = extract_data(data_name="funding_rounds", format_data="db")
        df_company = extract_data(data_name="company", format_data="db")
        df_investments = extract_data(data_name="investments", format_data="db")
        df_ipos = extract_data(data_name="ipos", format_data="db")
        
        # Extract API
        # URL API and date (20 years back)
        url = "https://api-milestones.vercel.app/api/data"
        start_date = "1994-01-01"
        end_date = "2014-01-01"

        # extract API
        df_milestones = extract_api_per_year(spark, url, start_date, end_date)        
        
        # dim_date_df = extract_data("dim_date", "csv") -> di warehouse


        # Load each transformed dataset into the data warehouse
        load_data(df_people, table_name="people")
        load_data(df_relationships, table_name="relationships")
        load_data(df_acquisition, table_name="acquisition")
        load_data(df_funds, table_name="funds")
        load_data(df_funding_rounds, table_name="funding_rounds")
        load_data(df_company, table_name="company")
        load_data(df_investments, table_name="investments")
        load_data(df_ipos, table_name="ipos")
        load_data(df_milestones, table_name="milestones")

        logging.info("===== Finish Investment Data Pipeline =====")

    except Exception as e:
        logging.error("===== Data Pipeline Failed =====")
        logging.error(e)
        raise




        # Transform each dataset separately
        # df_transactions = transform_data(df_transactions, "transactions")