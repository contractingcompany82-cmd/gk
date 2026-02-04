import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Smart Inventory ERP", layout="wide", page_icon="🏭")

# --- DATABASE SIMULATION (Session State) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {'Item_ID': 'P001', 'Name': 'Steel Pipe', 'Stock': 50, 'Min_Limit': 20, 'Price': 500, 'Category': 'Raw Material'},
        {'Item_ID': 'P002', 'Name': 'Safety Shoes', 'Stock': 5, 'Min_Limit': 10, 'Price': 1200, 'Category': 'Safety'}
    ])

if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=['Date', 'Item', 'Type', 'Qty', 'User', 'Party'])

# --- AUTHENTICATION ---
def login():
    st.title("🔐 Inventory Login")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.rerun()
            elif username == "user" and password == "user123":
                st.session_state.logged_in = True
                st.session_state.role = "User"
                st.rerun()
            else:
                st.error("Ghalat details! Admin: admin/admin123, User: user/user123")

if not st.session_state.logged_in:
    login()
else:
    # --- SIDEBAR ---
    st.sidebar.title(f"👤 Role: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ADMIN PANEL ---
    if st.session_state.role == "Admin":
        menu = st.sidebar.radio("Navigation", ["Dashboard", "Manage Inventory", "Stock In (Purchase)", "Suppliers", "Reports"])

        if menu == "Dashboard":
            st.title("📊 Admin Dashboard")
            inv = st.session_state.inventory
            
            # KPI Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Items", len(inv))
            stock_val = (inv['Stock'] * inv['Price']).sum()
            c2.metric("Inventory Value", f"₹{stock_val:,}")
            
            low_stock = inv[inv['Stock'] < inv['Min_Limit']]
            c3.metric("Low Stock Alerts", len(low_stock), delta_color="inverse")

            if not low_stock.empty:
                st.error("⚠️ In cheezon ka stock khatam ho raha hai!")
                st.dataframe(low_stock)

            st.subheader("Stock Summary")
            st.dataframe(inv, use_container_width=True)

        elif menu == "Manage Inventory":
            st.title("⚙️ Add/Update Items")
            with st.form("add_item"):
                name = st.text_input("Item Name")
                price = st.number_input("Unit Price", min_value=1)
                limit = st.number_input("Minimum Stock Limit", min_value=1)
                cat = st.selectbox("Category", ["Raw Material", "Finished Goods", "Tools"])
                if st.form_submit_button("Add Item"):
                    new_item = {'Item_ID': f"P00{len(st.session_state.inventory)+1}", 'Name': name, 'Stock': 0, 'Min_Limit': limit, 'Price': price, 'Category': cat}
                    st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_item])], ignore_index=True)
                    st.success("Naya item add ho gaya!")

        elif menu == "Stock In (Purchase)":
            st.title("📥 Purchase / Stock In")
            item = st.selectbox("Select Item", st.session_state.inventory['Name'])
            qty = st.number_input("Quantity", min_value=1)
            supplier = st.text_input("Supplier Name")
            if st.button("Add Stock"):
                st.session_state.inventory.loc[st.session_state.inventory['Name'] == item, 'Stock'] += qty
                new_t = {'Date': datetime.now(), 'Item': item, 'Type': 'IN', 'Qty': qty, 'User': 'Admin', 'Party': supplier}
                st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_t])], ignore_index=True)
                st.success(f"{qty} {item} stock mein add ho gaye.")

        elif menu == "Reports":
            st.title("📑 Full Transaction Reports")
            st.dataframe(st.session_state.transactions, use_container_width=True)

    # --- USER PANEL (Restricted) ---
    else:
        menu = st.sidebar.radio("Navigation", ["Stock Out (Sales/Dispatch)", "Check Stock"])
        
        if menu == "Stock Out (Sales/Dispatch)":
            st.title("📤 Stock Out (Usage/Sales)")
            item = st.selectbox("Select Item", st.session_state.inventory['Name'])
            current_stock = st.session_state.inventory.loc[st.session_state.inventory['Name'] == item, 'Stock'].values[0]
            st.write(f"Current Stock: **{current_stock}**")
            
            qty = st.number_input("Quantity to Dispatch", min_value=1, max_value=int(current_stock))
            customer = st.text_input("Customer / Department Name")
            
            if st.button("Dispatch"):
                if current_stock >= qty:
                    st.session_state.inventory.loc[st.session_state.inventory['Name'] == item, 'Stock'] -= qty
                    new_t = {'Date': datetime.now(), 'Item': item, 'Type': 'OUT', 'Qty': qty, 'User': 'User', 'Party': customer}
                    st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_t])], ignore_index=True)
                    st.success(f"{item} dispatch ho gaya!")
                else:
                    st.error("Stock kam hai!")

        elif menu == "Check Stock":
            st.title("🔍 View Available Stock")
            st.dataframe(st.session_state.inventory[['Item_ID', 'Name', 'Stock', 'Category']])
