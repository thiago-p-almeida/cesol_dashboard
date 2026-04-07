import os
import json
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class AcademicService:
    def __init__(self):
        # 1. Inicialização do Banco de Dados
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL não encontrada no .env")
        self.engine = create_engine(
            db_url,
            pool_pre_ping=True,  # Checa se a conexão está viva antes de usar
            pool_recycle=1800    # Recicla conexões a cada 30 minutos
)

        # 2. Leitura de Configuração de Capacidade (config/academic.json)
        self.config_path = Path(__file__).resolve().parent.parent.parent / "config" / "academic.json"
        self.capacity_config = self._load_capacity_config()

    def _load_capacity_config(self) -> dict:
        """Lê as capacidades do JSON com fallback de segurança."""
        default_config = {
            "total_capacity": 500,
            "capacity_infantil": 100,
            "capacity_fund1": 250,
            "capacity_fund2": 150
        }
        try:
            if self.config_path.exists():
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Erro ao ler academic.json: {e}. Usando padrão.")
        return default_config

    def get_active_students_df(self) -> pd.DataFrame:
        query = "SELECT * FROM students WHERE status = 'Ativo'"
        with self.engine.connect() as conn:
            df = pd.read_sql(query, conn)
            
        if not df.empty:
            df['net_tuition'] = df['full_tuition'] - df['discount_value'] - df['scholarship_value']
            df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
        return df

    def get_all_students_df(self) -> pd.DataFrame:
        query = "SELECT * FROM students"
        with self.engine.connect() as conn:
            df = pd.read_sql(query, conn)
            
        if not df.empty:
            df['net_tuition'] = df['full_tuition'] - df['discount_value'] - df['scholarship_value']
            df['entry_date'] = pd.to_datetime(df['entry_date'], errors='coerce')
            df['exit_date'] = pd.to_datetime(df['exit_date'], errors='coerce')
            df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
        return df

    def get_pedagogical_insights(self, df_all: pd.DataFrame) -> dict:
        """
        Calcula a Distorção Idade-Série (Alunos com 2+ anos acima da idade base).
        """
        if df_all is None or df_all.empty:
            return {"distortion_rate": 0.0, "distortion_by_grade": pd.DataFrame()}

        # Mapeamento de Idade Base (Referência 2026)
        age_map = {
            "Maternal": 3, "Jardim I": 4, "Jardim II": 5,
            "1º Ano": 6, "2º Ano": 7, "3º Ano": 8, "4º Ano": 9, "5º Ano": 10,
            "6º Ano": 11, "7º Ano": 12, "8º Ano": 13, "9º Ano": 14
        }

        # Filtra apenas alunos ativos com data de nascimento válida
        df = df_all[df_all['status'] == 'Ativo'].copy()
        df = df.dropna(subset=['birth_date', 'grade'])

        if df.empty:
            return {"distortion_rate": 0.0, "distortion_by_grade": pd.DataFrame()}

        # Cálculo vetorizado da idade (Contexto: 2026)
        df['current_age'] = 2026 - df['birth_date'].dt.year
        
        # Identifica distorção: Idade atual > (Idade Base + 2 anos)
        df['base_age'] = df['grade'].map(age_map)
        df['is_distorted'] = df['current_age'] > (df['base_age'] + 2)

        total_ativos = len(df)
        total_distorcidos = df['is_distorted'].sum()
        distortion_rate = (total_distorcidos / total_ativos) * 100 if total_ativos > 0 else 0

        # Agrupamento para o gráfico
        dist_by_grade = df[df['is_distorted']].groupby('grade').size().reset_index(name='Alunos Atrasados')

        return {
            "distortion_rate": round(distortion_rate, 1),
            "distortion_by_grade": dist_by_grade
        }

    def get_occupancy_metrics(self, df_active: pd.DataFrame) -> dict:
        """
        Calcula a Taxa de Ocupação cruzando Ativos vs Capacidade do JSON.
        """
        if df_active is None or df_active.empty:
            return {"global_occupancy": 0.0, "occupancy_df": pd.DataFrame()}

        # Mapeamento Segmento -> Chave do JSON
        mapping = {
            "Ed. Infantil": "capacity_infantil",
            "Fundamental I": "capacity_fund1",
            "Fundamental II": "capacity_fund2"
        }

        # Contagem de ativos por segmento
        counts = df_active['segment'].value_counts().to_dict()
        
        occupancy_data = []
        total_ativos = 0
        
        for segment, json_key in mapping.items():
            ativos = counts.get(segment, 0)
            capacidade = self.capacity_config.get(json_key, 1) # Evita div por zero
            vagas_restantes = max(0, capacidade - ativos)
            
            total_ativos += ativos
            occupancy_data.append({
                "Segmento": segment,
                "Ativos": ativos,
                "Capacidade": capacidade,
                "Vagas Restantes": vagas_restantes,
                "Taxa %": round((ativos / capacidade) * 100, 1)
            })

        global_cap = self.capacity_config.get("total_capacity", 1)
        global_rate = (total_ativos / global_cap) * 100

        return {
            "global_occupancy": round(global_rate, 1),
            "occupancy_df": pd.DataFrame(occupancy_data)
        }

    def get_class_density(self, df_active: pd.DataFrame) -> float:
        """Calcula a média arredondada de alunos por turma."""
        if df_active is None or df_active.empty:
            return 0.0
        
        group_cols = ['grade', 'classroom'] if 'classroom' in df_active.columns else ['grade']
        density = df_active.groupby(group_cols).size().mean()
        return round(float(density), 1) if pd.notna(density) else 0.0

    def get_churn_analysis(self) -> dict:
        df = self.get_all_students_df()
        if df.empty:
            return {"churn_rate": 0, "total_ativos": 0, "total_inativos": 0, "reasons_df": pd.DataFrame()}
        
        total_historico = len(df)
        ativos = len(df[df['status'] == 'Ativo'])
        inativos = len(df[df['status'] == 'Inativo'])
        churn_rate = (inativos / total_historico) * 100 if total_historico > 0 else 0
        
        reasons_df = df[df['status'] == 'Inativo']['exit_reason'].value_counts().reset_index()
        reasons_df.columns = ['Motivo', 'Quantidade'] if not reasons_df.empty else ['Motivo', 'Quantidade']
        
        return {
            "churn_rate": churn_rate,
            "total_ativos": ativos,
            "total_inativos": inativos,
            "reasons_df": reasons_df
        }