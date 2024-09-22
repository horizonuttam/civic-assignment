Data Cleaning Pipeline Framework
Overview
This repository contains a configurable data cleaning pipeline framework designed to streamline the processing of public datasets for faster and more consistent data quality. The framework allows users to configure and trigger data pipelines via API calls. The key feature of this pipeline is the flexibility to specify the order of tasks and add new tasks easily. It ensures reusability and better data quality by offering a library of atomic data cleaning tasks.

Features
Configurable Pipeline: Configure tasks like missing value assessment and duplicate row identification.
API Triggering: Users can trigger the pipeline and specify tasks via an API call.
Task Library: Add, update, or remove tasks dynamically within the framework.
Log Generation: Each task logs its output for reporting and verification.
Atomic Tasks Implemented
Identify Missing Values: Detect missing values in specified columns and compare them against configurable thresholds.
Identify Duplicate Rows: Detect duplicate rows, either as whole rows or based on specific column combinations.
Getting Started
Prerequisites
Python 3.7+
Flask
pandas
Installation
Clone this repository:

bash
Copy code
git clone https://github.com/your-username/data-cleaning-pipeline.git
cd data-cleaning-pipeline
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Flask server:

bash
Copy code
python app.py
The API will now be available at http://localhost:8000.

API Usage
Endpoint: /run_pipeline
This is the main endpoint used to configure and trigger the data cleaning pipeline.

Method: POST
URL: http://localhost:8000/run_pipeline
Request Format
json
Copy code
{
  "tasks": [
    {
      "task_name": "identify_missing_values",
      "config": {
        "column1": 10, 
        "column2": 5
      }
    },
    {
      "task_name": "identify_duplicate_rows",
      "config": {
        "columns": ["ID"]
      }
    }
  ]
}
Request Parameters:
tasks: A list of tasks to execute, each task should have:
task_name: The name of the task (e.g., identify_missing_values, identify_duplicate_rows).
config: Configuration parameters required for the task. Each task has its own configurable parameters:
For identify_missing_values, provide a dictionary of columns and the accepted missing value threshold.
For identify_duplicate_rows, provide the list of columns to check for duplicates.
Response
The response will contain the results of the executed tasks in the specified order:

json
Copy code
{
  "identify_missing_values": {
    "column1": {
      "missing_percentage": 5.0,
      "status": "Acceptable"
    },
    "column2": {
      "missing_percentage": 12.0,
      "status": "Unacceptable"
    }
  },
  "identify_duplicate_rows": {
    "duplicates_found": 3,
    "status": "Unacceptable"
  }
}
Example API Request
To trigger the pipeline, send a POST request to http://localhost:8000/run_pipeline with the following JSON payload:

json
Copy code
{
  "tasks": [
    {
      "task_name": "identify_missing_values",
      "config": {
        "ID": 0,
        "Age": 5
      }
    },
    {
      "task_name": "identify_duplicate_rows",
      "config": {
        "columns": ["ID"]
      }
    }
  ]
}
You can use tools like Postman, Insomnia, or any other HTTP client to send the POST request with the payload to trigger the pipeline.

Extending the Framework
Adding New Tasks
To add a new task:

Create a new Python class in the pipeline/tasks.py file.
Implement the task's logic and ensure it conforms to the required structure.
Update the pipeline configuration to recognize the new task.
Updating Existing Tasks
To update an existing task:

Modify the task's logic in the pipeline/tasks.py file.
Ensure the configuration and API documentation reflect the updates.
Project Structure
bash
Copy code
.
├── pipeline/
│   ├── __init__.py
│   ├── tasks.py       # Task implementations (e.g., Missing values, Duplicate rows)
│   └── pipeline.py    # Main pipeline logic
├── app.py             # Flask API for running the pipeline
├── trigger_pipeline.py # Script for triggering the pipeline via API
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
Logging
Each task logs its output, and the pipeline generates a comprehensive log file pipeline.log to track the results and errors.
