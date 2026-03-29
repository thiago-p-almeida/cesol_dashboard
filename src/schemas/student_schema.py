import pandera as pa
from pandera import Column, Check

# ==========================================
# 1. A FONTE DA VERDADE: TAXONOMIA ACADÊMICA
# ==========================================
# Centralizamos as regras de negócio aqui. 
# Qualquer mudança na estrutura da escola, altera-se apenas este dicionário.
ACADEMIC_TAXONOMY = {
    "Ed. Infantil": ["Maternal", "Jardim I", "Jardim II"],
    "Fundamental I": ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"],
    "Fundamental II": ["6º Ano", "7º Ano", "8º Ano", "9º Ano"]
}

# Extração automática para validação rápida no schema
VALID_SEGMENTS = list(ACADEMIC_TAXONOMY.keys())
VALID_GRADES = [grade for grades in ACADEMIC_TAXONOMY.values() for grade in grades]

# ==========================================
# 2. MAPEAMENTO DE COLUNAS (CSV -> DB)
# ==========================================
COLUMN_MAP = {
    "name": "name",
    "segment": "segment",
    "grade": "grade",
    "full_tuition": "full_tuition",
    "discount_value": "discount_value",
    "scholarship_value": "scholarship_value"
}

# ==========================================
# 3. SCHEMA DE VALIDAÇÃO (PANDERA)
# ==========================================
StudentSchema = pa.DataFrameSchema(
    columns={
        "name": Column(str, Check.str_length(min_value=2), nullable=False),
        
        "segment": Column(
            str, 
            Check.isin(VALID_SEGMENTS), 
            nullable=False,
            description="Deve ser estritamente um dos segmentos oficiais da escola."
        ),
        
        "grade": Column(
            str, 
            Check.isin(VALID_GRADES), 
            nullable=False,
            description="Deve ser uma das séries oficiais mapeadas na taxonomia."
        ),
        
        "full_tuition": Column(float, Check.ge(0.0), nullable=False),
        "discount_value": Column(float, Check.ge(0.0), nullable=False),
        "scholarship_value": Column(float, Check.ge(0.0), nullable=False)
    },
    
    # Validação Multicoluna Avançada (Data Quality)
    # Garante que a 'Série' pertence de fato ao 'Segmento' apontado na MESMA linha.
    checks=[
        pa.Check(
            lambda df: df.apply(
                lambda row: row["grade"] in ACADEMIC_TAXONOMY.get(row["segment"], []),
                axis=1
            ).all(),
            name="check_grade_belongs_to_segment",
            error="Inconsistência Relacional: Há séries atreladas a segmentos incorretos no arquivo."
        )
    ]
)