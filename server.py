import json
from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Define the endpoint for POST requests
@app.route('/api/receive', methods=['POST'])
def receive_data():
    """
    Handles incoming POST requests, extracts the data (JSON or raw),
    and prints it to the console where the server is running.
    """
    print("--- Received POST Request ---")
    
    # 1. Try to get JSON data
    try:
        data = request.json
        if data is not None:
            print("Received JSON Data:")
            # Pretty print the JSON data for readability
            print(json.dumps(data, indent=4))
        else:
            # If Content-Type is application/json but body is empty
            print("Received JSON Content-Type but body was empty.")
            
    except Exception as e:
        # 2. If it's not JSON, print the raw data (e.g., plain text, form data)
        data = request.data.decode('utf-8')
        if data:
            print(f"Received Raw Data (Non-JSON): {data}")
        else:
            print("Received request with no body content.")
            
    print("-------------------------------")
    
    # Return a success message
    return jsonify({
        "status": "success", 
        "message": "Data received and printed to server console."
    }), 200

# Run the application
if __name__ == '__main__':
    # To run:
    # 1. Save this file as app.py
    # 2. In your terminal, run: python app.py
    # 3. The server will start on http://127.0.0.1:5000/
    
    # To test the POST request using curl (run this in a *separate* terminal):
    # curl -X POST -H "Content-Type: application/json" -d '{"key": "value", "user_id": 123}' http://127.0.0.1:5000/api/receive
    app.run(debug=True)