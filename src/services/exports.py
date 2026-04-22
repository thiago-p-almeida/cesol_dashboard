import io
import pandas as pd
from pathlib import Path
import logging

class ExportService:
    def __init__(self):
        # Define o diretório raiz de exportação para o Evidence consumir
        self.analytics_dir = Path(__file__).resolve().parent.parent.parent / "data" / "analytics"
        self._ensure_directories()

    def _ensure_directories(self):
        """Garante que a estrutura de pastas dos contratos de dados exista."""
        self.analytics_dir.mkdir(parents=True, exist_ok=True)

    def to_excel(self, df: pd.DataFrame, sheet_name: str = 'Exportacao') -> bytes:
        """Exportação legado em Excel para o usuário final."""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        return output.getvalue()

    def publish_data_contract(self, df: pd.DataFrame, contract_name: str) -> str:
        """
        Publica um DataFrame como um arquivo Parquet (Contrato de Dados).
        Utiliza compressão 'snappy' padrão do ecossistema Big Data.
        """
        if df is None or df.empty:
            logging.warning(f"Tentativa de publicar contrato '{contract_name}' vazio.")
            return ""

        file_path = self.analytics_dir / f"{contract_name}.parquet"
        
        try:
            # PyArrow é o motor mais rápido e seguro para integração com DuckDB
            df.to_parquet(file_path, engine='pyarrow', compression='snappy', index=False)
            logging.info(f"Contrato de Dados '{contract_name}' publicado com sucesso em {file_path}")
            return str(file_path)
        except Exception as e:
            logging.error(f"Erro ao publicar contrato Parquet: {e}")
            raise e