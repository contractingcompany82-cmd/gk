import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="🏭 Smart Inventory ERP", layout="wide", page_icon="📦")

# --- INITIALIZE DATABASE (SESSION STATE) ---
# Real life me yahan SQL Database connect hoga. Abhi demo ke liye hum Session State use kar rahe hain.

if 'inventory' not in st.session_state:
    # Sample Inventory Data
    st.session_state['inventory'] = pd.DataFrame([
        {'ID': 'ITM-001', 'Name': 'Cement Bags', 'Category': 'Raw Material', 'Stock': 50, 'Reorder_Level': 20, 'Price': 350},
        {'ID': 'ITM-002', 'Name': 'Steel Rods (10mm)', 'Category': 'Raw Material', 'Stock': 100, 'Reorder_Level': 50, 'Price': 1200},
        {'ID': 'ITM-003', 'Name': 'Safety Helmets', 'Category': 'Safety Gear', 'Stock': 5, 'Reorder_Level': 10, 'Price': 150},
        {'ID': 'ITM-004', 'Name': 'Drill Machine', 'Category': 'Tools', 'Stock': 12, 'Reorder_Level': 5, 'Price': 4500},
    ])

if 'suppliers' not in st.session_state:
    st.session_state['suppliers'] = ["Alpha Traders", "BuildMat Corp", "Factory Direct Ltd"]

if 'transactions' not in st.session_state:
    st.session_state['transactions'] = pd.DataFrame(columns=['Date', 'Type', 'Item', 'Quantity', 'Party', 'Total_Value'])

# --- SIDEBAR ---
st.sidebar.title("🏭 ERP Menu")
menu = st.sidebar.radio("Go to:", ["Dashboard", "Stock In / Purchase", "Stock Out / Sales", "Inventory Master", "Reports"])

# --- HELPER FUNCTIONS ---
def get_stock(item_name):
    df = st.session_state['inventory']
    return df.loc[df['Name'] == item_name, 'Stock'].values[0]

def update_stock(item_name, qty, transaction_type):
    df = st.session_state['inventory']
    idx = df[df['Name'] == item_name].index[0]
    
    if transaction_type == "IN":
        df.at[idx, 'Stock'] += qty
    elif transaction_type == "OUT":
        df.at[idx, 'Stock'] -= qty
    
    st.session_state['inventory'] = df

# --- 1. DASHBOARD ---
if menu == "Dashboard":
    st.title("📊 Inventory Dashboard")
    
    df = st.session_state['inventory']
    
    # KPIS
    col1, col2, col3, col4 = st.columns(4)
    total_stock_value = (df['Stock'] * df['Price']).sum()
    low_stock_count = len(df[df['Stock'] <= df['Reorder_Level']])
    
    col1.metric("Total Items", len(df))
    col2.metric("Total Stock Value", f"₹ {total_stock_value:,}")
    col3.metric("Low Stock Alerts", low_stock_count, delta_color="inverse")
    col4.metric("Suppliers", len(st.session_state['suppliers']))
    
    st.markdown("---")
    
    # Low Stock Alert Section
    if low_stock_count > 0:
        st.error(f"⚠️ **Action Required:** {low_stock_count} items are below reorder level!")
        low_stock_items = df[df['Stock'] <= df['Reorder_Level']]
        st.dataframe(low_stock_items[['Name', 'Stock', 'Reorder_Level', 'Category']], use_container_width=True)
    else:
        st.success("✅ All stock levels are healthy.")

    # Charts
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df, x='Name', y='Stock', color='Category', title="Current Stock Levels")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.pie(df, names='Category', values='Stock', title="Inventory Distribution")
        st.plotly_chart(fig2, use_container_width=True)

# --- 2. STOCK IN (PURCHASE) ---
elif menu == "Stock In / Purchase":
    st.title("📥 Stock In (Purchase/Production)")
    
    with st.form("stock_in_form"):
        col1, col2 = st.columns(2)
        item = col1.selectbox("Select Item", st.session_state['inventory']['Name'].unique())
        supplier = col2.selectbox("Supplier / Source", st.session_state['suppliers'])
        
        qty = col1.number_input("Quantity Received", min_value=1, value=10)
        cost = col2.number_input("Total Cost (Optional)", min_value=0.0)
        
        submit = st.form_submit_button("Add to Stock")
        
        if submit:
            update_stock(item, qty, "IN")
            
            # Log Transaction
            new_trans = {
                'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'Type': 'Purchase (In)',
                'Item': item,
                'Quantity': qty,
                'Party': supplier,
                'Total_Value': cost
            }
            st.session_state['transactions'] = pd.concat([st.session_state['transactions'], pd.DataFrame([new_trans])], ignore_index=True)
            
            st.success(f"✅ {qty} units of {item} added successfully!")

# --- 3. STOCK OUT (SALES) ---
elif menu == "Stock Out / Sales":
    st.title("📤 Stock Out (Sales/Usage)")
    
    with st.form("stock_out_form"):
        col1, col2 = st.columns(2)
        item = col1.selectbox("Select Item", st.session_state['inventory']['Name'].unique())
        buyer = col2.text_input("Customer / Department Name", "Cash Counter")
        
        current_available = get_stock(item)
        st.info(f"Available Stock: **{current_available}** units")
        
        qty = col1.number_input("Quantity", min_value=1, max_value=int(current_available))
        
        # Calculate Price
        unit_price = st.session_state['inventory'].loc[st.session_state['inventory']['Name'] == item, 'Price'].values[0]
        total_bill = qty * unit_price
        col2.metric("Total Bill Amount", f"₹ {total_bill:,}")
        
        submit = st.form_submit_button("Process Order")
        
        if submit:
            if qty > current_available:
                st.error("❌ Not enough stock!")
            else:
                update_stock(item, qty, "OUT")
                 # Log Transaction
                new_trans = {
                    'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'Type': 'Sale (Out)',
                    'Item': item,
                    'Quantity': qty,
                    'Party': buyer,
                    'Total_Value': total_bill
                }
                st.session_state['transactions'] = pd.concat([st.session_state['transactions'], pd.DataFrame([new_trans])], ignore_index=True)
                st.success(f"✅ Order Processed! Bill: ₹ {total_bill}")
                st.rerun()

# --- 4. INVENTORY MASTER ---
elif menu == "Inventory Master":
    st.title("📦 Product Master Data")
    
    tab1, tab2 = st.tabs(["View All Items", "Add New Item"])
    
    with tab1:
        st.dataframe(st.session_state['inventory'], use_container_width=True)
        
    with tab2:
        st.subheader("Add New Product")
        with st.form("add_item"):
            c1, c2 = st.columns(2)
            new_name = c1.text_input("Item Name")
            new_cat = c2.selectbox("Category", ["Raw Material", "Finished Goods", "Tools", "Safety Gear", "Electronics"])
            new_stock = c1.number_input("Opening Stock", min_value=0)
            new_reorder = c2.number_input("Low Stock Alert Level", min_value=5)
            new_price = c1.number_input("Unit Price", min_value=0.0)
            
            if st.form_submit_button("Create Item"):
                new_id = f"ITM-{random.randint(100,999)}" if 'random' in globals() else f"ITM-{len(st.session_state['inventory'])+1:03d}"
                new_entry = {
                    'ID': new_id, 'Name': new_name, 'Category': new_cat, 
                    'Stock': new_stock, 'Reorder_Level': new_reorder, 'Price': new_price
                }
                st.session_state['inventory'] = pd.concat([st.session_state['inventory'], pd.DataFrame([new_entry])], ignore_index=True)
                st.success(f"Item {new_name} added!")

# --- 5. REPORTS ---
elif menu == "Reports":
    st.title("📑 Transaction History")
    
    df = st.session_state['transactions']
    
    # Filters
    filter_type = st.radio("Filter by Type:", ["All", "Purchase (In)", "Sale (Out)"], horizontal=True)
    
    if filter_type != "All":
        df = df[df['Type'] == filter_type]
    
    st.dataframe(df, use_container_width=True)
    
    # Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Report (CSV)", data=csv, file_name="inventory_report.csv", mime="text/csv")
