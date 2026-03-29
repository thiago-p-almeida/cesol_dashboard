import io
import pandas as pd

class ExportService:
    def to_excel(self, df: pd.DataFrame, sheet_name: str = 'Exportacao') -> bytes:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        return output.getvalue()