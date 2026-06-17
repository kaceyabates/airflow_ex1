from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from marketvol_scripts.download_stock import download_stock
from marketvol_scripts.run_query import run_query

default_args = {
    "owner": "kacey",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="marketvol",
    default_args=default_args,
    description="Market volume DAG for AAPL and TSLA",
    schedule_interval="0 18 * * 1-5",  # 6 PM, Mon–Fri
    start_date=datetime(2024, 1, 1, 18, 0),
    catchup=False,
) as dag:
    
    # t0: create temp directory
    t0 = BashOperator(
        task_id="t0_make_temp_dir",
        bash_command="mkdir -p /tmp/data/{{ ds }}",
    )

    # t1: download AAPL data
    t1 = PythonOperator(
        task_id="t1_download_aapl",
        python_callable=download_stock,
        op_kwargs={
            "symbol": "AAPL",
            "output_path": "/tmp/data/{{ ds }}/AAPL.csv",
        },
    )

    # t2: download TSLA data
    t2 = PythonOperator(
        task_id="t2_download_tsla",
        python_callable=download_stock,
        op_kwargs={
            "symbol": "TSLA",
            "output_path": "/tmp/data/{{ ds }}/TSLA.csv",
        },
    )

    # t3: move AAPL file to final directory
    t3 = BashOperator(
        task_id="t3_move_aapl",
        bash_command=(
            "mkdir -p /tmp/data/final/{{ ds }} && "
            "mv /tmp/data/{{ ds }}/AAPL.csv /tmp/data/final/{{ ds }}/AAPL.csv"
        ),
    )

    # t4: move TSLA file to final directory
    t4 = BashOperator(
        task_id="t4_move_tsla",
        bash_command=(
            "mkdir -p /tmp/data/final/{{ ds }} && "
            "mv /tmp/data/{{ ds }}/TSLA.csv /tmp/data/final/{{ ds }}/TSLA.csv"
        ),
    )

    # t5: run query on both final CSVs
    t5 = PythonOperator(
        task_id="t5_run_query",
        python_callable=run_query,
        op_kwargs={
            "input_dir": "/tmp/data/final/{{ ds }}",
        },
    )


    t0 >> [t1, t2]
    t1 >> t3
    t2 >> t4
    [t3, t4] >> t5


