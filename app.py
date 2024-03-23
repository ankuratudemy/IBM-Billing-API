from flask import Flask, request, jsonify
import requests
import datetime
from os.path import expanduser

app = Flask(__name__)

# Function to fetch IBM login API bearer token
def getBearerToken(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get('access_token')

# Define the main logic to process resource group usage
def processResourceGroupUsage(account_id, region_codes, billMonth, iam_token):
    METERING_HOST = "https://billing.cloud.ibm.com"
    aggregated_data = []
    for region_code in region_codes:
        METERING_URL = f"/v4/accounts/{account_id}/resource_groups/usage/{billMonth}?region={region_code}&_names=true"
        url = METERING_HOST + METERING_URL
        headers = {
            "Authorization": f"Bearer {iam_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        aggregated_data.append(response.json())
    return aggregated_data

# Define the main logic to process resource instance usage
def processResourceInstanceUsage(account_id, region_codes, billMonth, iam_token):
    METERING_HOST = "https://billing.cloud.ibm.com"
    aggregated_data = {}  # Dictionary to store data for each region

    for region_code in region_codes:
        region_aggregated_data = []  # List to store data for the current region
        url = f"{METERING_HOST}/v4/accounts/{account_id}/resource_instances/usage/{billMonth}?region={region_code}&_limit=30&_names=true"
        headers = {
            "Authorization": f"Bearer {iam_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        while url:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "resources" in data:
                    region_aggregated_data.extend(data["resources"])  # Append resources part to region_aggregated_data
                else:
                    print(f"No resources found in response for region {region_code}.")
                url = data.get('next')
                if url:
                    print(url)
                    url = f"{METERING_HOST}"+ url["href"]  # Get the next URL if available  # Update URL for next iteration
            else:
                print(f"Failed to fetch data for region {region_code}. Status code: {response.status_code}")
                break  # Exit the loop on failure

        aggregated_data[region_code] = region_aggregated_data  # Store aggregated data for the current region

    return aggregated_data
@app.route('/billing', methods=['POST'])
def billing():
    # Get parameters from the request JSON body
    request_json = request.get_json()
    print(request_json)
    api_key = request_json.get("apiKey")
    region_codes = request_json.get("regionCodes", ["ca-tor"])
    print(region_codes)
    account_id = request_json.get("accountId", "")
    billMonth = request_json.get("billMonth", datetime.datetime.now().strftime("%Y-%m"))

    if not api_key:
        return jsonify({"error": "API key is required"}), 400

    # Fetch IBM login API bearer token
    iam_token = getBearerToken(api_key)

    if not region_codes:
        return jsonify({"error": "Region codes are required"}), 400

    # Process resource group usage for each region code
    # aggregated_data = processResourceGroupUsage(account_id, region_codes, billMonth, iam_token)

    # Process resource instance usage for each region code
    aggregated_data = processResourceInstanceUsage(account_id, region_codes, billMonth, iam_token)

    return jsonify(aggregated_data)

if __name__ == '__main__':
    app.run(debug=True)
