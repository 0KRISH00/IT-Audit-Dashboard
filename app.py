import streamlit as st
import pandas as pd
import numpy as np
if not hasattr(np, 'bool8'):
    np.bool8 = np.bool_
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Config ---
st.set_page_config(
    page_title="Durairam Mobiles - Audit Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Dark Theme ---
def apply_custom_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap');
            
            /* Main Application Area */
            .stApp {
                background-color: #030712;
                color: #e2e8f0;
                font-family: 'Inter', sans-serif;
            }
            .stApp > header {
                background-color: transparent !important;
            }
            
            /* Typography */
            h1, h2, h3, h4 {
                color: #00f0ff !important;
                font-family: 'JetBrains Mono', monospace !important;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                text-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
                margin-bottom: 1rem !important;
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #080f1a;
                border-right: 1px solid #1e293b;
                box-shadow: 2px 0 15px rgba(0, 0, 0, 0.5);
            }
            
            /* KPI Metric Cards overrides */
            div[data-testid="metric-container"] {
                height: 145px;
                position: relative;
                background: linear-gradient(145deg, #0f172a, #1e293b);
                border: 1px solid #334155;
                border-left: 4px solid #00f0ff;
                padding: 24px 20px;
                border-radius: 10px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
                transition: transform 0.3s ease, box-shadow 0.3s ease, border-left-color 0.3s ease;
            }
            div[data-testid="metric-container"]:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(0, 240, 255, 0.2);
                border-left-color: #ff003c;
            }
            div[data-testid="metric-container"] > label {
                color: #94a3b8 !important;
                font-size: 0.9rem !important;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-family: 'JetBrains Mono', monospace;
                margin-bottom: 8px;
            }
            div[data-testid="metric-container"] > div {
                color: #ffffff !important;
                font-size: 2.2rem !important;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
            }
            
            /* Fix truncated metric deltas with hover dropdown */
            div[data-testid="stMetricDelta"] > div {
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
                max-width: 100%;
                cursor: help;
            }
            div[data-testid="stMetricDelta"] > div:hover {
                white-space: normal !important;
                overflow: visible !important;
                position: absolute;
                top: 75%;
                left: 10%;
                background: linear-gradient(145deg, #080f1a, #0f172a);
                border: 1px solid #38bdf8;
                padding: 10px 15px;
                border-radius: 8px;
                z-index: 1000;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
                width: max-content;
                max-width: 250px;
            }
            
            /* Badges */
            .badge-high { background-color: rgba(255, 0, 60, 0.15); color: #ff003c; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; border: 1px solid rgba(255,0,60,0.5); text-transform: uppercase; box-shadow: 0 0 10px rgba(255,0,60,0.2);}
            .badge-medium { background-color: rgba(252, 226, 5, 0.15); color: #fce205; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; border: 1px solid rgba(252,226,5,0.5); text-transform: uppercase; box-shadow: 0 0 10px rgba(252,226,5,0.2);}
            .badge-low { background-color: rgba(0, 240, 255, 0.15); color: #00f0ff; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; border: 1px solid rgba(0,240,255,0.5); text-transform: uppercase; box-shadow: 0 0 10px rgba(0,240,255,0.2);}
            .badge-pass { background-color: rgba(0, 255, 136, 0.15); color: #00ff88; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; border: 1px solid rgba(0,255,136,0.5); text-transform: uppercase; box-shadow: 0 0 10px rgba(0,255,136,0.2);}
            .badge-fail { background-color: rgba(255, 0, 60, 0.15); color: #ff003c; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; border: 1px solid rgba(255,0,60,0.5); text-transform: uppercase; box-shadow: 0 0 10px rgba(255,0,60,0.2);}
            .badge-partial { background-color: rgba(252, 226, 5, 0.15); color: #fce205; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; border: 1px solid rgba(252,226,5,0.5); text-transform: uppercase; box-shadow: 0 0 10px rgba(252,226,5,0.2);}
            
            /* Custom Table Styles */
            .custom-table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                background-color: #0b1320;
                border-radius: 10px;
                border: 1px solid #1e293b;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                margin-top: 1rem;
                margin-bottom: 2rem;
            }
            .custom-table th {
                background-color: #080f1a;
                color: #00f0ff;
                font-family: 'JetBrains Mono', monospace;
                text-transform: uppercase;
                font-size: 0.8rem;
                padding: 16px 20px;
                text-align: left;
                border-bottom: 2px solid #1e293b;
                letter-spacing: 1px;
            }
            .custom-table td {
                padding: 16px 20px;
                color: #cbd5e1;
                border-bottom: 1px solid #1e293b;
                font-size: 0.95rem;
                vertical-align: middle;
            }
            .custom-table tbody tr {
                transition: background-color 0.2s ease;
            }
            .custom-table tbody tr:hover {
                background-color: rgba(0, 240, 255, 0.05);
            }
            .custom-table tbody tr:last-child td {
                border-bottom: none;
            }
            
            /* Horizontal Rules / Section Separators */
            hr {
                border: 0;
                height: 1px;
                background-image: linear-gradient(to right, rgba(0, 240, 255, 0), rgba(0, 240, 255, 0.5), rgba(0, 240, 255, 0));
                margin: 3rem 0;
            }
            
            /* Expanders */
            .streamlit-expanderHeader {
                color: #00f0ff !important;
                background-color: #0f172a !important;
                font-family: 'JetBrains Mono', monospace;
                border-radius: 8px !important;
                border: 1px solid #1e293b !important;
            }
            
            /* Footer */
            .footer {
                margin-top: 60px;
                padding: 15px 0;
                text-align: center;
                font-size: 0.85rem;
                color: #64748b;
                border-top: 1px solid #1e293b;
                background-color: #030712;
            }
            
            /* Markdown Info boxes */
            .stAlert {
                background-color: rgba(15, 23, 42, 0.8) !important;
                border: 1px solid #334155 !important;
                border-radius: 8px !important;
            }
        </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# --- Data Loading ---
@st.cache(allow_output_mutation=True)
def load_data(filename):
    filepath = os.path.join("data", filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        st.warning(f"⚠️ Warning: '{filename}' not found in 'data/' folder. Please ensure the file exists.")
        return pd.DataFrame()

df_assets = load_data("assets_inventory.csv")
df_vulns = load_data("vulnerabilities.csv")
df_access = load_data("access_control.csv")
df_compliance = load_data("compliance_checklist.csv")
df_summary = load_data("audit_summary.csv")

# --- Helper Functions ---
def get_badge(status, badge_type):
    return f"<span class='badge-{badge_type}'>{status}</span>"

def render_html_table(df, col_badges=None):
    if df.empty:
        return "<p>No data available</p>"
    
    html = "<table class='custom-table'>"
    html += "<thead><tr>"
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            if col_badges and col in col_badges:
                val = str(val)
                badge_type = 'low'
                if val.lower() in ['high', 'critical', 'fail']: badge_type = 'high'
                elif val.lower() in ['medium', 'partial']: badge_type = 'medium'
                elif val.lower() in ['low', 'pass', 'up_to_date']: badge_type = 'pass'
                html += f"<td>{get_badge(val, badge_type)}</td>"
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

# --- Sidebar ---
st.sidebar.image("https://img.icons8.com/nolan/96/shield.png", width=60)
st.sidebar.title("Durairam Mobiles")
st.sidebar.caption("IT Infrastructure & Compliance Audit")
st.sidebar.markdown("---")

sections = [
    "Overview", 
    "Assets", 
    "Vulnerabilities", 
    "Access Control", 
    "Compliance", 
    "Risk Insights", 
    "Audit Report Summary"
]
selected_section = st.sidebar.radio("Navigation", sections)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters")

# Apply filters if data exists
filtered_assets = df_assets.copy() if not df_assets.empty else pd.DataFrame()
filtered_vulns = df_vulns.copy() if not df_vulns.empty else pd.DataFrame()

if not df_assets.empty:
    criticality_filter = st.sidebar.multiselect("Asset Criticality", df_assets['Criticality'].unique(), default=list(df_assets['Criticality'].unique()))
    patch_filter = st.sidebar.multiselect("Patch Status", df_assets['Patch_Status'].unique(), default=list(df_assets['Patch_Status'].unique()))
    filtered_assets = df_assets[(df_assets['Criticality'].isin(criticality_filter)) & (df_assets['Patch_Status'].isin(patch_filter))]

if not df_vulns.empty:
    severity_filter = st.sidebar.multiselect("Vulnerability Severity", df_vulns['Severity'].unique(), default=list(df_vulns['Severity'].unique()))
    filtered_vulns = filtered_vulns[filtered_vulns['Severity'].isin(severity_filter)]

if not df_compliance.empty:
    compliance_filter = st.sidebar.multiselect("Compliance Status", df_compliance['Status'].unique(), default=list(df_compliance['Status'].unique()))

# --- Main Content Area ---
st.title("Durairam Mobiles - IT Infrastructure & Compliance Audit Dashboard")
st.markdown("A comprehensive review of asset inventory, vulnerabilities, access controls, and compliance posture.")

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)
total_assets = len(filtered_assets) if not filtered_assets.empty else 0
crit_vulns = len(filtered_vulns[(filtered_vulns['Severity'] == 'Critical') & (filtered_vulns['Status'] == 'Open')]) if not filtered_vulns.empty else 0
comp_score = df_summary[df_summary['Metric'] == 'Overall Compliance Score']['Value'].values[0] if (not df_summary.empty and 'Overall Compliance Score' in df_summary['Metric'].values) else "N/A"
mfa_adopt = "N/A"
if not df_access.empty:
    mfa_yes = len(df_access[df_access['MFA_Enabled'] == 'Yes'])
    mfa_adopt = f"{int(mfa_yes / len(df_access) * 100)}%" if len(df_access) > 0 else "N/A"
overall_risk = df_summary[df_summary['Metric'] == 'Risk Rating']['Value'].values[0] if (not df_summary.empty and 'Risk Rating' in df_summary['Metric'].values) else "High"

col1.metric("Total Assets", total_assets)
col2.metric("Critical Vulns (Open)", crit_vulns, delta="-2 since last audit", delta_color="inverse")
col3.metric("Compliance Score", comp_score)
col4.metric("MFA Adoption", mfa_adopt, delta="Needs Improvement", delta_color="off")
col5.metric("Overall Risk", overall_risk)
st.markdown("<br>", unsafe_allow_html=True)

# --- Section Rendering ---

if selected_section == "Overview":
    st.header("Executive Overview")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Vulnerability Severity Distribution")
        if not filtered_vulns.empty:
            fig_pie = px.pie(filtered_vulns, names='Severity', hole=0.4, 
                             color='Severity',
                             color_discrete_map={'Critical':'#ef4444', 'High':'#f97316', 'Medium':'#eab308', 'Low':'#3b82f6'})
            fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'))
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No vulnerability data available.")
            
    with c2:
        st.subheader("Assets by Criticality")
        if not filtered_assets.empty:
            bar_df = pd.DataFrame(filtered_assets.groupby('Criticality').size().reset_index(name='Count').to_dict('records'))
            fig_bar = go.Figure()
            comp_map = {'High':'#ef4444', 'Medium':'#f97316', 'Low':'#3b82f6'}
            for lvl in comp_map:
                d = bar_df[bar_df['Criticality'] == lvl]
                if not d.empty:
                    fig_bar.add_trace(go.Bar(name=lvl, x=d['Criticality'], y=d['Count'], marker_color=comp_map[lvl]))
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'))
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No asset data available.")
            
    st.subheader("Simulated Vulnerability Trend")
    # Simulated trend data
    trend_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
        'Open Vulnerabilities': [8, 12, 10, 15, 22, 18, 14, 25, 20, len(filtered_vulns[filtered_vulns['Status'] == 'Open']) if not filtered_vulns.empty else 0]
    })
    fig_line = px.line(trend_data, x='Month', y='Open Vulnerabilities', markers=True, line_shape='spline')
    fig_line.update_traces(line_color='#38bdf8', line_width=3)
    fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'))
    st.plotly_chart(fig_line, use_container_width=True)


elif selected_section == "Assets":
    st.header("Asset Inventory")
    
    if not filtered_assets.empty:
        c1, c2 = st.columns(2)
        outdated_count = len(filtered_assets[filtered_assets['Patch_Status'].str.lower() == 'outdated'])
        high_crit_count = len(filtered_assets[filtered_assets['Criticality'].str.lower() == 'high'])
        c1.info(f"💾 **Outdated Assets:** {outdated_count} devices require patching.")
        c2.error(f"⚠️ **High Criticality Assets:** {high_crit_count} vital devices.")
        
        st.markdown(render_html_table(filtered_assets, col_badges=['Patch_Status', 'Criticality']), unsafe_allow_html=True)
    else:
        st.info("No asset data matching criteria.")


elif selected_section == "Vulnerabilities":
    st.header("Vulnerability Management")
    if not filtered_vulns.empty:
        open_vulns = filtered_vulns[filtered_vulns['Status'] == 'Open']
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("All Vulnerabilities")
            st.markdown(render_html_table(filtered_vulns, col_badges=['Severity', 'Status']), unsafe_allow_html=True)
            
        with c2:
            st.subheader("Priority Remediation Targets")
            critical_open = open_vulns[open_vulns['Severity'] == 'Critical']
            if not critical_open.empty:
                for _, v in critical_open.iterrows():
                    st.error(f"**{v['CVE']}** on {v['Asset_ID']} (Score: {v['Risk_Score']})")
            else:
                st.success("No open critical vulnerabilities!")
                
        st.subheader("Risk Score by Asset")
        vuln_df = pd.DataFrame(open_vulns.to_dict('records'))
        fig_scatter = go.Figure()
        sev_map = {'Critical':'#ef4444', 'High':'#f97316', 'Medium':'#eab308', 'Low':'#3b82f6'}
        for sev in sev_map:
            d = vuln_df[vuln_df['Severity'] == sev]
            if not d.empty:
                fig_scatter.add_trace(go.Scatter(name=sev, x=d['Asset_ID'], y=d['Risk_Score'], mode='markers', 
                                                 marker=dict(color=sev_map[sev], size=d['Risk_Score'].astype(float)*4)))
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'))
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("No vulnerability data available.")


elif selected_section == "Access Control":
    st.header("Identity & Access Management")
    if not df_access.empty:
        mfa_missing = df_access[df_access['MFA_Enabled'] == 'No']
        high_priv_no_mfa = mfa_missing[mfa_missing['Privilege_Level'] == 'High']
        
        if not high_priv_no_mfa.empty:
            st.error(f"🚨 **CRITICAL RISK:** {len(high_priv_no_mfa)} high-privilege users isolated without MFA enabled!")
            st.markdown(render_html_table(high_priv_no_mfa, col_badges=['MFA_Enabled', 'Privilege_Level']), unsafe_allow_html=True)
            
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Access Control List")
            st.markdown(render_html_table(df_access, col_badges=['MFA_Enabled', 'Privilege_Level']), unsafe_allow_html=True)
        with c2:
            st.subheader("Privilege Distribution")
            fig_role = px.pie(df_access, names='Privilege_Level', hole=0.5,
                              color_discrete_sequence=['#ef4444', '#f97316', '#3b82f6'])
            fig_role.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'))
            st.plotly_chart(fig_role, use_container_width=True)
    else:
        st.info("No access control data available.")


elif selected_section == "Compliance":
    st.header("Compliance Checklist & Status")
    if not df_compliance.empty:
        filtered_comp = df_compliance[df_compliance['Status'].isin(compliance_filter)]
        
        c1, c2 = st.columns([1, 2])
        with c1:
            status_counts = df_compliance['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig_comp = px.pie(status_counts, names='Status', values='Count', hole=0.6,
                              color='Status', color_discrete_map={'Pass':'#10b981', 'Fail':'#ef4444', 'Partial':'#f59e0b'})
            fig_comp.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'), margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_comp, use_container_width=True)
        
        with c2:
            st.subheader("Top Compliance Gaps")
            fails = df_compliance[df_compliance['Status'] == 'Fail']
            for _, row in fails.iterrows():
                st.warning(f"❌ **{row['Control_ID']} - {row['Control_Name']}**: {row['Remarks']}")
                
        st.markdown(render_html_table(filtered_comp, col_badges=['Status']), unsafe_allow_html=True)
    else:
        st.info("No compliance data available.")


elif selected_section == "Risk Insights":
    st.header("💡 AI-Driven Risk Insights")
    st.markdown("Automated observations based on the current data posture.")
    
    # Generate insights dynamically
    insights = []
    
    if not df_vulns.empty:
        crit_count = len(df_vulns[(df_vulns['Severity'] == 'Critical') & (df_vulns['Status'] == 'Open')])
        if crit_count > 0:
            insights.append(("error", f"Found {crit_count} Critical vulnerabilities that require immediate patching to prevent potential breaches."))
            
    if not df_access.empty:
        no_mfa = len(df_access[df_access['MFA_Enabled'] == 'No'])
        if no_mfa > 0:
            insights.append(("warning", f"Low MFA adoption identified. {no_mfa} users are currently operating without Multi-Factor Authentication."))
            
    if not df_assets.empty:
        outdated = df_assets[df_assets['Patch_Status'] == 'Outdated']
        network_outdated = outdated[outdated['Type'].isin(['Router', 'Switch', 'Firewall'])]
        if not network_outdated.empty:
            insights.append(("error", f"Critical risk identified: {len(network_outdated)} core network devices (Routers/Switches) are outdated."))
            
    if not df_compliance.empty:
        fails = len(df_compliance[df_compliance['Status'] == 'Fail'])
        if fails > 0:
            insights.append(("warning", f"{fails} compliance controls have failed, significantly affecting audit readiness and regulatory alignment."))

    for t, msg in insights:
        if t == "error":
            st.error(msg)
        else:
            st.warning(msg)
            
    if not insights:
        st.success("✅ No immediate high risks identified. Environment looks stable.")
        
    st.write("---")
    st.subheader("Risk Heatmap (Asset Volatility)")
    if not df_vulns.empty and not df_assets.empty:
        # Merge for heatmap
        heat_df = pd.merge(df_vulns, df_assets[['Asset_ID', 'Criticality']], on='Asset_ID', how='inner')
        if not heat_df.empty:
            severity_order = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
            heat_df['Sev_Num'] = heat_df['Severity'].map(severity_order)
            heatmap_data = heat_df.pivot_table(index='Asset_ID', columns='Criticality', values='Sev_Num', aggfunc='max').fillna(0)
            
            fig_heat = go.Figure(data=go.Heatmap(
                    z=heatmap_data.values,
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    colorscale='Reds'
                ))
            fig_heat.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'),
                xaxis_title="Asset Criticality", yaxis_title="Asset ID"
            )
            st.plotly_chart(fig_heat, use_container_width=True)
            


elif selected_section == "Audit Report Summary":
    st.header("Final Audit Report Summary")
    
    st.markdown("""
    ### 1. Scope & Methodology
    This audit encompasses the IT infrastructure for **Durairam Mobiles**, focusing on internal network devices, endpoint systems, and access control mechanisms. The methodology aligns with industry standard frameworks (NIST CSF, CIS Controls) assessing vulnerabilities, identity management, and overall compliance.
    """)
    
    st.markdown("### 2. Key Metrics Overview")
    if not df_summary.empty:
        for _, row in df_summary.iterrows():
            st.markdown(f"- **{row['Metric']}**: {row['Value']}")
            
    st.markdown("### 3. Executive Findings")
    st.warning("The environment currently operates at a **High Risk** level due to unpatched critical systems and missing MFA enforcement on highly privileged accounts.")
    
    st.markdown("### 4. Strategic Recommendations")
    with st.expander("Expand Recommendations", expanded=True):
        st.markdown("""
        - 🔐 **Enable MFA immediately** for all Database Admins and System Administrators.
        - 🛠 **Patch Management:** Prioritize patching for outdated Server and Router operating systems (e.g., AST-001, AST-008).
        - 🛡 **Access Control Readjustment:** Restrict generic sales accounts and enforce strict password policies on POS machines.
        - 💾 **Firmware Update:** Ensure that edge devices (Cameras, Routers) receive periodic firmware upgrades.
        - 🎓 **Cyber Awareness:** Push the pending 25% of staff to complete their mandatory security training.
        """)

# --- Footer ---
st.markdown("<div class='footer'>Simulated audit project for academic and portfolio demonstration | Durairam Mobiles SecOps</div>", unsafe_allow_html=True)
