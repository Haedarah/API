from flask import Flask, jsonify, request, abort
import pandas as pd

app = Flask(__name__)

path_to_database = 'database/users-points.xlsx'  #The database of the company
API_VALUE = "MONET-1"  #The hardcoded MONET API value

df = pd.read_excel(path_to_database,dtype=str)

#API key validation function
def require_api_value():
    api_value = request.headers.get('api-key') #retrieve the API key from the request
    #validate the API value
    if api_value != API_VALUE:
        abort(401, description="Unauthorized: Invalid or missing API key")

#Parse points column to a list of dictionaries. Input: string (a cell in the points column) | Output: list of dictionaries representing points items
def parse_points(points_column):
    points_list = []
    points_entries = points_column.split('},{')
    for entry in points_entries:
        clean_entry = entry.replace('{', '').replace('}', '').split(',')
        #populate the points_list with points items
        points_list.append({
            'points': int(clean_entry[0]),
            'expiry-date': clean_entry[1]
        })
    return points_list

#Get the grand total of a user's points
def get_user_total_points(user_id):
    points_list = parse_points(df[df['user-id'] == user_id]['points[#,date-of-expiry]'][int(user_id)-1])#parse the points
    total_points = sum(point['points'] for point in points_list)#calculate the total points
    return total_points

#A reverse of "parse_points" function:
#Convert back a list of dictionaries to the points column string format. Input: list of dictionaries | Output: string
def format_points(points_list):
    return ','.join([f"{{{item['points']},{item['expiry-date']}}}" for item in points_list])

#Adds an entry to the points cell
def append_points(user_id, amount_of_points, validity_of_points):
    points_list = parse_points(df[df['user-id'] == user_id]['points[#,date-of-expiry]'][int(user_id)-1]) #parse the points
    points_list.append({'points': amount_of_points, 'expiry-date': validity_of_points}) #append the new points item
    cell = format_points(points_list) #format back into a string
    df.loc[df['user-id'] == user_id, 'points[#,date-of-expiry]'] = cell #update the dataframe
    df.to_excel('database/users-points.xlsx', index=False) #update the database

#Deducts an amount of points from a user via passing their id
def deduct_points(user_id, points):
    points_list = parse_points(df[df['user-id'] == user_id]['points[#,date-of-expiry]'][int(user_id)-1]) #parse the points
    items_to_be_deleted=0 #keep track of the items that you want to delete
    
    #iterate over the points, marking the elements that need to be deleted, and adjusting the item that needs to be adjusted
    for item in points_list:
        if points>=item['points']:
            points -= item['points']
            items_to_be_deleted += 1
        else:
            item['points'] -= points
            break
    
    points_list=points_list[items_to_be_deleted:] #take the healthy slice of the points_list
    cell = format_points(points_list) #reverse-parse the points
    df.loc[df['user-id'] == user_id, 'points[#,date-of-expiry]'] = cell #update the dataframe
    df.to_excel('database/users-points.xlsx', index=False) #update the database


######################################################
######################## APIS ########################
######################################################
#########
## GET ##
#########
@app.route('/loyalty/get', methods=['GET']) #setting the GET API path
def get_user_data():
    require_api_value()  # Validate API key

    #Get the arguments passed with the GET request:
    user_id = request.args.get('id')
    phone_number = request.args.get('phone-number')
    email_address = request.args.get('email-address')

    #retrieve the user data based on the arguments of the GET request
    if user_id:
        user_data = df[df['user-id'] == user_id]
    elif phone_number:
        user_data = df[df['phone-number'] == phone_number]
    elif email_address:
        user_data = df[df['email-address'] == email_address]
    else:
        return jsonify({'error': 'Please provide either user-id, phone-number, or email-address'}), 400

    #return an error if no arguments are passed with the GET request
    if user_data.empty:
        return jsonify({'error': 'User not found'}), 404

    
    user_record = user_data.to_dict(orient='records')[0] #get the user record
    points_array = parse_points(user_record['points[#,date-of-expiry]']) #get the points of the user

    #generate the response
    response = {
        'user-id': user_record['user-id'],
        'points': points_array
    }

    #return the response
    return jsonify(response), 200

##########
## POST ##
##########
@app.route('/loyalty/post/add', methods=['POST'])
def add_user_points():
    require_api_value() 

    # Extract query parameters
    data = request.get_json()
    user_id = data.get('user-id')
    new_points = data.get('points')
    new_valid_until = data.get('valid-until')

    # Validate input parameters
    if not all([user_id, new_points, new_valid_until]):
        return jsonify({'error': 'Please provide user-id, points, and valid-until'}), 400

    #Validate that the passed "points" variable is an integer
    try:
        new_points = int(new_points)
    except ValueError:
        return jsonify({'error': 'Points must be an integer'}), 400

    #append the points you want to add
    append_points(user_id,new_points,new_valid_until)

    return jsonify({'message': 'Points added successfully'}), 200

@app.route('/loyalty/post/deduct', methods=['POST'])
def deduct_user_points():
    require_api_value()  

    # Extract query parameters
    data = request.get_json()
    user_id = data.get('user-id')
    points_to_be_deducted = data.get('points')

    # Validate input parameters
    if not all([user_id, points_to_be_deducted]):
        return jsonify({'error': 'Please provide user-id and points'}), 400

    try:
        points_to_be_deducted = int(points_to_be_deducted)
    except ValueError:
        return jsonify({'error': 'Points must be an integer'}), 400

    if points_to_be_deducted>get_user_total_points(user_id):
        return jsonify({'error': 'Insufficient points'}), 401
    
    #deduct the points you want to deduct
    deduct_points(user_id, points_to_be_deducted)
    
    return jsonify({'message': 'Points deducted successfully'}), 200
    

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
