import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

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
        """
        Camada de Limpeza (Data Quality): Converte variações de nomes 
        para a nova taxonomia enxuta aprovada e formata datas.
        """
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
        from src.schemas.student_schema import StudentSchema, COLUMN_MAP
        
        # 1. Lê o CSV esperando as colunas em Português-BR
        df = pd.read_csv(file_content, usecols=COLUMN_MAP.keys())
        
        # 2. TRADUÇÃO MÁGICA: Renomeia de PT-BR para EN
        # Ex: "mensalidade" vira "full_tuition" silenciosamente
        df = df.rename(columns=COLUMN_MAP)
        
        # 3. PARSING DE DATAS (Resiliência para formato BR)
        if 'birth_date' in df.columns:
            # Converte string DD/MM/YYYY para datetime. 
            # errors='coerce' transforma datas inválidas (ex: 31/02/2026) em NaT
            df['birth_date'] = pd.to_datetime(df['birth_date'], format='%d/%m/%Y', errors='coerce')
            
            # Filtro de Qualidade: Remove linhas onde a data de nascimento ficou inválida (NaT)
            # Isso impede que o banco de dados ou o Pandera quebrem
            df = df.dropna(subset=['birth_date'])
        
        # 4. Normalização (Transforma "Ensino Fundamental" em "Fundamental I")
        df = self._normalization_layer(df)
        
        # 5. Validação Estrita (Pandera valida as colunas já em Inglês e com datas corretas)
        validated_df = StudentSchema.validate(df)
        
        # 6. Carga no PostgreSQL
        validated_df.to_sql('students', self.engine, if_exists='append', index=False)
        
        return f"Sucesso! {len(validated_df)} registros importados e normalizados."