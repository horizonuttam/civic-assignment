from flask import Flask, request, jsonify
import pandas as pd
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    filename="pipeline.log", 
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    try:
        req_data = request.get_json()
        if not req_data or 'tasks' not in req_data:
            raise ValueError("Invalid input: JSON payload must include 'tasks'.")

        tasks_to_run = req_data['tasks']
        
        # Log received tasks
        logging.info(f"Received tasks: {tasks_to_run}")
        
        # Simulating data processing
        # (Replace this part with your actual data processing logic)
        results = {"message": "Pipeline run successfully", "tasks": tasks_to_run}
        
        return jsonify(results), 200

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 400  # Changed to 400 for client error

if __name__ == "__main__":
    try:
        print("Starting Flask app...")
        app.run(debug=True, host='0.0.0.0', port=8000)
    except Exception as e:
        logging.error(f"Failed to start the Flask app: {e}")
