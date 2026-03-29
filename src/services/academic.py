import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class AcademicService:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL não encontrada no .env")
        self.engine = create_engine(db_url)

    def get_active_students_df(self) -> pd.DataFrame:
        query = "SELECT * FROM students WHERE status = 'Ativo'"
        df = pd.read_sql(query, self.engine)
        
        if not df.empty:
            df['net_tuition'] = df['full_tuition'] - df['discount_value'] - df['scholarship_value']
        return df

    def get_churn_analysis(self) -> dict:
        query = "SELECT * FROM students"
        df = pd.read_sql(query, self.engine)
        
        if df.empty:
            return {"churn_rate": 0, "total_ativos": 0, "total_inativos": 0, "reasons_df": pd.DataFrame()}
        
        total_historico = len(df)
        ativos = len(df[df['status'] == 'Ativo'])
        inativos = len(df[df['status'] == 'Inativo'])
        
        churn_rate = (inativos / total_historico) * 100 if total_historico > 0 else 0
        
        reasons_df = df[df['status'] == 'Inativo']['exit_reason'].value_counts().reset_index()
        if not reasons_df.empty:
            reasons_df.columns = ['Motivo', 'Quantidade']
        else:
            reasons_df = pd.DataFrame(columns=['Motivo', 'Quantidade'])
        
        return {
            "churn_rate": churn_rate,
            "total_ativos": ativos,
            "total_inativos": inativos,
            "reasons_df": reasons_df
        }