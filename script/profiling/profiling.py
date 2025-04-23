from pyspark.sql import SparkSession
from pyspark.sql.functions import col, isnan, when, count
from utils.helper import init_spark_session
from staging.extract.extract_data import extract_data
from datetime import datetime
import json

def profile_spark(df: pd.DataFrame) -> dict:
    spark = init_spark_session()
    report = {}
    total_rows = df.count()

    for col_name in df.columns:
        data_type = str(df.schema[col_name].dataType)
        
        # Hitung missing value (null atau kosong)
        missing_count = df.filter(col(col_name).isNull() | (col(col_name) == "")).count()
        missing_percentage = (missing_count / total_rows) * 100 if total_rows > 0 else 0

        entry = {
            "data_type": data_type,
            "percentage_missing_value": round(missing_percentage, 2)
        }

        # Hitung nilai unik (jika tidak terlalu banyak)
        unique_values = df.select(col_name).distinct().limit(5).rdd.flatMap(lambda x: x).collect()
        entry["unique_value"] = unique_values

        # Deteksi valid date
        if "date" in col_name.lower() or "at" in col_name.lower():
            try:
                valid_dates = df.withColumn("parsed", col(col_name).cast("timestamp"))
                valid_count = valid_dates.filter(col("parsed").isNotNull()).count()
                entry["percentage_valid_date"] = round((valid_count / total_rows) * 100, 2) if total_rows > 0 else 0
            except:
                entry["percentage_valid_date"] = 0.0

        report[col_name] = entry

    profile_result = {
        "person_in_charge": "Hudiya Resa",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "report": report
    }

    # take variable name in df
    df_name = [name for name, value in globals().items() if value is df][0]

    # Save as JSON
    os.makedirs("profiling/output", exist_ok=True)
    file_path = f"profiling/output/{df_name}_profile_{datetime.now().strftime('%Y%m%d')}.json"
    with open(file_path, "w") as f:
        json.dump(profile_result, f, indent=4)

    print(f"Profiling report saved to: {file_path}")
    return profile_result

df_people = extract_data(data_name="people", format_data="csv")
df_relationships = extract_data(data_name="relationships", format_data="csv")
df_acquisition = extract_data(data_name="acquisition", format_data="db")
df_funds = extract_data(data_name="funds", format_data="db")
df_funding_rounds = extract_data(data_name="funding_rounds", format_data="db")
df_company = extract_data(data_name="company", format_data="db")
df_investments = extract_data(data_name="investments", format_data="db")
df_ipos = extract_data(data_name="ipos", format_data="db")

profile_report = profile_spark(df_people) 
profile_report = profile_spark(df_relationships) 
profile_report = profile_spark(df_acquisition) 
profile_report = profile_spark(df_funds) 
profile_report = profile_spark(df_funding_rounds) 
profile_report = profile_spark(df_company) 
profile_report = profile_spark(df_investments) 
profile_report = profile_spark(df_ipos) 