import os
from src.config import DATABASE_URL, DATA_DIR
import pandas as pd
from sqlalchemy import create_engine


def get_db_engine():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the .env file")
    return create_engine(DATABASE_URL)

def clean_currency(value_str):
    if pd.isna(value_str):
        return 0.0
    cleaned = str(value_str).replace('R$','').replace(' ','').replace('.','').replace(',','').replace(',','.')
    return float(cleaned)

def clean_percentage(value_str):
    if pd.isna(value_str):
        return 0.0
    cleaned = str(value_str).replace('%','').replace(',','.')
    return float(cleaned)

def run_etl():
    print("Starting ETL pipeline")

    # 1. EXTRACT
    df_annual = pd.read_csv(data_dir / "metas_anuais.csv")
    df_monthly = pd.read_csv(data_dir / "metas_mensais.csv")
    df_sellers = pd.read_csv(data_dir / "metas_vendedores.csv")
    print("Raw CSV files extracted")

    # 2. TRANSFORM
    # 2.1 Annual Targets
    df_annual["totalPrevistoAno"] = df_annual["totalPrevistoAno"].apply(clean_currency)
    df_annual["totalRealizadoAno"] = df_annual["totalRealizadoAno"].apply(clean_currency)
    df_annual["metaConcluidaPorcentagem"] = df_annual["metaConcluidaPorcentagem"].apply(
        clean_percentage
    )
    df_annual = df_annual.rename(
        columns={
            "id": "source_id",
            "tipo": "category",
            "totalPrevistoAno": "predicted_total_year",
            "totalRealizadoAno": "realized_total_year",
            "metaConcluidaPorcentagem": "completion_percentage",
        }
    )

    # 2.2 Monthly Targets
    df_monthly["previstoMes"] = df_monthly["previstoMes"].apply(clean_currency)
    df_monthly["realizadoMes"] = df_monthly["realizadoMes"].apply(clean_currency)
    df_monthly["concluidoMesPorcentagem"] = df_monthly["concluidoMesPorcentagem"].apply(
        clean_percentage
    )
    df_monthly = df_monthly.rename(
        columns={
            "id": "source_id",
            "tipo": "category",
            "previstoMes": "predicted_month",
            "realizadoMes": "realized_month",
            "concluidoMesPorcentagem": "completion_percentage",
            "mes": "month_name",
            "nMes": "month_number",
        }
    )
    df_monthly["month_number"] = df_monthly["month_number"].astype(int)

    # 2.3 Seller Performance
    df_sellers["concluidoMesPorcentagem"] = df_sellers["concluidoMesPorcentagem"].apply(
        clean_percentage
    )
    df_sellers = df_sellers.rename(
        columns={
            "id": "source_id",
            "vendedor": "seller_name",
            "concluidoMesPorcentagem": "completion_percentage",
            "mes": "month_name",
            "nMes": "month_number",
        }
    )
    df_sellers["month_number"] = df_sellers["month_number"].astype(int)
    print("Data cleaned and schema standardized to English.")

    # 3. LOAD
    engine = get_db_engine()
    print("Connected to PostgreSQL")

    df_annual.to_sql("annual_targets", engine, if_exists="replace", index=False)
    df_monthly.to_sql("monthly_targets", engine, if_exists="replace", index=False)
    df_sellers.to_sql("seller_performance", engine, if_exists="replace", index=False)

    print("ETL completed successfully")

if __name__ == "__main__":
    run_etl()




