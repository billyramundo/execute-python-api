from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import os
import subprocess
import tempfile
import json

#python 3.9.7
app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_script2():
    data = request.get_json()

    # Input validation
    if 'script' not in data:
        return jsonify({'error': 'No script provided'}), 400
    
    # Make common libraries accessible without need to import in the script (can update with others as needed)
    script = f"""
import numpy as np
import pandas as pd
import os

{data['script']}
"""

    # Validate there's a main method
    if 'def main()' not in script:
        return jsonify({'error': 'The script must contain a main function'}), 400
    
    try:
        script_path = None
        return_file_path = None
        
        # Create temp file to hold output of the script from the request
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json', dir='/tmp') as return_file:
                return_file_path = return_file.name
        
        
        # Create a temporary file to store the script
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', dir='/tmp') as temp_script:
            # Modify the script to write the return value to the temporary file
            script += f"""
import json

try:
    result = main()
    with open('{return_file_path}', 'w') as f:
        json.dump(result, f)
except Exception as e:
    with open('{return_file_path}', 'w') as f:
        json.dump({{"error": str(e)}}, f)
"""
            # Write the finalized script to a temp file
            temp_script.write(script.encode('utf-8'))
            script_path = temp_script.name

        # Run the script using nsjail
        result = subprocess.run(
            ['/usr/local/bin/nsjail', '--verbose', '--config', '/app/nsjail.cfg', '--', '/usr/local/bin/python3', script_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Check if the process completed successfully
        if result.returncode != 0:
            return jsonify({'error': 'Script execution failed', 'details': result.stderr}), 500
        
        # Read the return value from the temporary file
        with open(return_file_path, 'r') as f:
            return_value = json.load(f)
            
        # Validate that the result is a JSON object
        if not isinstance(return_value, dict):
            return jsonify({'error': 'main() must return a JSON object (dict)'}), 400
        
        return jsonify(return_value)

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during script execution', 'details': str(e)}), 500
    finally:
        # Clean up the temp files
        if(script_path):
            os.remove(script_path)
        if(return_file_path):
            os.remove(return_file_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



#Command to send json file called payload.json containing python script as body of request:
#  curl -X POST http://127.0.0.1:8080/execute -H "Content-Type: application/json" --data @payload.json