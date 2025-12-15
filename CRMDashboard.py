import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import io
import hashlib

# Page configuration
st.set_page_config(page_title="LASER CRM Dashboard", layout="wide", initial_sidebar_state="expanded")

# Authentication function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# User credentials (in production, use a secure database)
USERS = {
    'admin': {'password': hash_password('admin123'), 'role': 'admin'},
    'user': {'password': hash_password('user123'), 'role': 'user'}
}

# Initialize data in session state
def initialize_data():
    if 'clients_df' not in st.session_state:
        st.session_state.clients_df = pd.DataFrame({
            'Client Name': ['Between Coffee and Vine', 'TATU Capital', 'Tigzozo Media', 'Tourism Industry Pension Fund'],
            'Status': ['Active', 'Active', 'Completed', 'Proposal'],
            'Client Tier': ['Tier 2 - Standard', 'Tier 1 - Premium', 'Tier 1 - Premium', 'Tier 4 - Project-based'],
            'First Engagement': ['2025-03-01', '2024-03-01', '2024-12-01', '2023-11-01'],
            'Service Categories': ['HR Administration', 'Training & Development', 'HR Administration', 'Business Consulting'],
            'Monthly Recurring Revenue': [200, 400, 0, 0],
            'Total Revenue': [200, 400, 300, 1850],
            'Lifetime Value': [2400, 7000, 3300, 1850],
            'Consultants': ['Rebecca', 'Rebecca', 'Rebecca', 'Rebecca'],
            'Referral Source': ['Patience Mapeza - WBP connection', 'Mrs Phiri', 'Brenald Chinyowa from Mrs Phiri', 'Munja Nheta (UCPF)']
        })
    
    if 'services_df' not in st.session_state:
        st.session_state.services_df = pd.DataFrame({
            'Client Name': ['TATU Capital', 'Tigzozo Media', 'Between Coffee and Vine', 'Tourism Industry Pension Fund'],
            'Service Category': ['Training & Development', 'HR Administration', 'HR Administration', 'Business Consulting'],
            'Nature of Assignment': ['Training and Development', 'HR Administration', 'HR Administration', 'Business Consulting'],
            'Services Provided': ['Grooming and Deportment Training', 'Payroll Administration, Policy Design', 'Payroll Administration, Policy Design', 'Strategic Review'],
            'Date Engaged': ['2025-08-03', '2024-12-01', '2025-03-01', '2023-11-01'],
            'End Date': ['Once off', 'October 2025', None, None],
            'Status': ['Completed', 'Completed', 'Active', 'Proposal'],
            'Revenue Type': ['One-time', 'Recurring', 'Recurring', 'One-time'],
            'Revenue': [250, 300, 200, 0],
            'Monthly Recurring Revenue': [0, 0, 200, 0],
            'Consultant Assigned': ['Rebecca', 'Rebecca', 'Rebecca', 'Rebecca']
        })
    
    if 'issues_df' not in st.session_state:
        st.session_state.issues_df = pd.DataFrame({
            'Issue': ['Lost 2 recurring clients (Oct 2025)', 'Only 2 active recurring clients', 
                     '54% churn rate on recurring revenue', 'Low proposal conversion'],
            'Impact': ['MRR dropped 54.5% ($600 lost)', 'High revenue concentration risk', 
                      'Unsustainable business model', 'Only $700 in active proposals'],
            'Recommendation': ['Urgent: Win-back campaign + retention strategy', 
                             'Convert proposals to recurring contracts',
                             'Implement customer success program',
                             'Accelerate sales cycle, focus on high-value prospects']
        })
    
    if 'opportunities_df' not in st.session_state:
        st.session_state.opportunities_df = pd.DataFrame({
            'Opportunity': ['IDSS - Strategic Plan', 'NECs (20 Organizations)', 
                          'Convert Tier 4 to Recurring', 'Catering Industry Pension Fund',
                          'Tourism Industry Pension Fund'],
            'Potential Value': [2500, 'TBD', '1000+ MRR', 1450, 1200],
            'Priority': ['HIGH - Largest single opportunity', 'HIGH - Massive expansion potential',
                        'CRITICAL - Stabilize revenue', 'MEDIUM - Multiple services',
                        'MEDIUM - Policy Review']
        })

# Login page
def login_page():
    st.title("🔐 LASER CRM Dashboard Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Please login to continue")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Login", use_container_width=True):
                if username in USERS and USERS[username]['password'] == hash_password(password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_role = USERS[username]['role']
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with col_b:
            if st.button("Clear", use_container_width=True):
                st.rerun()
        
        st.info("**Demo Credentials:**\n\nAdmin: `admin` / `admin123`\n\nUser: `user` / `user123`")

# Logout function
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.rerun()

# Main dashboard
def main_dashboard():
    # Sidebar
    with st.sidebar:
        st.title("🎯 LASER CRM")
        st.markdown(f"**User:** {st.session_state.username}")
        st.markdown(f"**Role:** {st.session_state.user_role.upper()}")
        st.markdown("---")
        
        page = st.radio("Navigation", 
                       ["📊 Executive Summary", 
                        "👥 Client Master List", 
                        "📋 Service Engagements",
                        "💰 Revenue Analytics",
                        "👤 Consultant Performance",
                        "🔗 Referral Sources",
                        "⚠️ Issues & Opportunities"])
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    # Main content
    if page == "📊 Executive Summary":
        executive_summary()
    elif page == "👥 Client Master List":
        client_master_list()
    elif page == "📋 Service Engagements":
        service_engagements()
    elif page == "💰 Revenue Analytics":
        revenue_analytics()
    elif page == "👤 Consultant Performance":
        consultant_performance()
    elif page == "🔗 Referral Sources":
        referral_sources()
    elif page == "⚠️ Issues & Opportunities":
        issues_opportunities()

# Executive Summary
def executive_summary():
    st.title("📊 Executive Summary")
    
    # Calculate metrics
    total_clients = len(st.session_state.clients_df)
    active_clients = len(st.session_state.clients_df[st.session_state.clients_df['Status'] == 'Active'])
    total_mrr = st.session_state.clients_df['Monthly Recurring Revenue'].sum()
    total_arr = total_mrr * 12
    total_revenue = st.session_state.clients_df['Total Revenue'].sum()
    
    # KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Clients", total_clients)
    with col2:
        st.metric("Active Clients", active_clients)
    with col3:
        st.metric("Monthly Recurring Revenue", f"${total_mrr:,.0f}")
    with col4:
        st.metric("Annual Recurring Revenue", f"${total_arr:,.0f}")
    with col5:
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Client distribution by tier
        tier_counts = st.session_state.clients_df['Client Tier'].value_counts()
        fig = px.pie(values=tier_counts.values, names=tier_counts.index, 
                    title="Client Distribution by Tier")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue by service category
        revenue_by_service = st.session_state.services_df.groupby('Service Category')['Revenue'].sum().sort_values(ascending=False)
        fig = px.bar(x=revenue_by_service.values, y=revenue_by_service.index,
                    orientation='h', title="Revenue by Service Category",
                    labels={'x': 'Revenue ($)', 'y': 'Service Category'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Export button
    if st.button("📥 Export Executive Summary"):
        export_data()

# Client Master List
def client_master_list():
    st.title("👥 Client Master List")
    
    # Add/Edit controls
    if st.session_state.user_role == 'admin':
        with st.expander("➕ Add New Client"):
            with st.form("add_client_form"):
                col1, col2 = st.columns(2)
                with col1:
                    client_name = st.text_input("Client Name")
                    status = st.selectbox("Status", ["Active", "Proposal", "Prospect", "Completed"])
                    client_tier = st.selectbox("Client Tier", 
                                              ["Tier 1 - Premium", "Tier 2 - Standard", 
                                               "Tier 4 - Project-based"])
                    first_engagement = st.date_input("First Engagement")
                    service_categories = st.text_input("Service Categories")
                
                with col2:
                    mrr = st.number_input("Monthly Recurring Revenue", min_value=0, value=0)
                    total_revenue = st.number_input("Total Revenue", min_value=0, value=0)
                    lifetime_value = st.number_input("Lifetime Value", min_value=0, value=0)
                    consultants = st.text_input("Consultants")
                    referral_source = st.text_input("Referral Source")
                
                if st.form_submit_button("Add Client"):
                    new_client = pd.DataFrame({
                        'Client Name': [client_name],
                        'Status': [status],
                        'Client Tier': [client_tier],
                        'First Engagement': [first_engagement.strftime('%Y-%m-%d')],
                        'Service Categories': [service_categories],
                        'Monthly Recurring Revenue': [mrr],
                        'Total Revenue': [total_revenue],
                        'Lifetime Value': [lifetime_value],
                        'Consultants': [consultants],
                        'Referral Source': [referral_source]
                    })
                    st.session_state.clients_df = pd.concat([st.session_state.clients_df, new_client], ignore_index=True)
                    st.success(f"Client '{client_name}' added successfully!")
                    st.rerun()
    
    # Display and edit table
    st.subheader("Client List")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.multiselect("Filter by Status", 
                                       st.session_state.clients_df['Status'].unique(),
                                       default=st.session_state.clients_df['Status'].unique())
    with col2:
        tier_filter = st.multiselect("Filter by Tier",
                                    st.session_state.clients_df['Client Tier'].unique(),
                                    default=st.session_state.clients_df['Client Tier'].unique())
    
    # Apply filters
    filtered_df = st.session_state.clients_df[
        (st.session_state.clients_df['Status'].isin(status_filter)) &
        (st.session_state.clients_df['Client Tier'].isin(tier_filter))
    ]
    
    # Display table
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    # Delete functionality
    if st.session_state.user_role == 'admin':
        st.markdown("---")
        st.subheader("🗑️ Delete Client")
        client_to_delete = st.selectbox("Select client to delete", 
                                       st.session_state.clients_df['Client Name'].tolist())
        if st.button("Delete Client", type="primary"):
            st.session_state.clients_df = st.session_state.clients_df[
                st.session_state.clients_df['Client Name'] != client_to_delete
            ].reset_index(drop=True)
            st.success(f"Client '{client_to_delete}' deleted successfully!")
            st.rerun()

# Service Engagements
def service_engagements():
    st.title("📋 Service Engagements")
    
    # Add service
    if st.session_state.user_role == 'admin':
        with st.expander("➕ Add New Service Engagement"):
            with st.form("add_service_form"):
                col1, col2 = st.columns(2)
                with col1:
                    client_name = st.selectbox("Client Name", 
                                             st.session_state.clients_df['Client Name'].tolist())
                    service_category = st.text_input("Service Category")
                    nature = st.text_input("Nature of Assignment")
                    services_provided = st.text_area("Services Provided")
                    date_engaged = st.date_input("Date Engaged")
                
                with col2:
                    end_date = st.date_input("End Date (optional)", value=None)
                    status = st.selectbox("Status", ["Active", "Completed", "Proposal", "Prospect"])
                    revenue_type = st.selectbox("Revenue Type", ["One-time", "Recurring"])
                    revenue = st.number_input("Revenue", min_value=0, value=0)
                    mrr = st.number_input("Monthly Recurring Revenue", min_value=0, value=0)
                    consultant = st.text_input("Consultant Assigned")
                
                if st.form_submit_button("Add Service Engagement"):
                    new_service = pd.DataFrame({
                        'Client Name': [client_name],
                        'Service Category': [service_category],
                        'Nature of Assignment': [nature],
                        'Services Provided': [services_provided],
                        'Date Engaged': [date_engaged.strftime('%Y-%m-%d')],
                        'End Date': [end_date.strftime('%Y-%m-%d') if end_date else None],
                        'Status': [status],
                        'Revenue Type': [revenue_type],
                        'Revenue': [revenue],
                        'Monthly Recurring Revenue': [mrr],
                        'Consultant Assigned': [consultant]
                    })
                    st.session_state.services_df = pd.concat([st.session_state.services_df, new_service], ignore_index=True)
                    st.success("Service engagement added successfully!")
                    st.rerun()
    
    # Display services
    st.subheader("Service Engagements List")
    st.dataframe(st.session_state.services_df, use_container_width=True, hide_index=True)
    
    # Delete service
    if st.session_state.user_role == 'admin':
        st.markdown("---")
        st.subheader("🗑️ Delete Service Engagement")
        service_to_delete = st.selectbox("Select service to delete (by index)", 
                                        range(len(st.session_state.services_df)))
        if st.button("Delete Service", type="primary"):
            st.session_state.services_df = st.session_state.services_df.drop(service_to_delete).reset_index(drop=True)
            st.success("Service engagement deleted successfully!")
            st.rerun()

# Revenue Analytics
def revenue_analytics():
    st.title("💰 Revenue Analytics")
    
    # Calculate metrics
    total_mrr = st.session_state.clients_df['Monthly Recurring Revenue'].sum()
    total_arr = total_mrr * 12
    total_project_revenue = st.session_state.services_df[
        st.session_state.services_df['Revenue Type'] == 'One-time'
    ]['Revenue'].sum()
    
    recurring_clients = len(st.session_state.clients_df[
        st.session_state.clients_df['Monthly Recurring Revenue'] > 0
    ])
    avg_revenue_per_client = st.session_state.clients_df['Total Revenue'].mean()
    
    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total MRR", f"${total_mrr:,.0f}")
    with col2:
        st.metric("Annual Recurring Revenue", f"${total_arr:,.0f}")
    with col3:
        st.metric("Total Project Revenue", f"${total_project_revenue:,.0f}")
    with col4:
        st.metric("Recurring Clients", recurring_clients)
    with col5:
        st.metric("Avg Revenue/Client", f"${avg_revenue_per_client:,.0f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # MRR by client tier
        mrr_by_tier = st.session_state.clients_df.groupby('Client Tier')['Monthly Recurring Revenue'].sum()
        fig = px.bar(x=mrr_by_tier.index, y=mrr_by_tier.values,
                    title="Monthly Recurring Revenue by Client Tier",
                    labels={'x': 'Client Tier', 'y': 'MRR ($)'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue by status
        revenue_by_status = st.session_state.clients_df.groupby('Status')['Total Revenue'].sum()
        fig = px.pie(values=revenue_by_status.values, names=revenue_by_status.index,
                    title="Total Revenue by Client Status")
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.subheader("Revenue Breakdown")
    revenue_summary = st.session_state.clients_df.groupby('Service Categories').agg({
        'Total Revenue': 'sum',
        'Monthly Recurring Revenue': 'sum',
        'Client Name': 'count'
    }).rename(columns={'Client Name': 'Number of Clients'})
    st.dataframe(revenue_summary, use_container_width=True)

# Consultant Performance
def consultant_performance():
    st.title("👤 Consultant Performance")
    
    # Calculate performance metrics
    consultant_metrics = st.session_state.clients_df.groupby('Consultants').agg({
        'Client Name': 'count',
        'Total Revenue': 'sum',
        'Monthly Recurring Revenue': 'sum',
        'Lifetime Value': 'sum'
    }).rename(columns={
        'Client Name': 'Unique Clients',
        'Lifetime Value': 'Annual Recurring Revenue'
    })
    
    consultant_metrics['Avg Revenue per Client'] = (
        consultant_metrics['Total Revenue'] / consultant_metrics['Unique Clients']
    ).round(0)
    
    st.dataframe(consultant_metrics, use_container_width=True)
    
    # Visualization
    fig = px.bar(consultant_metrics, x=consultant_metrics.index, 
                y=['Total Revenue', 'Monthly Recurring Revenue'],
                title="Consultant Revenue Comparison",
                barmode='group')
    st.plotly_chart(fig, use_container_width=True)

# Referral Sources
def referral_sources():
    st.title("🔗 Referral Source Analysis")
    
    # Editable table for admin users
    if st.session_state.user_role == 'admin':
        st.subheader("✏️ Edit Client Information")
        st.info("💡 Click on any cell to edit it directly. You can edit Referral Source, Status, Total Revenue, and Monthly Recurring Revenue. Changes are saved automatically.")
        
        # Create editable dataframe with all editable columns
        referral_edit_df = st.session_state.clients_df[['Client Name', 'Referral Source', 'Status', 'Total Revenue', 'Monthly Recurring Revenue']].copy()
        
        # Use data_editor for inline editing
        edited_df = st.data_editor(
            referral_edit_df,
            use_container_width=True,
            hide_index=True,
            disabled=['Client Name'],  # Only Client Name is read-only
            column_config={
                "Client Name": st.column_config.TextColumn("Client Name", width="medium"),
                "Referral Source": st.column_config.TextColumn("Referral Source", width="large"),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    width="small",
                    options=["Active", "Proposal", "Prospect", "Completed"],
                    required=True
                ),
                "Total Revenue": st.column_config.NumberColumn(
                    "Total Revenue",
                    format="$%d",
                    min_value=0,
                    step=1
                ),
                "Monthly Recurring Revenue": st.column_config.NumberColumn(
                    "Monthly Recurring Revenue (MRR)",
                    format="$%d",
                    min_value=0,
                    step=1
                )
            },
            key="referral_editor"
        )
        
        # Check if any changes were made
        if not edited_df.equals(referral_edit_df):
            # Update the main dataframe with all edited fields
            for idx, row in edited_df.iterrows():
                client_name = row['Client Name']
                st.session_state.clients_df.loc[
                    st.session_state.clients_df['Client Name'] == client_name,
                    'Referral Source'
                ] = row['Referral Source']
                st.session_state.clients_df.loc[
                    st.session_state.clients_df['Client Name'] == client_name,
                    'Status'
                ] = row['Status']
                st.session_state.clients_df.loc[
                    st.session_state.clients_df['Client Name'] == client_name,
                    'Total Revenue'
                ] = row['Total Revenue']
                st.session_state.clients_df.loc[
                    st.session_state.clients_df['Client Name'] == client_name,
                    'Monthly Recurring Revenue'
                ] = row['Monthly Recurring Revenue']
            
            st.success("✅ Client data updated successfully!")
        
        st.markdown("---")
    else:
        # Read-only view for non-admin users
        st.subheader("📋 Client Information")
        referral_display = st.session_state.clients_df[['Client Name', 'Referral Source', 'Status', 'Total Revenue', 'Monthly Recurring Revenue']].sort_values('Client Name')
        st.dataframe(referral_display, use_container_width=True, hide_index=True)
        st.markdown("---")
    
    # Referral performance metrics
    st.subheader("📊 Referral Performance Metrics")
    referral_metrics = st.session_state.clients_df.groupby('Referral Source').agg({
        'Client Name': 'count',
        'Total Revenue': 'sum',
        'Monthly Recurring Revenue': 'sum'
    }).rename(columns={'Client Name': 'Clients Referred'}).sort_values('Total Revenue', ascending=False)
    
    st.dataframe(referral_metrics, use_container_width=True)
    
    # Visualization
    fig = px.bar(referral_metrics, x=referral_metrics.index, y='Total Revenue',
                title="Total Revenue by Referral Source",
                labels={'x': 'Referral Source', 'y': 'Total Revenue ($)'})
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Issues and Opportunities
def issues_opportunities():
    st.title("⚠️ Critical Issues & Growth Opportunities")
    
    # Critical Issues
    st.subheader("🚨 Critical Issues & Risks")
    st.dataframe(st.session_state.issues_df, use_container_width=True, hide_index=True)
    
    # Add/Delete issues (admin only)
    if st.session_state.user_role == 'admin':
        with st.expander("➕ Add New Issue"):
            with st.form("add_issue_form"):
                issue = st.text_input("Issue")
                impact = st.text_area("Impact")
                recommendation = st.text_area("Recommendation")
                
                if st.form_submit_button("Add Issue"):
                    new_issue = pd.DataFrame({
                        'Issue': [issue],
                        'Impact': [impact],
                        'Recommendation': [recommendation]
                    })
                    st.session_state.issues_df = pd.concat([st.session_state.issues_df, new_issue], ignore_index=True)
                    st.success("Issue added successfully!")
                    st.rerun()
    
    st.markdown("---")
    
    # Growth Opportunities
    st.subheader("🎯 Growth Opportunities")
    st.dataframe(st.session_state.opportunities_df, use_container_width=True, hide_index=True)
    
    # Add/Delete opportunities (admin only)
    if st.session_state.user_role == 'admin':
        with st.expander("➕ Add New Opportunity"):
            with st.form("add_opportunity_form"):
                opportunity = st.text_input("Opportunity")
                potential_value = st.text_input("Potential Value")
                priority = st.selectbox("Priority", 
                                       ["HIGH - Largest single opportunity",
                                        "HIGH - Massive expansion potential",
                                        "CRITICAL - Stabilize revenue",
                                        "MEDIUM - Multiple services",
                                        "MEDIUM - Policy Review"])
                
                if st.form_submit_button("Add Opportunity"):
                    new_opp = pd.DataFrame({
                        'Opportunity': [opportunity],
                        'Potential Value': [potential_value],
                        'Priority': [priority]
                    })
                    st.session_state.opportunities_df = pd.concat([st.session_state.opportunities_df, new_opp], ignore_index=True)
                    st.success("Opportunity added successfully!")
                    st.rerun()

# Export function
def export_data():
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state.clients_df.to_excel(writer, sheet_name='Clients', index=False)
        st.session_state.services_df.to_excel(writer, sheet_name='Services', index=False)
        st.session_state.issues_df.to_excel(writer, sheet_name='Issues', index=False)
        st.session_state.opportunities_df.to_excel(writer, sheet_name='Opportunities', index=False)
    
    output.seek(0)
    st.download_button(
        label="📥 Download Excel Report",
        data=output,
        file_name=f"CRM_Dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Main app logic
def main():
    initialize_data()
    
    if not st.session_state.authenticated:
        login_page()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()