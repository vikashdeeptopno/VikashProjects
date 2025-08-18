
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Coffee Shop Analytics Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #8B4513;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #8B4513;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('index_1.csv')

    # Data preprocessing
    df['date'] = pd.to_datetime(df['date'])
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.day_name()
    df['month'] = df['datetime'].dt.month
    df['card'].fillna('CASH_TRANSACTION', inplace=True)

    return df

def main():
    # Load data
    df = load_data()

    # Header
    st.markdown('<h1 class="main-header">☕ Coffee Shop Analytics Dashboard</h1>', unsafe_allow_html=True)

    # Sidebar filters
    st.sidebar.header("Filters")

    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=[df['date'].min(), df['date'].max()],
        min_value=df['date'].min(),
        max_value=df['date'].max()
    )

    # Coffee type filter
    coffee_types = st.sidebar.multiselect(
        "Select Coffee Types",
        options=df['coffee_name'].unique(),
        default=df['coffee_name'].unique()
    )

    # Payment method filter
    payment_methods = st.sidebar.multiselect(
        "Select Payment Methods",
        options=df['cash_type'].unique(),
        default=df['cash_type'].unique()
    )

    # Filter data
    if len(date_range) == 2:
        filtered_df = df[
            (df['date'] >= pd.to_datetime(date_range[0])) &
            (df['date'] <= pd.to_datetime(date_range[1])) &
            (df['coffee_name'].isin(coffee_types)) &
            (df['cash_type'].isin(payment_methods))
        ]
    else:
        filtered_df = df[
            (df['coffee_name'].isin(coffee_types)) &
            (df['cash_type'].isin(payment_methods))
        ]

    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        total_revenue = filtered_df['money'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")

    with col2:
        total_transactions = len(filtered_df)
        st.metric("Total Transactions", f"{total_transactions:,}")

    with col3:
        avg_transaction = filtered_df['money'].mean()
        st.metric("Avg Transaction", f"${avg_transaction:.2f}")

    with col4:
        unique_customers = filtered_df['card'].nunique()
        st.metric("Unique Customers", f"{unique_customers:,}")

    with col5:
        unique_products = filtered_df['coffee_name'].nunique()
        st.metric("Product Variety", f"{unique_products}")

    st.markdown("---")

    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Sales Trends", "☕ Products", "👥 Customers", "💰 Revenue Analysis"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Daily revenue trend
            daily_revenue = filtered_df.groupby('date')['money'].sum().reset_index()
            fig = px.line(daily_revenue, x='date', y='money', 
                         title='Daily Revenue Trend',
                         labels={'money': 'Revenue ($)', 'date': 'Date'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Payment method distribution
            payment_dist = filtered_df['cash_type'].value_counts()
            fig = px.pie(values=payment_dist.values, names=payment_dist.index,
                        title='Payment Method Distribution')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            # Hourly sales pattern
            hourly_sales = filtered_df.groupby('hour')['money'].sum().reset_index()
            fig = px.bar(hourly_sales, x='hour', y='money',
                        title='Revenue by Hour of Day',
                        labels={'money': 'Revenue ($)', 'hour': 'Hour'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            # Day of week pattern
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_pattern = filtered_df.groupby('day_of_week')['money'].sum().reindex(day_order).reset_index()
            fig = px.bar(daily_pattern, x='day_of_week', y='money',
                        title='Revenue by Day of Week',
                        labels={'money': 'Revenue ($)', 'day_of_week': 'Day'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            # Transaction count over time
            daily_transactions = filtered_df.groupby('date').size().reset_index(name='transactions')
            fig = px.line(daily_transactions, x='date', y='transactions',
                         title='Daily Transaction Count',
                         labels={'transactions': 'Number of Transactions', 'date': 'Date'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Average transaction value over time
            daily_avg = filtered_df.groupby('date')['money'].mean().reset_index()
            fig = px.line(daily_avg, x='date', y='money',
                         title='Daily Average Transaction Value',
                         labels={'money': 'Avg Transaction ($)', 'date': 'Date'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Weekly performance
        st.subheader("Weekly Performance Analysis")
        weekly_data = filtered_df.groupby(filtered_df['date'].dt.to_period('W')).agg({
            'money': ['sum', 'count', 'mean']
        }).round(2)
        weekly_data.columns = ['Revenue', 'Transactions', 'Avg_Transaction']
        weekly_data.index = weekly_data.index.to_timestamp()

        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=['Weekly Revenue', 'Weekly Transactions', 'Weekly Avg Transaction'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
        )

        fig.add_trace(go.Scatter(x=weekly_data.index, y=weekly_data['Revenue'], mode='lines+markers', name='Revenue'), row=1, col=1)
        fig.add_trace(go.Scatter(x=weekly_data.index, y=weekly_data['Transactions'], mode='lines+markers', name='Transactions'), row=1, col=2)
        fig.add_trace(go.Scatter(x=weekly_data.index, y=weekly_data['Avg_Transaction'], mode='lines+markers', name='Avg Transaction'), row=1, col=3)

        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            # Top products by revenue
            product_revenue = filtered_df.groupby('coffee_name')['money'].sum().sort_values(ascending=False).head(10)
            fig = px.bar(x=product_revenue.values, y=product_revenue.index, orientation='h',
                        title='Top 10 Products by Revenue',
                        labels={'x': 'Revenue ($)', 'y': 'Coffee Type'})
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Top products by quantity
            product_quantity = filtered_df['coffee_name'].value_counts().head(10)
            fig = px.bar(x=product_quantity.values, y=product_quantity.index, orientation='h',
                        title='Top 10 Products by Quantity Sold',
                        labels={'x': 'Quantity Sold', 'y': 'Coffee Type'})
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        # Product performance table
        st.subheader("Product Performance Summary")
        product_summary = filtered_df.groupby('coffee_name').agg({
            'money': ['sum', 'count', 'mean'],
            'card': 'nunique'
        }).round(2)
        product_summary.columns = ['Total Revenue', 'Quantity Sold', 'Avg Price', 'Unique Customers']
        product_summary = product_summary.sort_values('Total Revenue', ascending=False)
        product_summary['Revenue Share %'] = (product_summary['Total Revenue'] / product_summary['Total Revenue'].sum() * 100).round(2)

        st.dataframe(product_summary, use_container_width=True)

    with tab4:
        # Customer analysis (card customers only)
        card_customers = filtered_df[filtered_df['cash_type'] == 'card']

        if not card_customers.empty:
            customer_stats = card_customers.groupby('card').agg({
                'money': ['sum', 'count', 'mean'],
                'coffee_name': 'nunique'
            }).round(2)
            customer_stats.columns = ['Total Spent', 'Visit Count', 'Avg Spending', 'Unique Products']

            col1, col2 = st.columns(2)

            with col1:
                # Customer spending distribution
                fig = px.histogram(customer_stats, x='Total Spent', nbins=20,
                                 title='Customer Spending Distribution',
                                 labels={'Total Spent': 'Total Spent ($)', 'count': 'Number of Customers'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Visit frequency distribution
                fig = px.histogram(customer_stats, x='Visit Count', nbins=20,
                                 title='Customer Visit Frequency',
                                 labels={'Visit Count': 'Number of Visits', 'count': 'Number of Customers'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            # Top customers
            st.subheader("Top 20 Customers by Spending")
            top_customers = customer_stats.nlargest(20, 'Total Spent')
            st.dataframe(top_customers, use_container_width=True)

            # Customer retention metrics
            repeat_customers = (customer_stats['Visit Count'] > 1).sum()
            total_customers = len(customer_stats)
            retention_rate = repeat_customers / total_customers * 100

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Repeat Customers", f"{repeat_customers}")
            with col2:
                st.metric("Retention Rate", f"{retention_rate:.1f}%")
            with col3:
                st.metric("Avg Customer Lifetime Value", f"${customer_stats['Total Spent'].mean():.2f}")
        else:
            st.warning("No card customer data available for the selected filters.")

    with tab5:
        col1, col2 = st.columns(2)

        with col1:
            # Revenue by payment method
            payment_revenue = filtered_df.groupby('cash_type')['money'].agg(['sum', 'count', 'mean']).round(2)
            payment_revenue.columns = ['Total Revenue', 'Transaction Count', 'Avg Transaction']

            fig = px.bar(payment_revenue, x=payment_revenue.index, y='Total Revenue',
                        title='Revenue by Payment Method',
                        labels={'Total Revenue': 'Revenue ($)', 'index': 'Payment Method'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Monthly revenue trend
            monthly_revenue = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['money'].sum().reset_index()
            monthly_revenue['date'] = monthly_revenue['date'].dt.to_timestamp()

            fig = px.line(monthly_revenue, x='date', y='money',
                         title='Monthly Revenue Trend',
                         labels={'money': 'Revenue ($)', 'date': 'Month'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Revenue breakdown table
        st.subheader("Revenue Analysis Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Payment Method Analysis**")
            payment_revenue['Revenue Share %'] = (payment_revenue['Total Revenue'] / payment_revenue['Total Revenue'].sum() * 100).round(2)
            st.dataframe(payment_revenue, use_container_width=True)

        with col2:
            st.write("**Time-based Revenue Analysis**")
            time_revenue = pd.DataFrame({
                'Period': ['Peak Hour Revenue', 'Best Day Revenue', 'Weekend Revenue', 'Weekday Revenue'],
                'Value': [
                    filtered_df[filtered_df['hour'] == filtered_df.groupby('hour')['money'].sum().idxmax()]['money'].sum(),
                    filtered_df[filtered_df['day_of_week'] == filtered_df.groupby('day_of_week')['money'].sum().idxmax()]['money'].sum(),
                    filtered_df[filtered_df['day_of_week'].isin(['Saturday', 'Sunday'])]['money'].sum(),
                    filtered_df[~filtered_df['day_of_week'].isin(['Saturday', 'Sunday'])]['money'].sum()
                ]
            })
            time_revenue['Value'] = time_revenue['Value'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(time_revenue, use_container_width=True, hide_index=True)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"  
        "Coffee Shop Analytics Dashboard | Built with ❤️ and ☕"  
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
