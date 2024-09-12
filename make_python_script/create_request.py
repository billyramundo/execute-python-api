import json

# Read the content of the script
with open("script.py", "r") as script_file:
    script_content = script_file.read()

# Prepare the payload
payload = {"script": script_content}

# Write to payload.json
with open("payload.json", "w") as json_file:
    json.dump(payload, json_file)
