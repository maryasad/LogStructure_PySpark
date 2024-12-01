from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, from_json, struct
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType
import pandas as pd
from sqlalchemy import create_engine
import re
from config import *

def create_spark_session():
    """Create and configure Spark session"""
    spark = SparkSession.builder
    for key, value in SPARK_CONFIG.items():
        spark = spark.config(key, value)
    
    return spark.getOrCreate()

def extract_log_info(log_text):
    """
    Extract important information from log text
    Customize this function based on your log format
    """
    try:
        # Example pattern matching for SQL Server stored procedures and tables
        stored_proc_pattern = r"EXEC\s+(\w+)"
        table_pattern = r"(?:FROM|INTO|UPDATE)\s+([a-zA-Z0-9_]+\.?[a-zA-Z0-9_]+\.?[a-zA-Z0-9_]+)"
        
        stored_procs = re.findall(stored_proc_pattern, log_text)
        affected_tables = re.findall(table_pattern, log_text)
        
        return {
            'stored_procedure': stored_procs[0] if stored_procs else None,
            'affected_table': affected_tables[0] if affected_tables else None,
            'log_text': log_text
        }
    except Exception as e:
        return {
            'stored_procedure': None,
            'affected_table': None,
            'log_text': log_text,
            'error': str(e)
        }

def process_logs():
    """Main function to process logs using Spark"""
    # Create Spark session
    spark = create_spark_session()
    
    try:
        # Read from source database
        source_df = spark.read \
            .format("jdbc") \
            .option("url", SOURCE_DB_CONNECTION) \
            .option("dbtable", SOURCE_TABLE_NAME) \
            .load()
        
        # Register UDF for log processing
        extract_log_udf = udf(extract_log_info, 
                            StructType([
                                StructField("stored_procedure", StringType(), True),
                                StructField("affected_table", StringType(), True),
                                StructField("log_text", StringType(), True),
                                StructField("error", StringType(), True)
                            ]))
        
        # Process logs
        processed_df = source_df.withColumn(
            "extracted_info",
            extract_log_udf(col(LOG_COLUMN_NAME))
        )
        
        # Flatten the extracted information
        final_df = processed_df.select(
            col("id").alias("source_log_id"),
            col("extracted_info.stored_procedure"),
            col("extracted_info.affected_table"),
            col("execution_time"),
            col("process_name"),
            col("status")
        )
        
        # Convert to pandas for easier database insertion
        pandas_df = final_df.toPandas()
        
        # Create target database connection
        target_engine = create_engine(TARGET_DB_CONNECTION)
        
        # Write to mapping table
        pandas_df.to_sql(
            'log_mapping',
            target_engine,
            if_exists='append',
            index=False,
            chunksize=BATCH_SIZE
        )
        
        print(f"Successfully processed {len(pandas_df)} log entries")
        
    except Exception as e:
        print(f"Error processing logs: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    process_logs()
