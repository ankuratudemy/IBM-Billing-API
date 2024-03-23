### Flask API for IBM Billing Data

This repository contains a Flask application that provides an API for fetching IBM billing data. The API supports retrieving both resource group usage and resource instance usage data for specified regions and account ID. It also includes a simple HTML page to display the fetched data in a table format.

#### Installation and Usage

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository

2. run app.py as api locally:

   curl --location 'http://127.0.0.1:5000/billing' \
  --header 'Content-Type: application/json' \
  --data '{
  "resourceInstanceUsage": true,
  "apiKey": "<apiKey>",
  "regionCodes": ["ca-tor","us-south"],
  "accountId": "<account-id>",
  "billMonth": "2024-01"
}'
