import json

def json_updater(file,field, updated_data):
    json_file = open(file, "r") # Open the JSON file for reading
    data = json.load(json_file) # Read the JSON into the buffer
    json_file.close() # Close the JSON file

    ## Working with buffered content
    tmp = data[field] 
    data[field] = updated_data

    ## Save our changes to JSON file
    print("Updating %s field..."%(field))
    print("New Data: %s\n\n"%(updated_data))

    json_file = open(file, "w+")
    json_file.write(json.dumps(data, indent=4))
    json_file.close()