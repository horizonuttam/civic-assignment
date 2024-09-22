import os
from flask import Flask, request, jsonify
import pandas as pd
import logging

def create_project_structure(base_dir):
    directories = [
        "pipeline",
        "pipeline/__init__.py",
        "pipeline/tasks.py",
        "pipeline/pipeline.py",
        "app.py",
        "requirements.txt",
        "trigger_pipeline.py"
    ]

    for directory in directories:
        if not directory.endswith('.py'):
            os.makedirs(os.path.join(base_dir, directory), exist_ok=True)
        else:
            file_path = os.path.join(base_dir, directory)
            with open(file_path, 'w') as f:
                pass

logging.basicConfig(level=logging.INFO, filename="pipeline.log", 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

def load_excel_file(file_path):
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        logging.error(f"Error loading Excel file: {e}")
        raise

class IdentifyMissingValues:
    def __init__(self, config):
        self.config = config

    def run(self, data):
        results = {}
        for column, threshold in self.config.items():
            if column in data.columns:
                missing_percentage = data[column].isna().mean() * 100
                results[column] = {
                    "missing_percentage": missing_percentage,
                    "status": "Acceptable" if missing_percentage <= threshold else "Unacceptable"
                }
                logging.info(f"Missing values check for column {column}: {results[column]}")
            else:
                results[column] = {"error": f"Column '{column}' not found in dataset."}
                logging.error(f"Column '{column}' not found in dataset.")
        return results

class Pipeline:
    def __init__(self, tasks):
        self.tasks = tasks

    def run(self, data):
        report = {}
        for task_name, task in self.tasks:
            result = task.run(data)
            report[task_name] = result
        return report

@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    try:
        req_data = request.get_json()
        tasks_to_run = req_data['tasks']
        data = load_excel_file("Assignment Task _ Dataset.xlsx")

        task_instances = []
        for task_info in tasks_to_run:
            task_name = task_info['task_name']
            task_config = task_info['config']
            if task_name == "identify_missing_values":
                task_instances.append((task_name, IdentifyMissingValues(task_config)))

        pipeline = Pipeline(task_instances)
        result = pipeline.run(data)

        return jsonify(result)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    base_directory = "Assignment project1"
    create_project_structure(base_directory)
    print(f"Project structure created at: {base_directory}")
