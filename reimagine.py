#!/bin/bash
"""Python program used to hit apis found at http://api.reimaginebanking.com/"""
import click
import requests
import json
import sys

API_KEY = "PLACE API KEY HERE"
REIMAGINE_URL = "http://api.reimaginebanking.com"

@click.group()
def reimagine_apis():
    """Program to hit apis found at http://api.reimaginebanking.com/."""

@click.option('-b', '--beginning_page', default=1, type=int, help='Beginning page you want to return.')
@click.option('-e', '--end_page', default=1, type=int, help='End page you want to return.')
@reimagine_apis.command()
def get_atms(beginning_page: int, end_page: int):
    """List atms for pages supplied (end inclusive). By default gives you first page."""
    atms_url = "/atms"
    current_page = beginning_page # readibility
    for current_page in range(beginning_page, end_page + 1):
        atms_response = requests.get(REIMAGINE_URL + atms_url,
                                     params={"key": API_KEY,
                                            "page": current_page})
        print(atms_response.content)

@click.option('-c', '--customer_id', help='Customer id you want to search.')
@reimagine_apis.command()
def get_customer_purchases(customer_id):
    """Gets all customers, optionally by id."""
    customers_url = "/customers"
    if customer_id:
        customers_response = requests.get(REIMAGINE_URL + customers_url + "/{}".format(customer_id),
                                          params={"key": API_KEY})
        customer_json = [json.loads(customers_response.content)]
    else:
        customers_response = requests.get(REIMAGINE_URL + customers_url, params={"key": API_KEY})
        customer_json = json.loads(customers_response.content)
    accounts_url = "/customers/{}/accounts"
    purchases_url = "/accounts/{}/purchases"
    for customer in customer_json:
        print("Customer payload: {}".format(customer))
        account_response = requests.get(REIMAGINE_URL + accounts_url.format(customer['_id']), 
                                        params={"key": API_KEY})
        account_json = json.loads(account_response.content)
        if len(account_json) > 0:
            purchases_response = requests.get(REIMAGINE_URL + purchases_url.format(account_json[0]['_id']),
                                              params={"key": API_KEY})
            print(purchases_response.content)
        else:
            print("No purchases associated with customer id {}".format(customer['_id']))

@click.option('-c', '--customer_id', help='Customer id you want to create an acoount for. (Ex 5e5db5fc322fa016762f3adf).')
@click.option('-n', '--nickname', help='Account nickname')
@reimagine_apis.command()
def create_new_savings_account(customer_id, nickname):
    """Posts a new account object for customer id."""
    accounts_url = "/customers/{}/accounts"
    accounts_response = requests.post(REIMAGINE_URL + accounts_url.format(customer_id), params={"key": API_KEY},
                                  json={"type": "Savings", "nickname": nickname, "balance":0, "rewards":0})
    print(accounts_response.content)

@click.option('-f', '--first_name', help='First name of customer.')
@click.option('-l', '--last_name', help='Last name of customer.')
@click.option('--street_number', help='Street Number.', type=int)
@click.option('--street_name', help='Street name.')
@click.option('-c', '--city', help='City.')
@click.option('--state', help='State, must be the state\'s initials.')
@click.option('-z', '--zip_code', help='Zip code.', type=int)
@reimagine_apis.command()
def create_new_customer(first_name, last_name, street_number, street_name, city, state, zip_code):
    """Creates a new customer. Follow argument help guidelines."""
    if len(state) > 2:
        sys.exit("""Error: state must be initials""")
    customer_url = "/customers"
    address = {
        "street_number": str(street_number),
        "street_name": street_name,
        "city": city,
        "state": state,
        "zip": str(zip_code)
    }
    customer_response = requests.post(REIMAGINE_URL + customer_url, params={"key": API_KEY},
                                  json={"first_name": first_name, "last_name": last_name, "address": address},
                                  headers={'content-type':'application/json'})
    print(customer_response.content)

@click.option('-a', '--amount', type=int, help='Amount for deposit.')
@click.option('-i', '--account_id', help='Account id you want to search.')
@reimagine_apis.command()
def add_deposit(amount, account_id):
    deposits_url = "/accounts/{}/deposits"
    deposit_response = requests.post(REIMAGINE_URL + deposits_url.format(account_id),
                                    params={"key": API_KEY},
                                    json={"medium": "balance", "transaction_date": "2020-03-20", "status": "pending", "description": "Deposit", "amount": amount},
                                    headers={'content-type':'application/json'})
    print(deposit_response.content)

@reimagine_apis.command()
def get_merchants():
    merchant_url = "/enterprise/merchants"
    merchant_response = requests.get(REIMAGINE_URL + merchant_url, params={"key": API_KEY})
    print(merchant_response.content)

@reimagine_apis.command()
def delete_customers():
    data_url = "/data"
    data_response = requests.delete(REIMAGINE_URL + data_url, params={"key": API_KEY, "type": "Customers"},
                                    headers={'content-type':'application/json'})
    print(data_response.status_code)

if __name__ == '__main__':
    reimagine_apis()