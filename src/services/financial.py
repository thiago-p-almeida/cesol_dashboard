import os
import json
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class FinancialService:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL não encontrada no .env")
        self.engine = create_engine(db_url)

    def get_financial_summary(self, month: int, year: int = 2024) -> pd.DataFrame:
        query = f"""
            SELECT status, SUM(amount) as total
            FROM financial_transactions
            WHERE type = 'Receita' AND category = 'Mensalidade'
              AND EXTRACT(MONTH FROM reference_date) = {month}
              AND EXTRACT(YEAR FROM reference_date) = {year}
            GROUP BY status
        """
        return pd.read_sql(query, self.engine)

    def get_revenue_by_segment(self, df_active: pd.DataFrame) -> pd.DataFrame:
        if df_active.empty:
            return pd.DataFrame(columns=['Segmento', 'Receita_Esperada'])
        
        segment_df = df_active.groupby('segment')['net_tuition'].sum().reset_index()
        segment_df.columns =['Segmento', 'Receita_Esperada']
        return segment_df.sort_values(by='Receita_Esperada', ascending=False)

    def get_expenses_summary(self) -> dict:
        config_path = Path(__file__).resolve().parent.parent.parent / "config" / "expenses.json"
        
        custos_base = {
            "Aluguel": 15000.00,
            "Folha de Pagamento": 45000.00,
            "Manutenção/Limpeza": 5000.00,
            "Marketing": 2000.00,
            "Software/Sistemas": 1500.00
        }

        try:
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if isinstance(data, dict) and data:
                        custos_base = {str(k): float(v) for k, v in data.items()}
        except Exception:
            pass

        df_details = pd.DataFrame([{"categoria": k, "valor": v} for k, v in custos_base.items()])
        total_despesas = sum(custos_base.values())

        return {
            "total_despesas": total_despesas,
            "aluguel": custos_base.get("Aluguel", 0.0),
            "folha": custos_base.get("Folha de Pagamento", 0.0),
            "details": df_details
        }

    def get_financial_forecasting(self, df_active: pd.DataFrame, months: int = 6, delinquency_rate: float = 0.05) -> pd.DataFrame:
        if df_active is None or df_active.empty:
            return pd.DataFrame(columns=["Mês", "Receita Bruta", "Receita Projetada (Líquida)", "Risco de Inadimplência"])
            
        monthly_revenue = df_active['net_tuition'].sum()
        current_date = datetime.now()
        forecast_data =[]
        
        for i in range(1, months + 1):
            target_date = current_date + pd.DateOffset(months=i)
            expected_revenue = monthly_revenue * (1 - delinquency_rate)
            risk_value = monthly_revenue * delinquency_rate
            
            forecast_data.append({
                "Mês": target_date.strftime('%b/%Y'),
                "Receita Bruta": monthly_revenue,
                "Receita Projetada (Líquida)": expected_revenue,
                "Risco de Inadimplência": risk_value
            })
            
        return pd.DataFrame(forecast_data)