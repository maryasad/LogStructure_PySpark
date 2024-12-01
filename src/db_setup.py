from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, MetaData, Table
from datetime import datetime
import os

# Create source and target database files in a 'data' directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

SOURCE_DB_PATH = os.path.join(DATA_DIR, 'source.db')
TARGET_DB_PATH = os.path.join(DATA_DIR, 'target.db')

# Create database URLs
SOURCE_DB_URL = f'sqlite:///{SOURCE_DB_PATH}'
TARGET_DB_URL = f'sqlite:///{TARGET_DB_PATH}'

def create_source_database():
    """Create source database with sample ETL log data"""
    engine = create_engine(SOURCE_DB_URL)
    metadata = MetaData()

    # Create ETL logs table
    etl_logs = Table(
        'etl_logs', 
        metadata,
        Column('id', Integer, primary_key=True),
        Column('execution_time', DateTime),
        Column('process_name', String(100)),
        Column('log_text', Text),
        Column('status', String(20))
    )

    metadata.create_all(engine)

    # Insert sample data
    sample_logs = [
        {
            'execution_time': datetime(2023, 1, 1, 10, 30),
            'process_name': 'DailyPatientETL',
            'log_text': '''
            EXEC sp_ProcessPatientData
            BEGIN TRANSACTION
            SELECT * FROM Patients.dbo.RawData
            WHERE UpdateDate >= '2023-01-01'
            INSERT INTO Patients.dbo.Processed (PatientId, Name, DOB)
            VALUES (...)
            COMMIT TRANSACTION
            ''',
            'status': 'SUCCESS'
        },
        {
            'execution_time': datetime(2023, 1, 1, 11, 45),
            'process_name': 'DiagnosisETL',
            'log_text': '''
            EXEC sp_ProcessDiagnosis
            BEGIN TRANSACTION
            UPDATE Diagnosis.dbo.Current
            FROM Diagnosis.dbo.Staging
            WHERE Current.DiagnosisId = Staging.DiagnosisId
            COMMIT TRANSACTION
            ''',
            'status': 'SUCCESS'
        }
    ]

    with engine.connect() as conn:
        for log in sample_logs:
            conn.execute(etl_logs.insert(), log)
        conn.commit()

def create_target_database():
    """Create target database for mapping data"""
    engine = create_engine(TARGET_DB_URL)
    metadata = MetaData()

    # Create mapping table
    log_mapping = Table(
        'log_mapping', 
        metadata,
        Column('id', Integer, primary_key=True),
        Column('source_log_id', Integer),
        Column('stored_procedure', String(100)),
        Column('affected_table', String(100)),
        Column('execution_time', DateTime),
        Column('process_name', String(100)),
        Column('status', String(20))
    )

    metadata.create_all(engine)

if __name__ == "__main__":
    print("Creating source database...")
    create_source_database()
    print(f"Source database created at: {SOURCE_DB_PATH}")

    print("\nCreating target database...")
    create_target_database()
    print(f"Target database created at: {TARGET_DB_PATH}")
