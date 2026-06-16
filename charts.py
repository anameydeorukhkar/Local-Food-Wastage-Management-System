#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import plotly.express as px
import pandas as pd


def style_chart(fig):

    fig.update_layout(

        template="simple_white",

        title_x=0.05,

        title_font_size=18,

        font=dict(

            family="Arial",

            size=13

        ),

        height=420,

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        showlegend=True

    )

    return fig


def create_charts(providers,receivers,food,claims):

    charts={}

    # -------- Provider Cities --------

    provider_city=(

        providers["City"]

        .dropna()

        .value_counts()

        .head(10)

    )

    fig1=px.bar(

        x=provider_city.values,

        y=provider_city.index,

        orientation="h",

        title="Top Cities by Food Providers",

        labels={

            "x":"Providers",

            "y":"City"

        }

    )

    charts["fig1"]=style_chart(fig1)


    # -------- Receiver Cities --------

    receiver_city=(

        receivers["City"]

        .dropna()

        .value_counts()

        .head(10)

    )

    fig2=px.bar(

        x=receiver_city.values,

        y=receiver_city.index,

        orientation="h",

        title="Top Cities by Receivers",

        labels={

            "x":"Receivers",

            "y":"City"

        }

    )

    charts["fig2"]=style_chart(fig2)


    # -------- Food Type --------

    fig3=px.pie(

        food,

        names="Food_Type",

        hole=0.45,

        title="Food Type Distribution"

    )

    charts["fig3"]=style_chart(fig3)


    # -------- Meal Type --------

    fig4=px.pie(

        food,

        names="Meal_Type",

        hole=0.45,

        title="Meal Type Distribution"

    )

    charts["fig4"]=style_chart(fig4)


    # -------- Claim Status --------

    fig5=px.pie(

        claims,

        names="Status",

        hole=0.55,

        title="Claim Status Overview"

    )

    charts["fig5"]=style_chart(fig5)


    # -------- Provider Category --------

    provider_type=(

        food["Provider_Type"]

        .dropna()

        .value_counts()

    )

    fig6=px.bar(

        x=provider_type.values,

        y=provider_type.index,

        orientation="h",

        title="Provider Category Distribution",

        labels={

            "x":"Count",

            "y":"Provider Type"

        }

    )

    charts["fig6"]=style_chart(fig6)


    # -------- Food Availability --------

    food_city=(

        food["Location"]

        .dropna()

        .value_counts()

        .head(10)

    )

    fig7=px.bar(

        x=food_city.values,

        y=food_city.index,

        orientation="h",

        title="Top Cities by Food Availability",

        labels={

            "x":"Food Listings",

            "y":"City"

        }

    )

    charts["fig7"]=style_chart(fig7)


    # -------- Most Claimed Meals --------

    meal_claims=pd.merge(

        claims,

        food,

        on="Food_ID",

        how="inner"

    )

    if meal_claims.empty:

        fig8=px.bar(

            title="Most Claimed Meal Types"

        )

    else:

        meal_claims=(

            meal_claims["Meal_Type"]

            .value_counts()

            .reset_index()

        )

        meal_claims.columns=[

            "Meal_Type",

            "Total"

        ]

        fig8=px.bar(

            meal_claims,

            x="Total",

            y="Meal_Type",

            orientation="h",

            title="Most Claimed Meal Types"

        )

    charts["fig8"]=style_chart(fig8)

    return charts


