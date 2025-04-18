import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import emoji
from streamlit_option_menu import option_menu

# --- Database connection ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="capstone_tennis"
    )

def load_table(table_name):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- Page setup ---
st.set_page_config(page_title="Tennis Data Explorer", layout="wide")

# --- Sidebar navigation ---
with st.sidebar:
    selected = option_menu(
        menu_title="Tennis App Navigation",
        options=["Home", "Dashboard", "Table Explorer", "Custom Query"],
        icons=["house", "bar-chart", "table", "cloud-upload", "terminal"],
        menu_icon="cast",
        default_index=0,
    )

# --- Page: Home ---
if selected == "Home":
    st.markdown("<h1 style='text-align: center;'>🎾 Welcome to the Tennis Data Explorer!</h1>", unsafe_allow_html=True)
    st.image("images/tennistour.jpg",  use_container_width=True)
    #st.image("images/tennistour.jpg", width=400)  # You can adjust 400 to whatever size you want

    # st.markdown(
    # """
    # <div style="text-align: center;">
    #     <img src="images/tennistour.jpg" width="400">
    # </div>
    # """,
    # unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'> Slide through the sidebar to cruise around the app.</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'> Deep dive into tennis stats</h4>", unsafe_allow_html=True)
   
    # text_with_emoji = emoji.emojize("Deep dive into tennis stats :fire:", language='alias')
    # st.markdown("<h4 style='text-align: center;'> {text_with_emoji} </h4>", unsafe_allow_html=True)

    #st.write(text_with_emoji)
    #st.write("### Deep dive into tennis stats straight from your MySQL plug.")
    #st.write(""" Use the sidebar to navigate through the app.""")

# --- Page: Dashboard ---
elif selected == "Dashboard":
    st.title("📊 Tennis Analytics Dashboard")
    
    df_rank = load_table("ranking")
    df_players = load_table("competitorsdetails")
    
    merged = df_rank.merge(df_players, on="competitor_id")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Players by Points")
        top = merged.sort_values(by="points", ascending=False).head(10)
        fig = px.bar(top, x="name", y="points", color="country")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Player Distribution by Country")
        dist = merged["country"].value_counts().reset_index()
        dist.columns = ["country", "count"]
        fig2 = px.pie(dist, values="count", names="country")
        st.plotly_chart(fig2, use_container_width=True)

# --- Page: Table Explorer ---
elif selected == "Table Explorer":
    st.title("📁 Explore Tables")
    tables = ["categories", "competitions", "competitorsdetails", "complexes", "ranking", "venue"]
    selected_table = st.selectbox("Choose a table to explore:", tables)
    df = load_table(selected_table)
    st.dataframe(df, use_container_width=True)

# --- Page: Upload Data ---
# elif selected == "Upload Data":
#     st.title("📂 Upload CSV to Table")

#     uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
#     if uploaded_file:
#         df_upload = pd.read_csv(uploaded_file)
#         st.write("Preview:")
#         st.dataframe(df_upload)

#         selected_table = st.selectbox("Select target table", ["categories", "competitions", "competitorsdetails", "complexes", "ranking", "venue"])

#         if st.button("Upload to Database"):
#             conn = get_connection()
#             cursor = conn.cursor()
#             for _, row in df_upload.iterrows():
#                 columns = ", ".join(row.index)
#                 placeholders = ", ".join(["%s"] * len(row))
#                 sql = f"INSERT INTO {selected_table} ({columns}) VALUES ({placeholders})"
#                 cursor.execute(sql, tuple(row))
#             conn.commit()
#             conn.close()
#             st.success("Data uploaded successfully!")

# --- Page: Custom Query ---
elif selected == "Custom Query":
    st.title("🧮 Kick Off Your Own SQL Search")

    query = st.text_area("Enter your SQL query:")
    if st.button("Run Query"):
        try:
            df_query = run_query(query)
            st.dataframe(df_query)
        except Exception as e:
            st.error(f"Error: {e}")
