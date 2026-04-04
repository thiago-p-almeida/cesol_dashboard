#!/usr/bin/env python3
import os
import sys
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from faker import Faker

# Ajuste de PATH para encontrar os modelos dentro de src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
from src.database.models import Base, Student

# Configurações
fake = Faker('pt_BR')
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:4544@localhost:5432/cesol_pro")
TOTAL_ALUNOS = 140

ACADEMIC_TAXONOMY = {
    "Ed. Infantil": ["Maternal", "Jardim I", "Jardim II"],
    "Fundamental I": ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"],
    "Fundamental II": ["6º Ano", "7º Ano", "8º Ano", "9º Ano"]
}

AGE_BY_GRADE = {
    "Maternal": 3, "Jardim I": 4, "Jardim II": 5,
    "1º Ano": 6, "2º Ano": 7, "3º Ano": 8, "4º Ano": 9, "5º Ano": 10,
    "6º Ano": 11, "7º Ano": 12, "8º Ano": 13, "9º Ano": 14
}

EXIT_REASONS = ["Mudança de cidade", "Problemas financeiros", "Insatisfação com metodologia", "Questões familiares"]

def gerar_aluno(aluno_id):
    """Gera dados de um aluno fictício com lógica de BI integrada."""
    if aluno_id <= 35: 
        segment = "Ed. Infantil"
    elif aluno_id <= 105: 
        segment = "Fundamental I"
    else: 
        segment = "Fundamental II"
    
    grade = random.choice(ACADEMIC_TAXONOMY[segment])
    is_inativo = random.random() < 0.10
    
    status = "Inativo" if is_inativo else "Ativo"
    exit_date = (datetime.now() - timedelta(days=random.randint(1, 180))).date() if is_inativo else None
    exit_reason = random.choice(EXIT_REASONS) if is_inativo else None
    
    # Lógica de Idade com 15% de distorção (atraso pedagógico)
    idade_base = AGE_BY_GRADE[grade]
    if random.random() < 0.15:
        idade_base += random.randint(2, 3)
    
    birth_date = datetime(2026 - idade_base, random.randint(1, 12), random.randint(1, 28)).date()
    full_tuition = round(random.uniform(800.00, 1500.00), 2)
    entry_date = (datetime.now() - timedelta(days=random.randint(365, 1095))).date()
    
    return {
        "name": fake.name(),
        "birth_date": birth_date,
        "segment": segment,
        "grade": grade,
        "classroom": "Única",  # CORREÇÃO FASE 3.1: Define turma única para habilitar cálculo de densidade
        "status": status,
        "entry_date": entry_date,
        "exit_date": exit_date,
        "exit_reason": exit_reason,
        "full_tuition": full_tuition,
        "discount_value": round(random.uniform(50, 200), 2) if random.random() < 0.3 else 0.0,
        "scholarship_value": round(random.uniform(200, 500), 2) if random.random() < 0.1 else 0.0,
        "batch_id": None
    }

def main():
    print("="*60)
    print("🎓 CESOL Pro - Seed de Dados (v2.6 - Saneamento de Turmas)")
    print("="*60)
    
    engine = create_engine(DATABASE_URL)
    
    # PASSO 1: Garante a estrutura correta do banco (incluindo birth_date e classroom)
    print("🛠️ Verificando estrutura do banco de dados...")
    Base.metadata.create_all(engine)
    
    # PASSO 2: Limpar dados existentes para evitar duplicidade
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE students RESTART IDENTITY CASCADE"))
        conn.commit()
        print("✅ Tabela students limpa e pronta.")

    # PASSO 3: Inserir novos dados com a nova taxonomia de turmas
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print(f"🚀 Gerando e inserindo {TOTAL_ALUNOS} alunos...")
        for i in range(1, TOTAL_ALUNOS + 1):
            dados = gerar_aluno(i)
            session.add(Student(**dados))
        
        session.commit()
        print(f"\n{'='*60}\n✅ SEED CONCLUÍDO COM SUCESSO!\n{'='*60}")
    except Exception as e:
        session.rollback()
        print(f"❌ Erro durante a inserção: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()