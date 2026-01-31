import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def create_byseason(df):
    byseason = df.groupby('season')['count_customer'].sum().reset_index()
    return byseason

def create_monthlybike(df):
    bymonthly = df.groupby('month')['count_customer'].sum().reset_index()
    return bymonthly

def format_number(num):
    if num >= 1_000_000:
        return f'{num / 1_000_000:.2f} M'
    elif num >= 1_000:
        return f'{num / 1_000:.2f} K'
    else:
        return str(num)

bike_df = pd.read_csv(r'C:\Users\wawan\Dev\submission_dicoding\dashboard\rent_bike.csv', encoding='utf-8')

byseason_df = create_byseason(bike_df)
total_customer = byseason_df['count_customer'].sum()

st.header('Bike Rental Dashboard at Dicobike')

st.sidebar.title('Filter Dashboard')                 
season_choice = st.sidebar.multiselect(
    'Season',
    options=bike_df['season'].unique(),
    default=bike_df['season'].unique()
)

year_options = ['All'] + sorted(bike_df['year'].unique().tolist())
select_year = st.sidebar.selectbox('Year', year_options)

holiday_options = ['All'] + sorted(bike_df['holiday'].unique().tolist())
select_holiday = st.sidebar.selectbox('Holiday', holiday_options)

if select_year == 'All' and select_holiday == 'All':
    df_filtered = bike_df[bike_df['season'].isin(season_choice)]
elif select_year == 'All' and select_holiday == select_holiday:
    df_filtered = bike_df[(bike_df['season'].isin(season_choice)) & (bike_df['holiday'] == select_holiday)]
elif select_year == select_year and select_holiday == 'All':
    df_filtered = bike_df[(bike_df['season'].isin(season_choice)) & (bike_df['year'] == select_year)]
else:
    df_filtered = bike_df[(bike_df['season'].isin(season_choice)) & (bike_df['year'] == select_year) & (bike_df['holiday'] == select_holiday)]

if not df_filtered.empty:
    col1, col2, col3, col4 = st.columns(4)

    # KPI Metrics
    with col1:
        total_customer = df_filtered['count_customer'].sum()
        total_customer_format = format_number(total_customer)
        st.metric(label='Total Customer', value=total_customer_format)
        
    with col2:
        feeling_temperature = df_filtered['feeling_temperature'].mean()
        st.metric(label='Feeling Temperature', value=f'{feeling_temperature:.2f}\u00B0C')
        
    with col3:
        min_temperature = df_filtered['temperature'].min()
        st.metric(label='Lowest Temperature', value=f'{min_temperature:.2f}\u00B0C')
        
    with col4:
        max_temperature = df_filtered['temperature'].max()
        st.metric(label='Highest Temperature', value=f'{max_temperature:.2f}\u00B0C')

    st.divider()

    col5, padding, col6 = st.columns([4, 1, 4])   

    with col5:
        casual_customer = df_filtered['casual'].sum()
        subcription_customer = df_filtered['registered'].sum()
        percentage_registered = subcription_customer / total_customer
        
        fig, ax = plt.subplots(figsize=(5, 3))
        
        sizes = [casual_customer, subcription_customer, total_customer]
        colors = ['#D3D3D3', '#1E88E5', '#FFFFFF']
        
        ax.pie(sizes, colors=colors, startangle=0, counterclock=True)
        
        center_circle = plt.Circle((0,0), 0.75, fc='white')
        ax.add_artist(center_circle)
        
        ax.set_ylim(0, 1)
        ax.axis('equal')
        
        ax.text(0, 0.1, f'{percentage_registered:.2f}%', ha='center', va='center', fontsize=20, fontweight='bold', color='#1E88E5')
        ax.text(0, -0.15, "Subcription", ha='center', va='center', fontsize=12, color='gray')
        plt.axis('off')
        st.pyplot(fig)

    with col6:
        avg_humidity = df_filtered['humidity'].mean()
        max_humidity = bike_df['humidity'].max()
        
        fig, ax = plt.subplots(figsize=(5, 3))
        
        sizes = [max_humidity - avg_humidity, avg_humidity, max_humidity]
        colors = ['#D3D3D3', '#1E88E5', '#FFFFFF']
        
        ax.pie(sizes, colors=colors, startangle=0, counterclock=True)
        
        center_circle = plt.Circle((0,0), 0.75, fc='white')
        ax.add_artist(center_circle)
        
        ax.set_ylim(0, 1)
        ax.axis('equal')
        
        ax.text(0, 0.1, f'{avg_humidity:.2f}%', ha='center', va='center', fontsize=20, fontweight='bold', color='#1E88E5')
        ax.text(0, -0.15, "Humidity", ha='center', va='center', fontsize=12, color='gray')
        plt.axis('off')
        st.pyplot(fig)

    col7, spacer, col8 = st.columns([4, 1, 4])
    
    with col7:
        byweather = df_filtered.groupby('weathersit')['count_customer'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(7, 4))
        
        max_val = byweather['count_customer'].max()
        
        colors = ['#1E88E5' if (val == max_val) else '#D3D3D3' for val in byweather['count_customer']]
        
        ax.bar(byweather['weathersit'], byweather['count_customer'], color=colors)
        
        ax.set_title('AVG Customer Rent based on Weather', fontsize=10)
        ax.set_ylabel('Average Rent')
        ax.set_xlabel('Weather Situation')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        st.pyplot(fig)
        
    with col8:
        bymonth = df_filtered.groupby('month')['count_customer'].sum().reset_index()
        
        fig, ax = plt.subplots(figsize=(7, 4))
        
        ax.plot(
            bymonth['month'],
            bymonth['count_customer'],
            linestyle='-',
            marker='o'
        )
        
        ax.set_title('Trends Monthly Rent Bike')
        ax.set_ylabel('total customer')
        
        st.pyplot(fig)
        
    col9, spacer, col10 = st.columns([4, 1, 4])
    
    with col9:
        byweekday = df_filtered.groupby('weekday').agg(
            avg_casual_customer=('casual', 'mean'),
            avg_subcription_customer=('registered', 'mean')
        ).reset_index()
        
        sort_weekday = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        byweekday['weekday'] = pd.Categorical(byweekday['weekday'], categories=sort_weekday, ordered=True)
        byweekday = byweekday.sort_values('weekday')
        
        fig, ax = plt.subplots(figsize=(7, 4))
        
        ax.plot(
            byweekday['weekday'],
            byweekday['avg_casual_customer'],
            label='casual',
            marker='o',
            color='pink'
        )
        
        ax.plot(
            byweekday['weekday'],
            byweekday['avg_subcription_customer'],
            label='subcription',
            marker='o',
            color='#1E88E5'
        )
        
        ax.set_title('Trends Weekday Rent Bike')
        ax.set_ylabel('Total Customer')
        ax.legend()
        
        st.pyplot(fig)
        
    with col10:
        byhour = df_filtered.groupby('hour').agg(
            avg_casual_customer=('casual', 'mean'),
            avg_subcription_customer=('registered', 'mean')
        ).reset_index()
        
        fig, ax = plt.subplots(figsize=(7, 4))
        
        ax.plot(
            byhour['hour'],
            byhour['avg_casual_customer'],
            label='casual',
            marker='o',
            color='pink'
        )
        
        ax.plot(
            byhour['hour'],
            byhour['avg_subcription_customer'],
            label='subcription',
            marker='o',
            color='#1E88E5'
        )
        
        ax.set_title('Trends Hour Rent Bike')
        ax.set_ylabel('Total Customer')
        ax.legend()
        
        st.pyplot(fig)
else:
    st.warning('Please select at least one filter in the sidebar')