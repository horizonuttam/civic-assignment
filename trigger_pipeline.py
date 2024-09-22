from flask import Flask, request, jsonify
import json

def trigger_pipeline(api_url, tasks):
    try:
        # Prepare the payload and headers
        payload = {"tasks": tasks}
        headers = {"Content-Type": "application/json"}

        # Make the POST request to the Flask API
        response = request.post(api_url, headers=headers, data=json.dumps(payload))

        # Check for success (HTTP 200)
        if response.status_code == 200:
            print("Pipeline triggered successfully!")
            try:
                # Try to parse the response as JSON
                response_data = response.json()
                print("Response:", json.dumps(response_data, indent=4))
            except json.JSONDecodeError:
                # If response is not in JSON format
                print("Response was not in JSON format:", response.text)
        else:
            # Handle failed status codes
            print(f"Failed to trigger pipeline. Status code: {response.status_code}")
            print("Response:", response.text)

    except request.exceptions.RequestException as e:
        # Catch any request-related errors
        print(f"An error occurred with the request: {e}")
    except Exception as e:
        # Catch any other exceptions
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # The API endpoint for the Flask app
    api_url = "http://localhost:8000/run_pipeline"
    
    # Define the tasks to run
    tasks = [{"task_name": "identify_missing_values", "config": {"column1": 20}}]
    
    # Trigger the pipeline by making the API request
    trigger_pipeline(api_url, tasks)
