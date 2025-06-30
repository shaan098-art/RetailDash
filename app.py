# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load data
df = pd.read_excel("Retail_IA_PBL.csv.xlsx")
df['date'] = pd.to_datetime(df['date'])

# Sidebar filters
st.sidebar.header("Filter Data")
stores = st.sidebar.multiselect("Select Stores:", df['store_id'].unique(), default=df['store_id'].unique())
categories = st.sidebar.multiselect("Select Categories:", df['category'].unique(), default=df['category'].unique())
shelves = st.sidebar.multiselect("Select Shelf Levels:", df['shelf_level'].unique(), default=df['shelf_level'].unique())
date_range = st.sidebar.date_input("Select Date Range:", [df['date'].min(), df['date'].max()])

# Filter data
df_filtered = df[
    (df['store_id'].isin(stores)) &
    (df['category'].isin(categories)) &
    (df['shelf_level'].isin(shelves)) &
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1]))
]

# Title
st.title("Retail Sales & Shelf Analytics Dashboard")
st.markdown("This dashboard provides in-depth insights on units sold, revenue, pricing, promotions, and foot traffic across shelves and stores.")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", "Shelf Analysis", "Category Insights", "Time Series", "Promotion Impact", "Foot Traffic"
])

with tab1:
    # Overview tab content
    st.write("Content for Tab 1")

with tab2:
    # Shelf Analysis tab content
    st.write("Content for Tab 2")

with tab3:
    # Category Insights tab content
    st.write("Content for Tab 3")

with tab4:
    # Time Series tab content
    st.write("Content for Tab 4")

with tab5:
    # Promotion Impact tab content
    st.write("Content for Tab 5")

with tab6:
    # Foot Traffic tab content
    st.write("Content for Tab 6")

    # Overview
    with st.container():
        st.subheader("📊 Overall KPIs")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Units Sold", int(df_filtered['units_sold'].sum()))
        col2.metric("Total Revenue", f"${df_filtered['revenue'].sum():,.2f}")
        col3.metric("Average Price", f"${df_filtered['price'].mean():.2f}")

        st.write("### Units Sold by Shelf Level")
        st.write("This chart shows the total units sold from each shelf level to identify which placement performs best.")
        fig1 = px.bar(df_filtered.groupby('shelf_level')['units_sold'].sum().reset_index(),
                     x='shelf_level', y='units_sold', color='shelf_level', title='Units Sold by Shelf Level')
        st.plotly_chart(fig1, use_container_width=True)

        st.write("### Revenue by Store")
        st.write("Compare store-wise revenue performance to identify high and low performers.")
        fig2 = px.bar(df_filtered.groupby('store_id')['revenue'].sum().reset_index(),
                     x='store_id', y='revenue', title='Revenue by Store', color='store_id')
        st.plotly_chart(fig2, use_container_width=True)

    # Shelf Analysis
    st.subheader("🪜 Shelf Level Breakdown")
    st.write("Understand the sales distribution across different shelf levels.")
    fig3 = px.box(df_filtered, x='shelf_level', y='units_sold', color='shelf_level', title='Distribution of Units Sold by Shelf')
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.scatter(df_filtered, x='price', y='units_sold', color='shelf_level', title='Price vs Units Sold by Shelf')
    st.write("This scatter plot reveals the price sensitivity across shelf placements.")
    st.plotly_chart(fig4, use_container_width=True)

    # Category Insights
    st.subheader("🛍️ Category Performance")
    st.write("Total units sold per category.")
    fig5 = px.bar(df_filtered.groupby('category')['units_sold'].sum().reset_index(), x='category', y='units_sold',
                  title='Units Sold per Category', color='category')
    st.plotly_chart(fig5, use_container_width=True)

    st.write("Category-wise revenue performance.")
    fig6 = px.pie(df_filtered, values='revenue', names='category', title='Revenue Share by Category')
    st.plotly_chart(fig6, use_container_width=True)

    # Time Series
    st.subheader("📅 Time Trends")
    st.write("Observe daily units sold and revenue trends.")
    time_df = df_filtered.groupby('date')[['units_sold', 'revenue']].sum().reset_index()
    fig7 = px.line(time_df, x='date', y='units_sold', title='Daily Units Sold Trend')
    st.plotly_chart(fig7, use_container_width=True)

    fig8 = px.line(time_df, x='date', y='revenue', title='Daily Revenue Trend', color_discrete_sequence=['orange'])
    st.plotly_chart(fig8, use_container_width=True)

    # Promotion Impact
    st.subheader("🏷️ Promotions & Sales")
    st.write("Compare average units sold with and without promotions.")
    promo_df = df_filtered.groupby('promotion')['units_sold'].mean().reset_index()
    promo_df['promotion'] = promo_df['promotion'].map({0: 'No Promo', 1: 'Promo'})
    fig9 = px.bar(promo_df, x='promotion', y='units_sold', color='promotion', title='Average Units Sold by Promotion')
    st.plotly_chart(fig9, use_container_width=True)

    # Foot Traffic
    st.subheader("🚶 Foot Traffic Impact")
    st.write("Relationship between store traffic and units sold.")
    fig10 = px.scatter(df_filtered, x='foot_traffic', y='units_sold', color='store_id',
                       trendline='ols', title='Foot Traffic vs Units Sold')
    st.plotly_chart(fig10, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Created by Data Science Team | For Retail Org Directors & Stakeholders")
