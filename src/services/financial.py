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

    def get_financial_summary(self, month: int, year: int = 2026) -> pd.DataFrame:
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
        segment_df.columns = ['Segmento', 'Receita_Esperada']
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
            "marketing": custos_base.get("Marketing", 0.0), # Extrato para o cálculo de CAC
            "details": df_details
        }
        
    def calculate_ltv(self, df_all: pd.DataFrame) -> float:
        """
        LTV = (Tempo Médio de Permanência dos alunos inativos) * (Ticket Médio atual)
        """
        if df_all is None or df_all.empty:
            return 0.0
            
        # 1. Isola inativos que tenham datas consistentes
        df_inativos = df_all[(df_all['status'] == 'Inativo') & df_all['entry_date'].notna() & df_all['exit_date'].notna()].copy()
        
        if df_inativos.empty:
            return 0.0
            
        # 2. Calcula tempo de permanência em meses (aprox 30.44 dias)
        df_inativos['tenure_months'] = (df_inativos['exit_date'] - df_inativos['entry_date']).dt.days / 30.44
        avg_tenure = df_inativos['tenure_months'].mean()
        
        # 3. Pega o ticket médio atual
        df_ativos = df_all[df_all['status'] == 'Ativo']
        if df_ativos.empty:
            return 0.0
            
        ticket_medio = df_ativos['net_tuition'].mean()
        
        ltv = avg_tenure * ticket_medio
        return float(ltv) if pd.notna(ltv) else 0.0

    def calculate_cac(self, df_all: pd.DataFrame, marketing_budget: float) -> float:
        """
        CAC = Investimento em Marketing / Matrículas do ano atual
        """
        if df_all is None or df_all.empty or marketing_budget <= 0:
            return 0.0
            
        current_year = datetime.now().year
        
        # Alunos matriculados este ano
        novos_alunos = df_all[df_all['entry_date'].dt.year == current_year]
        qtd_novos = len(novos_alunos)
        
        if qtd_novos == 0:
            return 0.0 # Sem conversões, cálculo impossível ou infinito
            
        return float(marketing_budget / qtd_novos)

    def get_financial_forecasting(self, df_active: pd.DataFrame, months: int = 6, delinquency_rate: float = 0.05) -> pd.DataFrame:
        """
        Gera os dados de projeção para os próximos meses baseados na receita ativa.
        """
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