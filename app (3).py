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
.main{padding-top:1rem;}
div.block-container{padding-top:1rem;padding-bottom:1rem;}
.stMetric{background:#fff;padding:18px;border-radius:12px;box-shadow:0px 2px 8px rgba(0,0,0,0.05);}
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

st.sidebar.title("🍱 Food Waste System")

page=st.sidebar.radio(
    "Navigation",
    ["🏠 Overview","🍱 Food Explorer","📊 Analytics","✏️ Manage Listings"]
)

# ================= OVERVIEW =================

if page=="🏠 Overview":

    st.title("🍱 Local Food Wastage Management System")

    st.caption("Reduce Food Waste | Connect Communities")

    col1,col2,col3=st.columns(3)
    col4,col5,col6=st.columns(3)

    col1.metric("Providers",total_providers)
    col2.metric("Receivers",total_receivers)
    col3.metric("Food Listings",total_food)

    col4.metric("Claims",total_claims)
    col5.metric("Completed",completed)
    col6.metric("Pending",pending)

    st.divider()

    st.subheader("🎯 Project Objective")

    st.write("""
This platform connects food providers with receivers to reduce food wastage and improve food accessibility.
""")

    st.subheader("💡 Key Insights")

    col1,col2=st.columns(2)

    with col1:

        st.info(f"🏆 Top Food City : {food['Location'].mode()[0]}")

        st.info(f"🍽 Most Common Meal : {food['Meal_Type'].mode()[0]}")

    with col2:

        st.info(f"🏢 Top Provider : {food['Provider_Type'].mode()[0]}")

        st.info(f"📈 Completion Rate : {completion_rate}%")

# ================= FOOD EXPLORER =================

elif page=="🍱 Food Explorer":

    st.title("🍱 Food Explorer")

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

    st.dataframe(filtered,use_container_width=True)

# ================= ANALYTICS =================

elif page=="📊 Analytics":

    st.title("📊 Analytics Dashboard")

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

# ================= CRUD =================

elif page=="✏️ Manage Listings":

    st.title("✏️ Manage Listings")

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




