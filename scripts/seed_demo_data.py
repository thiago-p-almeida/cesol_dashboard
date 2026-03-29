
# Seed de dados fictícios para o CESOL Pro.

# Executa inserções diretas no PostgreSQL usando os modelos SQLAlchemy
# para popular as tabelas de alunos (students) e lotar alguns registros
# de churn.

# Uso (na raiz do projeto):

#    python scripts/seed_demo_data.py


import os
import sys
from datetime import datetime, date

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.models import Base, Student  # noqa: E402


def get_session():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("Defina DATABASE_URL no arquivo .env antes de rodar o seed.")
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def seed_students(session):
    # Insere um conjunto pequeno porém variado de alunos.
    if session.query(Student).count() > 0:
        print("Já existem alunos na tabela 'students'. Seed não será reaplicado.")
        return

    alunos = [
        # Ed. Infantil
        dict(
            name="Ana Souza",
            segment="Ed. Infantil",
            grade="Maternal",
            classroom="A",
            status="Ativo",
            entry_date=date(2023, 1, 10),
            full_tuition=1500.0,
            discount_value=150.0,
            scholarship_value=0.0,
        ),
        dict(
            name="Bruno Lima",
            segment="Ed. Infantil",
            grade="Jardim I",
            classroom="B",
            status="Ativo",
            entry_date=date(2023, 2, 15),
            full_tuition=1550.0,
            discount_value=50.0,
            scholarship_value=100.0,
        ),
        # Fundamental I
        dict(
            name="Carla Menezes",
            segment="Fundamental I",
            grade="3º Ano",
            classroom="A",
            status="Ativo",
            entry_date=date(2022, 2, 1),
            full_tuition=1800.0,
            discount_value=180.0,
            scholarship_value=0.0,
        ),
        dict(
            name="Diego Ferreira",
            segment="Fundamental I",
            grade="5º Ano",
            classroom="B",
            status="Inativo",
            entry_date=date(2021, 2, 1),
            exit_date=date(2024, 12, 1),
            exit_reason="Mudança de cidade",
            full_tuition=1900.0,
            discount_value=0.0,
            scholarship_value=0.0,
        ),
        # Fundamental II
        dict(
            name="Eduarda Campos",
            segment="Fundamental II",
            grade="7º Ano",
            classroom="A",
            status="Ativo",
            entry_date=date(2021, 2, 1),
            full_tuition=2100.0,
            discount_value=210.0,
            scholarship_value=0.0,
        ),
        dict(
            name="Felipe Costa",
            segment="Fundamental II",
            grade="9º Ano",
            classroom="B",
            status="Inativo",
            entry_date=date(2020, 2, 1),
            exit_date=date(2024, 11, 15),
            exit_reason="Inadimplência",
            full_tuition=2200.0,
            discount_value=0.0,
            scholarship_value=200.0,
        ),
    ]

    for a in alunos:
        session.add(Student(**a))

    session.commit()
    print(f"Inseridos {len(alunos)} alunos fictícios em 'students'.")


def main():
    session = get_session()
    print(f"Seed iniciado em {datetime.now().isoformat(timespec='seconds')}")
    seed_students(session)
    print("Seed concluído.")


if __name__ == "__main__":
    main()

