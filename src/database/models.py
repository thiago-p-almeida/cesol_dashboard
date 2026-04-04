from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    # Dados Demográficos
    birth_date = Column(Date, nullable=True) # Suporta o cálculo do KPI de Distorção Idade-Série (TB-028)
    
    # Taxonomia Acadêmica (TB-005)
    segment = Column(String)  # Infantil, Fundamental I, etc.
    grade = Column(String)    # 1º Ano, 2º Ano...
    classroom = Column(String) # Turma A, B...
    
    # Status e Retenção (TB-002, TB-006)
    status = Column(String, default="Ativo") 
    entry_date = Column(Date, default=datetime.utcnow)
    exit_date = Column(Date, nullable=True)
    exit_reason = Column(String, nullable=True)
    
    # Financeiro Base (TB-014)
    full_tuition = Column(Float) # Mensalidade cheia
    discount_value = Column(Float, default=0.0)
    scholarship_value = Column(Float, default=0.0)

    # Auditoria e Linhagem (TB-015)
    # FK para rastrear de qual importação este aluno veio
    batch_id = Column(Integer, ForeignKey('import_batches.id'), nullable=True)

class FinancialTransaction(Base):
    __tablename__ = 'financial_transactions'
    
    id = Column(Integer, primary_key=True)
    type = Column(String) # 'Revenue' ou 'Expense'
    category = Column(String) # Aluguel, Folha, Mensalidade (TB-017)
    description = Column(String)
    amount = Column(Float, nullable=False)
    reference_date = Column(Date, nullable=False)
    status = Column(String) # 'Expected' ou 'Received'
    
class ImportBatch(Base):
    __tablename__ = 'import_batches'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    import_date = Column(DateTime, default=datetime.utcnow)
    row_count = Column(Integer) # Métrica de volume processado
    status = Column(String) # 'Success', 'Failed'
    logs = Column(String) # Registro de erros (TB-015, TB-044)

    # Relacionamento Pro: Permite acessar alunos via batch.students
    students = relationship("Student", backref="batch")