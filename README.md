# Airflow Mini-Project (Project 1): marketvol

## Project Description

This project implements an Apache Airflow pipeline named marketvol.
The DAG downloads 1-minute interval stock data for AAPL and TSLA using yfinance, stores raw files in /tmp/data/<ds>/, moves them to /tmp/data/final/<ds>/, and runs a Python task that loads both CSVs and prints row counts.

Schedule: Monday-Friday at 6 PM.

Operators used:
- BashOperator
- PythonOperator

Tasks:
- t0: create directory
- t1: download AAPL
- t2: download TSLA
- t3: move AAPL
- t4: move TSLA
- t5: run query on both CSVs

Task dependencies:
- t0 -> [t1, t2]
- t1 -> t3
- t2 -> t4
- [t3, t4] -> t5

## Repository Structure

```text
marketvol_dag.py
marketvol_scripts/
	download_stock.py
	run_query.py
README.md
dag_run_output.txt
```

dag_run_output.txt contains the successful Airflow run log.

## Setup and Run

### 1. Install Apache Airflow

```bash
pip install apache-airflow
```

### 2. Initialize Airflow metadata database

```bash
airflow db init
```

### 3. Place DAG and scripts

Copy the DAG and helper scripts into the Airflow DAGs directory:

- Place marketvol_dag.py in ~/airflow/dags/
- Place marketvol_scripts/ in ~/airflow/dags/

Expected result:
- ~/airflow/dags/marketvol_dag.py
- ~/airflow/dags/marketvol_scripts/download_stock.py
- ~/airflow/dags/marketvol_scripts/run_query.py

### 4. Start Airflow services

Start the webserver:

```bash
airflow webserver --port 8080
```

Start the scheduler (in a separate terminal):

```bash
airflow scheduler
```

## Trigger the DAG in Airflow UI

1. Open http://localhost:8080.
2. Find the marketvol DAG.
3. Turn it on if paused.
4. Click Trigger DAG.

## Verify Output

After a successful run, confirm these outputs:

- Raw CSVs created in /tmp/data/<ds>/
- Final CSVs moved to /tmp/data/final/<ds>/
- The final task prints row counts for both files


