import json
import os

def onboard_company():
    #read user input
    print("# Company Name #")
    company_name = input("Enter the company's name: ")
    print("# Company API Details #")
    api_url = input("Enter the API URL (example: http://localhost:5000/loyalty): ")
    api_params_GET = input("Enter the GET-API accepted parameters, separated by commas (example: /get?id,/get?phone-number,/get?email-address): ")
    api_params_POST = input("Enter the POST-API accepted parameters, separated by commas (example: /post/add,/post/deduct): ")
    print("# API KEY/VALUE Details #")
    api_key = input("Enter the API-KEY that should be used in the header (example: api-key): ") #idk how to ask clearly for that :))
    api_value = input("Enter the API-VALUE for Monet to use (example: MONET-1): ")
    print("#####################################################################")
    print(f"# This is how it would look in the headers: {api_key}={api_value} #########")
    print("#####################################################################")

    #organize the points in a json file
    company_details = {
        "company_name": company_name,
        "api_url": api_url,
        "api_params_GET": api_params_GET,
        "api_params_POST": api_params_POST,
        "api_key": api_key,
        "api_value": api_value
    }

    #save the file
    folder_path = 'on-boarded_companies'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, f'{company_name}_api_details.json')

    with open(file_path, 'w') as json_file:
        json.dump(company_details, json_file, indent=4)

    print(f"Company '{company_name}' has been onboarded successfully.")
    print(f"Details saved at: {file_path}")

onboard_company()