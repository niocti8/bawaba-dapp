import streamlit as st
from web3 import Web3
from hashlib import sha256
from geopy.geocoders import Nominatim
import pandas as pd
import csv
import os
from datetime import datetime
import time

# RSK setup (simulated)
w3 = Web3(Web3.HTTPProvider('https://public-node.testnet.rsk.co'))
contract_address = "0xSimulatedAddress"
contract_abi = [{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"vendor","type":"address"},{"internalType":"bytes32","name":"orderId","type":"bytes32"}],"name":"claimReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"usedOrderIds","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]
contract = w3.eth.contract(address=contract_address, abi=contract_abi)
EXA_ADDRESS = "0xSimulatedExaAddress"
EXA_PRIVATE_KEY = "simulated_key"

# File setup
VENDORS_FILE = "vendors.csv"
ITEMS_FILE = "items.csv"
ORDERS_FILE = "orders.csv"
UPLOADS_FILE = "uploads.csv"
for file, headers in [
    (VENDORS_FILE, ["vendor_name", "ogo_api_key", "knet_merchant_id", "vendor_wallet", "icon"]),
    (ITEMS_FILE, ["vendor_name", "item_name", "price_kwd", "description"]),
    (ORDERS_FILE, ["order_id", "vendor", "item", "address", "user_wallet", "lat", "lon", "timestamp"]),
    (UPLOADS_FILE, ["order_id", "vendor", "user_wallet", "timestamp", "item", "price_kwd"])
]:
    if not os.path.exists(file):
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        if file == VENDORS_FILE:
            with open(file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["FluxEats", "", "sim123", "0xVendor1", "🌌"])
                writer.writerow(["NebulaBites", "", "sim456", "0xVendor2", "☄️"])

def load_vendors(): return pd.read_csv(VENDORS_FILE).set_index("vendor_name").to_dict("index")
def load_items(): return pd.read_csv(ITEMS_FILE)
def get_user_tier(wallet):
    orders_df = pd.read_csv(ORDERS_FILE)
    uploads_df = pd.read_csv(UPLOADS_FILE)
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    orders = len(orders_df[(orders_df["user_wallet"] == wallet) & (pd.to_datetime(orders_df["timestamp"]) >= month_start)])
    uploads = len(uploads_df[(uploads_df["user_wallet"] == wallet) & (pd.to_datetime(uploads_df["timestamp"]) >= month_start)])
    total = orders + uploads
    if total >= 10: return "Gold", 300000, 1.2
    elif total >= 5: return "Silver", 250000, 1.1
    return "Bronze", 210000, 1.0

# Simulated APIs
def process_knet_payment(vendor, item, price_kwd, merchant_id):
    return {"transaction_id": f"KNET-{sha256(str([vendor, item]).encode()).hexdigest()[:8]}"}

def dispatch_ogo_delivery(vendor, item, delivery_address, api_key):
    return "Dispatched" if api_key else "Self-managed"

# Aether Flux Mascot and Bawaba Logo
def aether_flux(): return '<span class="aether-flux">✨</span>'
def bawaba_logo():
    return '''
    <div class="bawaba-logo">
        <span class="eternal-gate">∞</span>
        <span class="gate-orb">•</span>
        <span class="bawaba-text">Bawaba</span>
    </div>
    '''

st.markdown("""
    <style>
    .bawaba-logo { text-align: center; margin-bottom: 20px; position: relative; }
    .eternal-gate { font-size: 50px; background: linear-gradient(to top, #4B0082, #00CED1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 10px #00CED1; transform: rotate(90deg); display: inline-block; }
    .gate-orb { font-size: 14px; color: #FFD700; text-shadow: 0 0 5px #00CED1; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
    .bawaba-text { font-size: 24px; color: #FFFFFF; text-shadow: 0 0 5px #8A2BE2; font-family: 'Exo 2', sans-serif; display: block; margin-top: -10px; }
    .title { font-size: 36px; font-weight: bold; color: #8A2BE2; text-align: center; }
    .subtitle { font-size: 18px; color: #00CED1; text-align: center; margin-bottom: 20px; }
    .success { background-color: #e6f3ff; padding: 10px; border-radius: 8px; color: #1E90FF; }
    .error { background-color: #ffe6e6; padding: 10px; border-radius: 8px; color: #E74C3C; }
    .stButton>button { background-color: #8A2BE2; color: white; border-radius: 8px; padding: 10px; }
    .vendor-icon { font-size: 24px; margin-right: 10px; }
    .aether-flux { font-size: 32px; color: #FFD700; margin-right: 10px; text-shadow: 0 0 10px #00CED1, 0 0 20px #8A2BE2; animation: flux-glow 2s infinite; }
    .portal-door { text-align: center; font-size: 60px; color: #8A2BE2; animation: portal-pulse 2s infinite; }
    .market-stall { background-color: #F0F8FF; padding: 10px; border-radius: 8px; margin: 5px; animation: stall-pop 1s ease-in; }
    .live-feed { font-size: 20px; color: #FFD700; animation: feed-blink 1.5s infinite; }
    @keyframes flux-glow { 0% { text-shadow: 0 0 5px #00CED1, 0 0 10px #8A2BE2; } 50% { text-shadow: 0 0 15px #00CED1, 0 0 25px #8A2BE2; } 100% { text-shadow: 0 0 5px #00CED1, 0 0 10px #8A2BE2; } }
    @keyframes portal-pulse { 0% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.2); opacity: 1; } 100% { transform: scale(1); opacity: 0.8; } }
    @keyframes stall-pop { 0% { transform: scale(0.8); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
    @keyframes feed-blink { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Exo+2&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Order & Claim", "Bawaba Portal", "Living Market", "Vendor Portal"])

# Tab 1: Order & Claim
with tab1:
    st.markdown(bawaba_logo(), unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Order & unlock EXARUNE rewards!</div>', unsafe_allow_html=True)

    items_df = load_items()
    vendors = load_vendors()
    with st.form(key="order_form"):
        wallet_address = st.text_input(f"{aether_flux()} Your Bawaba Wallet", placeholder="e.g., 0x1234...", max_chars=42, unsafe_allow_html=True)
        vendor_name = st.selectbox("Select Vendor", options=vendors.keys(), format_func=lambda x: f'<span class="vendor-icon">{vendors[x]["icon"]}</span> {x}', unsafe_allow_html=True)
        item_options = items_df[items_df["vendor_name"] == vendor_name]["item_name"].tolist()
        item = st.selectbox("Select Item", options=item_options) if item_options else st.write("No items yet!")
        price_kwd = items_df[(items_df["vendor_name"] == vendor_name) & (items_df["item_name"] == item)]["price_kwd"].iloc[0] if item_options else 0
        st.write(f"Price: {price_kwd} KWD")
        delivery_address = st.text_input("Delivery Address", placeholder="e.g., Salmiya, Kuwait")
        submit_button = st.form_submit_button(label="Order & Claim EXARUNE")

    if submit_button:
        if not all([wallet_address, vendor_name, item, delivery_address]):
            st.markdown('<div class="error">Please fill in all fields.</div>', unsafe_allow_html=True)
        elif not wallet_address.startswith("0x") or len(wallet_address) != 42:
            st.markdown('<div class="error">Invalid Bawaba wallet address.</div>', unsafe_allow_html=True)
        else:
            order_id = f"{vendor_name}-{sha256(item.encode()).hexdigest()[:8]}"
            order_hash = "0x" + sha256(order_id.encode()).hexdigest()
            if contract.functions.usedOrderIds(order_hash).call():
                st.markdown('<div class="error">Order already claimed.</div>', unsafe_allow_html=True)
            else:
                knet_result = process_knet_payment(vendor_name, item, price_kwd, vendors[vendor_name]["knet_merchant_id"])
                delivery_result = dispatch_ogo_delivery(vendor_name, item, delivery_address, vendors[vendor_name]["ogo_api_key"])

                tier, user_reward, upload_bonus = get_user_tier(wallet_address)
                vendor_wallet = vendors[vendor_name]["vendor_wallet"]
                nonce = w3.eth.get_transaction_count(EXA_ADDRESS)
                tx = contract.functions.claimReward(wallet_address, vendor_wallet, order_hash).build_transaction({
                    'from': EXA_ADDRESS,
                    'nonce': nonce,
                    'gas': 200000,
                    'gasPrice': w3.to_wei('1', 'gwei')
                })
                signed_tx = w3.eth.account.sign_transaction(tx, EXA_PRIVATE_KEY)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

                geolocator = Nominatim(user_agent="bawaba_rewards")
                location = geolocator.geocode(delivery_address)
                lat, lon = (location.latitude, location.longitude) if location else (0, 0)
                with open(ORDERS_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([order_id, vendor_name, item, delivery_address, wallet_address, lat, lon, datetime.now().isoformat()])

                st.markdown(f'<div class="success">Paid {price_kwd} KWD! {user_reward//10**18}K EXARUNE to you (Tier: {tier}), 50K to vendor. Delivery: {delivery_result}. TX: {tx_hash.hex()}</div>', unsafe_allow_html=True)

# Tab 2: Bawaba Portal (Gamified Receipt Upload)
with tab2:
    st.markdown(bawaba_logo(), unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Step through the Aether Flux to earn!</div>', unsafe_allow_html=True)
    st.markdown('<div class="portal-door">🌐</div>', unsafe_allow_html=True)

    with st.form(key="upload_form"):
        wallet_address = st.text_input(f"{aether_flux()} Your Bawaba Wallet ", placeholder="e.g., 0x1234...", max_chars=42, key="upload_wallet", unsafe_allow_html=True)
        order_id = st.text_input("Order ID", placeholder="e.g., #1234 or CR-123456")
        receipt_vendor = st.text_input("Vendor Name", placeholder="e.g., Talabat")
        receipt_item = st.text_input("Item Purchased", placeholder="e.g., Shawarma")
        receipt_price = st.number_input("Price (KWD)", min_value=0.0, step=0.01)
        upload_button = st.form_submit_button(label="Enter Portal & Claim")

    if upload_button:
        if not all([wallet_address, order_id, receipt_vendor, receipt_item, receipt_price]):
            st.markdown('<div class="error">Please fill in all fields.</div>', unsafe_allow_html=True)
        elif not wallet_address.startswith("0x") or len(wallet_address) != 42:
            st.markdown('<div class="error">Invalid Bawaba wallet address.</div>', unsafe_allow_html=True)
        else:
            order_hash = "0x" + sha256(order_id.encode()).hexdigest()
            if contract.functions.usedOrderIds(order_hash).call():
                st.markdown('<div class="error">Order ID already claimed.</div>', unsafe_allow_html=True)
            else:
                tier, _, upload_bonus = get_user_tier(wallet_address)
                base_reward = 100000 * 10**18
                total_reward = int(base_reward * upload_bonus)
                nonce = w3.eth.get_transaction_count(EXA_ADDRESS)
                tx = contract.functions.claimReward(wallet_address, EXA_ADDRESS, order_hash).build_transaction({
                    'from': EXA_ADDRESS,
                    'nonce': nonce,
                    'gas': 200000,
                    'gasPrice': w3.to_wei('1', 'gwei')
                })
                signed_tx = w3.eth.account.sign_transaction(tx, EXA_PRIVATE_KEY)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

                with open(UPLOADS_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([order_id, receipt_vendor, wallet_address, datetime.now().isoformat(), receipt_item, receipt_price])

                st.markdown(f'<div class="success">Flux Gate opened! {total_reward//10**18}K EXARUNE earned (Tier: {tier})! TX: {tx_hash.hex()}</div>', unsafe_allow_html=True)

# Tab 3: Living Market
with tab3:
    st.markdown(bawaba_logo(), unsafe_allow_html=True)
    st.markdown('<div class="subtitle">A bustling bazaar of Bawaba trades!</div>', unsafe_allow_html=True)

    df_orders = pd.read_csv(ORDERS_FILE)
    if not df_orders.empty and "lat" in df_orders.columns and "lon" in df_orders.columns:
        df_filtered = df_orders[df_orders["lat"] != 0]
        if not df_filtered.empty:
            st.map(df_filtered, zoom=10, use_container_width=True)

    st.write("### Market Stalls")
    df_uploads = pd.read_csv(UPLOADS_FILE)
    vendors = load_vendors()
    if not df_uploads.empty:
        for _, row in df_uploads.tail(5).iterrows():
            vendor_icon = vendors.get(row["vendor"], {}).get("icon", "🛒")
            st.markdown(f'<div class="market-stall">{vendor_icon} {row["vendor"]} - {row["item"]} ({row["price_kwd"]} KWD) - Uploaded by {row["user_wallet"][:6]}...</div>', unsafe_allow_html=True)
            time.sleep(0.5)
        st.write("Browse stalls above—more features coming soon!")

    st.write("### Live Vendor Feed")
    with st.expander("FluxEats Live Order (Simulated)"):
        st.markdown('<span class="live-feed">📸</span> Now preparing: Cosmic Wrap!', unsafe_allow_html=True)
    with st.expander("NebulaBites Live Order (Simulated)"):
        st.markdown('<span class="live-feed">📸</span> Now preparing: Stellar Pizza!', unsafe_allow_html=True)

# Tab 4: Vendor Portal
with tab4:
    st.markdown(bawaba_logo(), unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Launch your items with Bawaba!</div>', unsafe_allow_html=True)

    with st.form(key="vendor_form"):
        vendor_name = st.text_input("Vendor Name", placeholder="e.g., FluxEats")
        item_name = st.text_input("Item Name", placeholder="e.g., Cosmic Wrap")
        price_kwd = st.number_input("Price (KWD)", min_value=0.0, step=0.01)
        description = st.text_area("Description", placeholder="e.g., Stellar spiced wrap")
        vendor_wallet = st.text_input(f"{aether_flux()} Vendor Bawaba Wallet", placeholder="e.g., 0x5678...", max_chars=42, unsafe_allow_html=True)
        vendor_icon = st.selectbox("Choose Your Icon", options=["🌌", "☄️", "🌀", "🌠", "💫"])
        add_button = st.form_submit_button(label="Add Item")

    if add_button:
        if not all([vendor_name, item_name, price_kwd, description, vendor_wallet]):
            st.markdown('<div class="error">Please fill in all required fields.</div>', unsafe_allow_html=True)
        elif not vendor_wallet.startswith("0x") or len(vendor_wallet) != 42:
            st.markdown('<div class="error">Invalid Bawaba wallet address.</div>', unsafe_allow_html=True)
        else:
            with open(ITEMS_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([vendor_name, item_name, price_kwd, description])
            vendors_data = load_vendors()
            if vendor_name not in vendors_data:
                with open(VENDORS_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([vendor_name, "", "simulated_id", vendor_wallet, vendor_icon])
            st.markdown(f'<div class="success">Item {item_name} added for {vendor_name} {vendor_icon}!</div>', unsafe_allow_html=True)

st.markdown("---")
st.write("Powered by Bawaba & Rootstock | Gate to Tomorrow")
