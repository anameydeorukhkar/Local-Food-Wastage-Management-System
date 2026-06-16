#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import sqlite3
from charts import create_charts

# ================= PAGE CONFIG =================

st.set_page_config(page_title="Local Food Wastage Management System",page_icon="🍱",layout="wide")

# ================= CSS =================

st.markdown("""
<style>

.main{
padding-top:1rem;
}

div.block-container{
padding-top:1rem;
padding-bottom:1rem;
}

div[data-testid="stMetric"]{
background:#111827;
border:1px solid #334155;
padding:20px;
border-radius:16px;
box-shadow:0 4px 10px rgba(0,0,0,0.2);
}

div[data-testid="stMetricLabel"]{
font-size:16px;
font-weight:600;
color:#cbd5e1;
}

div[data-testid="stMetricValue"]{
font-size:36px;
font-weight:700;
color:#ffffff;
}

div[data-testid="stMetricDelta"]{
display:none;
}

</style>
""",unsafe_allow_html=True)

# ================= LOAD DATA =================

@st.cache_data
def load_data():

    providers=pd.read_csv("providers_data.csv")
    receivers=pd.read_csv("receivers_data.csv")
    food=pd.read_csv("food_listings_data.csv")
    claims=pd.read_csv("claims_data.csv")

    return providers,receivers,food,claims

providers,receivers,food,claims=load_data()

# ================= SQLITE =================

conn=sqlite3.connect("food_waste.db",check_same_thread=False)

providers.to_sql("providers",conn,if_exists="replace",index=False)
receivers.to_sql("receivers",conn,if_exists="replace",index=False)
food.to_sql("food_listings",conn,if_exists="replace",index=False)
claims.to_sql("claims",conn,if_exists="replace",index=False)

# ================= KPI =================

total_providers=len(providers)
total_receivers=len(receivers)
total_food=len(food)
total_claims=len(claims)

completed=len(claims[claims["Status"]=="Completed"])
pending=len(claims[claims["Status"]=="Pending"])
cancelled=len(claims[claims["Status"]=="Cancelled"])

completion_rate=0 if total_claims==0 else round((completed/total_claims)*100,1)

# ================= CHARTS =================

charts=create_charts(providers,receivers,food,claims)

# ================= SIDEBAR =================

st.sidebar.title("Food Waste System")

page=st.sidebar.radio(
    "Navigation",
    ["Overview","Food Explorer","Analytics","Manage Listings","SQL Analysis"]
)

# ================= OVERVIEW =================

if page=="Overview":

    st.title("Local Food Wastage Management System")

    st.caption("Reduce Food Waste | Connect Communities")

    col1,col2,col3=st.columns(3)
    col4,col5,col6=st.columns(3)

    col1.metric("🏢 Providers",total_providers)
    col2.metric("🤝 Receivers",total_receivers)
    col3.metric("🍱 Food Listings",total_food)
    col4.metric("📋 Claims",total_claims)
    col5.metric("✅ Completed",completed)
    col6.metric("⏳ Pending",pending)

    st.divider()

    st.subheader("Project Objective")

    st.write("""
This platform connects food providers with receivers to reduce food wastage and improve food accessibility.
""")

    st.subheader("Key Insights")

    col1,col2=st.columns(2)

    with col1:

        st.success(f"Top Food City : {food['Location'].mode()[0]}")
        st.info(f"Most Common Meal : {food['Meal_Type'].mode()[0]}")

    with col2:

        st.warning(f"Top Provider : {food['Provider_Type'].mode()[0]}")
        st.error(f"Completion Rate : {completion_rate}%")

    st.subheader("📌 Recommendations")

    st.success(
    "Prioritize food redistribution in high-waste cities."
    )

    st.success(
    "Notify receivers about food nearing expiry."
    )

    st.success(
    "Focus on underutilized meal categories."
    )
# ================= FOOD EXPLORER =================

elif page=="Food Explorer":

    st.title("Food Explorer")

    col1,col2=st.columns(2)

    with col1:

        city=st.selectbox(
            "City",
            ["All"]+list(sorted(food["Location"].unique()))
        )

        food_type=st.selectbox(
            "Food Type",
            ["All"]+list(sorted(food["Food_Type"].unique()))
        )

    with col2:

        meal=st.selectbox(
            "Meal Type",
            ["All"]+list(sorted(food["Meal_Type"].unique()))
        )

        provider=st.selectbox(
            "Provider Type",
            ["All"]+list(sorted(food["Provider_Type"].unique()))
        )

    filtered=food.copy()

    if city!="All":
        filtered=filtered[filtered["Location"]==city]

    if food_type!="All":
        filtered=filtered[filtered["Food_Type"]==food_type]

    if meal!="All":
        filtered=filtered[filtered["Meal_Type"]==meal]

    if provider!="All":
        filtered=filtered[filtered["Provider_Type"]==provider]

    st.dataframe(
        filtered,
        use_container_width=True
    )

    st.subheader("📞 Provider Contact Information")

    provider_contacts=providers[
        ["Name","City","Contact"]
    ]

    st.dataframe(
        provider_contacts,
        use_container_width=True
    )

# ================= ANALYTICS =================

elif page=="Analytics":

    st.title("Analytics Dashboard")

    chart_pairs=[
        ("fig1","fig2"),
        ("fig3","fig4"),
        ("fig5","fig6"),
        ("fig7","fig8")
    ]

    for left,right in chart_pairs:

        col1,col2=st.columns(2)

        with col1:

            st.plotly_chart(
                charts[left],
                use_container_width=True
            )

        with col2:

            st.plotly_chart(
                charts[right],
                use_container_width=True
            )

# ================= SQL ANALYSIS =================

elif page=="SQL Analysis":

    st.title("SQL Analysis Dashboard")

    st.caption("Outputs of the SQL queries used for food wastage analysis")

    queries={

    "1️⃣ Food Providers per City":"""

    SELECT City,
    COUNT(*) AS Total_Providers

    FROM providers

    GROUP BY City

    ORDER BY Total_Providers DESC

    """,

    "2️⃣ Food Receivers per City":"""

    SELECT City,
    COUNT(*) AS Total_Receivers

    FROM receivers

    GROUP BY City

    ORDER BY Total_Receivers DESC

    """,

    "3️⃣ Provider Contribution":"""

    SELECT Provider_Type,
    SUM(Quantity) AS Total_Food_Donated

    FROM food_listings

    GROUP BY Provider_Type

    ORDER BY Total_Food_Donated DESC

    """,

    "4️⃣ Top Food Claimers":"""

    SELECT Receiver_ID,
    COUNT(*) AS Total_Claims

    FROM claims

    GROUP BY Receiver_ID

    ORDER BY Total_Claims DESC

    """,

    "5️⃣ Total Food Available":"""

    SELECT SUM(Quantity)
    AS Total_Food_Available

    FROM food_listings

    """,

    "6️⃣ Cities with Highest Listings":"""

    SELECT Location,
    COUNT(*) AS Total_Listings

    FROM food_listings

    GROUP BY Location

    ORDER BY Total_Listings DESC

    """,

    "7️⃣ Most Available Food Types":"""

    SELECT Food_Type,
    COUNT(*) AS Frequency

    FROM food_listings

    GROUP BY Food_Type

    ORDER BY Frequency DESC

    """,

    "8️⃣ Claims per Food Item":"""

    SELECT Food_ID,
    COUNT(*) AS Total_Claims

    FROM claims

    GROUP BY Food_ID

    ORDER BY Total_Claims DESC

    """,

    "9️⃣ Successful Providers":"""

    SELECT f.Provider_ID,
    COUNT(*) AS Successful_Claims

    FROM claims c

    JOIN food_listings f

    ON c.Food_ID=f.Food_ID

    WHERE c.Status='Completed'

    GROUP BY f.Provider_ID

    ORDER BY Successful_Claims DESC

    """,

    "🔟 Claim Status Percentage":"""

    SELECT Status,

    ROUND(

    COUNT(*)*100.0/

    (SELECT COUNT(*) FROM claims),

    2

    ) AS Percentage

    FROM claims

    GROUP BY Status

    """,

    "1️⃣1️⃣ Most Claimed Meal Types":"""

    SELECT f.Meal_Type,

    COUNT(*) AS Total_Claims

    FROM claims c

    JOIN food_listings f

    ON c.Food_ID=f.Food_ID

    GROUP BY f.Meal_Type

    ORDER BY Total_Claims DESC

    """,

    "1️⃣2️⃣ Provider Donation Quantity":"""

    SELECT Provider_ID,

    SUM(Quantity) AS Total_Donated

    FROM food_listings

    GROUP BY Provider_ID

    ORDER BY Total_Donated DESC

    """,

    "1️⃣3️⃣ Top 5 Receivers":"""

    SELECT Receiver_ID,

    COUNT(*) AS Total_Claims

    FROM claims

    GROUP BY Receiver_ID

    ORDER BY Total_Claims DESC

    LIMIT 5

    """,

    "1️⃣4️⃣ Food Near Expiry":"""

    SELECT *

    FROM food_listings

    WHERE

    julianday(Expiry_Date)

    -julianday('now')<=2

    AND

    julianday(Expiry_Date)

    >=julianday('now')

    """,

    "1️⃣5️⃣ Most Claimed Food Categories":"""

    SELECT f.Food_Type,

    COUNT(*) AS Total_Claims

    FROM claims c

    JOIN food_listings f

    ON c.Food_ID=f.Food_ID

    GROUP BY f.Food_Type

    ORDER BY Total_Claims DESC

    """,

    "1️⃣6️⃣ Highest Food Quantity by City":"""
    SELECT Location,

    SUM(Quantity) AS Total_Quantity

    FROM food_listings

    GROUP BY Location

    ORDER BY Total_Quantity DESC;
    """,

    "1️⃣7️⃣ Average Food Quantity per Listing":"""

    SELECT ROUND(
    AVG(Quantity),
    2
    ) AS Average_Quantity

    FROM food_listings;
    """,

    "1️⃣8️⃣ Top 10 Most Active Providers":"""

    SELECT Provider_ID,

    COUNT(*) AS Total_Listings

    FROM food_listings

    GROUP BY Provider_ID

    ORDER BY Total_Listings DESC

    LIMIT 10;
    """
    }

    for title,query in queries.items():

        with st.expander(title):

            result=pd.read_sql_query(

                query,

                conn

            )

            st.dataframe(

                result,

                use_container_width=True

            )
# ================= CRUD =================

elif page=="Manage Listings":

    st.title("Manage Listings")

    with st.expander("📄 View Current Listings"):

        st.dataframe(food,use_container_width=True)

    # ---------- ADD ----------

    with st.expander("➕ Add New Listing"):

        food_id=st.number_input("Food ID",step=1,key="food_id")

        food_name=st.text_input("Food Name")

        quantity=st.number_input("Quantity",step=1,key="quantity")

        expiry=st.text_input("Expiry Date (YYYY-MM-DD)")

        provider_id=st.number_input("Provider ID",step=1,key="provider_id")

        provider_type=st.text_input("Provider Type")

        location=st.text_input("Location")

        food_type=st.text_input("Food Type")

        meal_type=st.text_input("Meal Type")

        if st.button("Add Food"):

            cursor=conn.cursor()

            cursor.execute(
                """
                INSERT INTO food_listings
                VALUES (?,?,?,?,?,?,?,?,?)
                """,
                (
                    food_id,
                    food_name,
                    quantity,
                    expiry,
                    provider_id,
                    provider_type,
                    location,
                    food_type,
                    meal_type
                )
            )

            conn.commit()

            st.success("Food Added Successfully")

            st.rerun()

    # ---------- UPDATE ----------

    with st.expander("✏️ Update Existing Listing"):

        update_id=st.number_input(
            "Food ID to Update",
            step=1,
            key="update_id"
        )

        new_quantity=st.number_input(
            "New Quantity",
            step=1,
            key="new_quantity"
        )

        if st.button("Update Quantity"):

            cursor=conn.cursor()

            cursor.execute(
                """
                UPDATE food_listings
                SET Quantity=?
                WHERE Food_ID=?
                """,
                (
                    new_quantity,
                    update_id
                )
            )

            conn.commit()

            st.success("Updated Successfully")

            st.rerun()

    # ---------- DELETE ----------

    with st.expander("🗑 Delete Listing"):

        delete_id=st.number_input(
            "Food ID to Delete",
            step=1,
            key="delete_id"
        )

        if st.button("Delete Food"):

            cursor=conn.cursor()

            cursor.execute(
                """
                DELETE FROM food_listings
                WHERE Food_ID=?
                """,
                (delete_id,)
            )

            conn.commit()

            st.success("Deleted Successfully")

            st.rerun()

# ================= CLOSE =================

conn.close()



# In[ ]:




