#!/usr/bin/env python3

# Script de Seed de Dados - CESOL Pro
# Popula o banco com 140 alunos fictícios para testes


import os
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from faker import Faker

# Configurar Faker para português do Brasil
fake = Faker('pt_BR')

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:4544@localhost:5432/cesol_pro")
TOTAL_ALUNOS = 140
TAXA_INATIVOS = 0.10  # 10% inativos

# Taxonomia acadêmica
ACADEMIC_TAXONOMY = {
    "Ed. Infantil": ["Maternal", "Jardim I", "Jardim II"],
    "Fundamental I": ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"],
    "Fundamental II": ["6º Ano", "7º Ano", "8º Ano", "9º Ano"]
}

# Motivos de saída para alunos inativos
EXIT_REASONS = [
    "Mudança de cidade",
    "Problemas financeiros",
    "Insatisfação com metodologia",
    "Transferência para escola pública",
    "Mudança de bairro",
    "Conflito de horário",
    "Questões familiares"
]

def criar_engine():
    # Cria engine de conexão com PostgreSQL.
    return create_engine(DATABASE_URL)

def truncar_tabela(engine):
    # Limpa tabela students antes de inserir novos dados.
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE students RESTART IDENTITY CASCADE"))
        conn.commit()
    print("✅ Tabela students truncada")

def gerar_aluno(aluno_id, total_alunos):
    
    Gera dados de um aluno fictício.
    
    Distribuição:
    - Ed. Infantil: 25% (35 alunos)
    - Fundamental I: 50% (70 alunos)  
    - Fundamental II: 25% (35 alunos)
    
    # Definir segmento baseado no ID
    if aluno_id <= 35:
        segment = "Ed. Infantil"
    elif aluno_id <= 105:
        segment = "Fundamental I"
    else:
        segment = "Fundamental II"
    
    # Escolher série aleatória do segmento
    grade = random.choice(ACADEMIC_TAXONOMY[segment])
    
    # Definir status (90% ativos, 10% inativos)
    # Distribuir inativos ao longo dos 140
    is_inativo = aluno_id in random.sample(range(1, 141), 14)
    
    if is_inativo:
        status = "Inativo"
        # Data de saída nos últimos 6 meses
        dias_atras = random.randint(1, 180)
        exit_date = datetime.now() - timedelta(days=dias_atras)
        exit_reason = random.choice(EXIT_REASONS)
    else:
        status = "Ativo"
        exit_date = None
        exit_reason = None
    
    # Dados pessoais
    name = fake.name()
    
    # Dados financeiros realistas
    full_tuition = round(random.uniform(800.00, 1500.00), 2)
    
    # 30% dos alunos têm desconto
    has_discount = random.random() < 0.30
    discount_value = round(random.uniform(50.00, min(300.00, full_tuition * 0.20)), 2) if has_discount else 0.00
    
    # 10% dos alunos têm bolsa
    has_scholarship = random.random() < 0.10
    scholarship_value = round(random.uniform(200.00, min(500.00, full_tuition * 0.30)), 2) if has_scholarship else 0.00
    
    # Data de entrada (alunos antigos de 1-3 anos atrás)
    dias_entrada = random.randint(365, 1095)
    entry_date = datetime.now() - timedelta(days=dias_entrada)
    
    return {
        "name": name,
        "segment": segment,
        "grade": grade,
        "status": status,
        "entry_date": entry_date.date(),
        "exit_date": exit_date.date() if exit_date else None,
        "exit_reason": exit_reason,
        "full_tuition": full_tuition,
        "discount_value": discount_value,
        "scholarship_value": scholarship_value,
        "batch_id": None  # Seed manual, sem batch
    }

def inserir_alunos(engine):
    # Insere 140 alunos no banco de dados.
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print(f"🚀 Iniciando inserção de {TOTAL_ALUNOS} alunos...\n")
        
        for i in range(1, TOTAL_ALUNOS + 1):
            aluno = gerar_aluno(i, TOTAL_ALUNOS)
            
            # Query de inserção
            query = text(
                INSERT INTO students 
                (name, segment, grade, status, entry_date, exit_date, exit_reason, 
                 full_tuition, discount_value, scholarship_value, batch_id)
                VALUES 
                (:name, :segment, :grade, :status, :entry_date, :exit_date, :exit_reason,
                 :full_tuition, :discount_value, :scholarship_value, :batch_id)
            )
            
            session.execute(query, aluno)
            
            # Progresso a cada 10 alunos
            if i % 10 == 0:
                status_icon = "👶" if aluno['segment'] == "Ed. Infantil" else "📚" if aluno['segment'] == "Fundamental I" else "🎓"
                print(f"  {status_icon} Aluno {i:3d}/{TOTAL_ALUNOS}: {aluno['name'][:25]:25} | {aluno['segment'][:15]:15} | {aluno['grade'][:10]:10} | R$ {aluno['full_tuition']:>7.2f} | {aluno['status']}")
        
        session.commit()
        
        # Resumo final
        print(f"\n{'='*60}")
        print("✅ SEED CONCLUÍDO COM SUCESSO!")
        print(f"{'='*60}")
        
        # Contagem por status
        result = session.execute(text("SELECT status, COUNT(*) FROM students GROUP BY status")).fetchall()
        print("\n📊 Resumo:")
        for status, count in result:
            print(f"   {status}: {count} alunos")
        
        # Contagem por segmento
        result = session.execute(text("SELECT segment, COUNT(*) FROM students GROUP BY segment")).fetchall()
        print("\n📚 Por Segmento:")
        for segment, count in result:
            print(f"   {segment}: {count} alunos")
        
        # Receita total mensal esperada
        result = session.execute(text(
            SELECT SUM(full_tuition - discount_value - scholarship_value) as receita
            FROM students WHERE status = 'Ativo'
        )).fetchone()
        print(f"\n💰 Receita mensal estimada (alunos ativos): R$ {result[0]:,.2f}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao inserir alunos: {e}")
        raise
    finally:
        session.close()

def main():
    # Função principal.
    print("="*60)
    print("🎓 CESOL Pro - Seed de Dados")
    print("="*60)
    print(f"Conectando a: {DATABASE_URL.replace('4544', '****')}\n")
    
    engine = criar_engine()
    
    # Verificar conexão
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Conexão com PostgreSQL estabelecida")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return
    
    # Truncar e inserir
    truncar_tabela(engine)
    inserir_alunos(engine)
    
    print("🚀 Pronto! Execute o dashboard:")
    print("   source .venv/bin/activate")
    print("   export PYTHONPATH=\"${PYTHONPATH}:$(pwd)/src\ ")
    print("   streamlit run src/app/main.py")

if __name__ == "__main__":
    main()