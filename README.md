# Setting up
1. Install python3 and pip3, specific versions shouldn't matter
2. Run pip3 install -r requirements.txt
3. In reimagine.py, update API_KEY string with your api key

# Example Commands
You can run python3 reimagine.py <command-name> for details on args, types

1. Uses the GET /atms endpoint.
- python3 reimagine.py get-atms -b 1 -e 10

2. Uses at least one endpoint for customers, accounts and bills, two of which must be a POST request.
Run in-order so you have a customer id/ account to work with.</b>
- python3 reimagine.py create-new-customer -f Ryan -l Reynolds --street_number 100 --street_name "Hollywood Blvd" -c "Los Angeles" --state CA -z 90100
- python3 reimagine.py create-new-savings-account -c <customer_id> -n "Nickname"
- python3 reimagine.py get-customer-purchases

3. Uses one purchase endpoint
Included in:
- python3 reimagine.py get-customer-purchases

4. Uses one money movement endpoint (deposit, withdrawal, transfer) that is NOT a GET request
- python3 reimagine.py add-deposit --amount 100 --account_id <savings_account_id>

5. Uses one enterprise endpoint
- python3 reimagine.py get-merchants

6. Use the DELETE /data endpoint to delete a data entity(Accounts, Customers, etc) of your choice
- python3 reimagine.py delete-customers
