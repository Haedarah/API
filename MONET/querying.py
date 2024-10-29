import json
import requests
import os

#read the API details of an on-boarded company
def load_company_details(company_name):
    file_path = f'on-boarded_companies/{company_name}_api_details.json'
    if not os.path.exists(file_path):
        print(f"Company '{company_name}' not found in the on-boarded companies.")
        return None
    
    with open(file_path, 'r') as file:
        company_details = json.load(file)
    return company_details

#query an API - GET
def query_get_api(company_details, param, value):
    #fetch the needed details
    api_url = company_details["api_url"]
    api_key = company_details["api_key"]
    api_value = company_details["api_value"]

    #prepare the url of the query    
    full_url = f"{api_url}{param}={value}"
    
    #prepare the headers of the query
    headers = {
        api_key: api_value
    }
    
    #send the GET request
    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return(response.status_code, response.text)

#query an API - POST : for adding points
def query_post_add_api(company_details, param, user_id, points, valid_until):
    #fetch the needed details
    api_url = company_details["api_url"]
    api_key = company_details["api_key"]
    api_value = company_details["api_value"]
    
    #prepare the url of the query
    full_url = f"{api_url}{param}"

    #prepare the headers of the query
    headers = {
        api_key: api_value
    }

    #prepare the parameters to be passed with the query
    data = {
        "user-id": str(user_id),
        "points": str(points),
        "valid-until": str(valid_until)
    }

    #send the POST request
    response = requests.post(full_url, headers=headers, json=data)
        
    if response.status_code == 200:
        return response.json()
    else:
        return(response.status_code, response.text)

#query an API - POST : for deducting points
def query_post_deduct_api(company_details, param, user_id, points):
    #fetch the needed details
    api_url = company_details["api_url"]
    api_key = company_details["api_key"]
    api_value = company_details["api_value"]
    
    #prepare the url of the query
    full_url = f"{api_url}{param}"

    #prepare the headers of the query
    headers = {
        api_key: api_value
    }

    #prepare the parameters to be passed with the query
    data = {
        "user-id": str(user_id),
        "points": str(points),
    }

    #send the POST request
    response = requests.post(full_url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return(response.status_code, response.text)


def main():
    #CLI
    print("# Welcome to the API Interaction Script #")
    
    company_name = input("Enter the company's name you want to interact with: ")
    company_details = load_company_details(company_name)
    
    #validate the there is an on-boarded company with the same name
    if not company_details:
        return
    
    print(f"Successfully loaded API details for {company_name}.")
    
    api_params_GET = company_details["api_params_GET"].split(',')
    api_params_POST = company_details["api_params_POST"].split(',')

    while True:
        get_or_post = input("For a GET request, enter 'G'. For a POST request, enter 'P'. To exit, enter 'E': ")
        
        if get_or_post == 'E':
            print("Exiting the script.")
            break
        
        elif get_or_post == 'G':
            print(f"Available parameters for a GET query: {api_params_GET}")
            param = input("Enter the parameter you want to query: ").strip()
        
            if param not in api_params_GET:
                print(f"Invalid parameter. Please choose from {api_params_GET}.")
                continue

            value = input(f"Enter the value for {param}: ").strip()
        
            result = query_get_api(company_details, param, value)
        
            if result:
                print("API Response:")
                print(json.dumps(result, indent=4))
        
        elif get_or_post == 'P':
            print(f"Available parameters for a POST query: {api_params_POST}")
            param = input("Enter the parameter you want to query: ").strip()
            
            if param not in api_params_POST:
                print(f"Invalid parameter. Please choose from {api_params_POST}.")
                continue
            
            if param == "/post/add" :
                user_id = input("Enter the user ID: ").strip()
                points = input("Enter the points: ").strip()
                valid_until = input("Enter the valid until date: ").strip()
                
                result = query_post_add_api(company_details, param, user_id, points, valid_until)
                
                if result:
                    print("API Response:")
                    print(json.dumps(result, indent=4))

            elif param == "/post/deduct" :
                user_id = input("Enter the user ID: ").strip()
                points = input("Enter the points to be deducted: ").strip()

                result = query_post_deduct_api(company_details, param, user_id, points)
                
                if result:
                    print("API Response:")
                    print(json.dumps(result, indent=4))
        
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
