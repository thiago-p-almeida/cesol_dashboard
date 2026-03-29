import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from src.schemas.student_schema import StudentSchema, COLUMN_MAP

# Carrega variáveis de ambiente
load_dotenv()

class DataIngestionService:
    def __init__(self):
        # Inicializa a conexão com o banco de dados PostgreSQL.
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL não encontrada no arquivo .env")
        self.engine = create_engine(db_url)

    def _normalization_layer(self, df: pd.DataFrame) -> pd.DataFrame:
        
        # Camada de Limpeza (Data Quality): Converte variações de nomes 
        # para a nova taxonomia enxuta aprovada (Phase 2).
        
        # Mapeamento de 'sujeira' para o padrão enxuto
        cleanup_map = {
            "Educação Infantil": "Ed. Infantil",
            "Ensino Fundamental I": "Fundamental I",
            "Ensino Fundamental": "Fundamental I",
            "Fundamental": "Fundamental I",
            "Ensino Fundamental II": "Fundamental II"
        }
        
        # 1. Normalização básica: remove espaços e garante tipo string
        df['segment'] = df['segment'].astype(str).str.strip()
        
        # 2. Aplicação da substituição baseada no mapa
        df['segment'] = df['segment'].replace(cleanup_map)
        
        return df

    def process_students_csv(self, file_content, file_name):
        # Processa, normaliza e valida a entrada de novos alunos.
        # Carrega apenas as colunas necessárias mapeadas no schema
        df = pd.read_csv(file_content, usecols=COLUMN_MAP.keys())
        
        # Etapa 1: Normalização (Transformação)
        # Transforma "Ensino Fundamental" em "Fundamental I" etc.
        df = self._normalization_layer(df)
        
        # Etapa 2: Validação Estrita (Pandera)
        # O StudentSchema (Phase 1) garante que o dado agora está limpo
        validated_df = StudentSchema.validate(df)
        
        # Etapa 3: Carga (Load) para o PostgreSQL
        # append: adiciona novos alunos sem apagar os existentes
        validated_df.to_sql('students', self.engine, if_exists='append', index=False)
        
        return f"Sucesso! {len(validated_df)} registros importados e normalizados."