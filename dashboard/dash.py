# Importing required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import plotly.express as px
import plotly.graph_objects as go

# Setting the seaborn style for all plots to 'dark'
sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
# Fungsi di bawah ini digunakan untuk mempersiapkan berbagai dataframe yang akan digunakan dalam analisis data penyewaan sepeda.

# Fungsi untuk membuat dataframe penyewaan harian (total semua penyewaan per hari)
def create_daily_rent_df(df):
    # Grouping data berdasarkan tanggal dan menghitung total penyewaan sepeda per hari
    daily_rent_df = df.groupby(by='date').agg({
       "count": "sum"
    }).reset_index()
    return daily_rent_df

# Fungsi untuk membuat dataframe penyewaan harian untuk penyewa kasual (casual)
def create_daily_casual_rent_df(df):
    # Grouping data berdasarkan tanggal dan menghitung total penyewaan kasual per hari
    daily_casual_rent_df = df.groupby(by='date').agg({
       "casual": "sum"
    }).reset_index()
    return daily_casual_rent_df

# Fungsi untuk membuat dataframe penyewaan harian untuk penyewa terdaftar (registered)
def create_daily_registered_rent_df(df):
   # Grouping data berdasarkan tanggal dan menghitung total penyewaan terdaftar per hari
   daily_registered_rent_df = df.groupby(by='date').agg({
       "registered": "sum"
    }).reset_index()
   return daily_registered_rent_df

# Fungsi untuk membuat dataframe penyewaan berdasarkan musim (season)
def create_season_rent_df(df):
    # Grouping data berdasarkan musim dan menghitung total penyewaan untuk penyewa terdaftar dan kasual
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Fungsi untuk membuat dataframe penyewaan bulanan
def create_monthly_rent_df(df):
    # Grouping data berdasarkan bulan dan menghitung total penyewaan per bulan
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    
    # Mendefinisikan urutan bulan yang benar
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    
    # Mengurutkan dataframe berdasarkan urutan bulan dan mengisi dengan 0 jika tidak ada data
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Fungsi untuk membuat dataframe penyewaan tahunan
def create_yearly_rent_df(df):
    # Grouping data berdasarkan tahun dan menghitung total penyewaan per tahun
    yearly_rent_df = df.groupby(by='year').agg({
        'count': 'sum'
    })
    
    # Mendefinisikan urutan tahun yang benar
    ordered_year = ['2011', '2012']
    
    # Mengurutkan dataframe berdasarkan urutan tahun dan mengisi dengan 0 jika tidak ada data
    yearly_rent_df = yearly_rent_df.reindex(ordered_year, fill_value=0)
    return yearly_rent_df

# Fungsi untuk membuat dataframe penyewaan berdasarkan hari dalam seminggu
def create_weekday_rent_df(df):
    # Grouping data berdasarkan hari dalam seminggu dan menghitung total penyewaan per hari
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Fungsi untuk membuat dataframe penyewaan berdasarkan hari kerja (working day)
def create_workingday_rent_df(df):
    # Grouping data berdasarkan apakah hari tersebut hari kerja atau bukan dan menghitung total penyewaan
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Fungsi untuk membuat dataframe penyewaan berdasarkan hari libur (holiday)
def create_holiday_rent_df(df):
    # Grouping data berdasarkan apakah hari tersebut adalah hari libur dan menghitung total penyewaan
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Fungsi untuk membuat dataframe penyewaan berdasarkan kondisi cuaca (weather)
def create_weather_rent_df(df):
    # Grouping data berdasarkan kondisi cuaca dan menghitung total penyewaan
    weather_rent_df = df.groupby(by='weather').agg({
        'count': 'sum'
    })
    return weather_rent_df
        
# Load cleaned data
url = "https://raw.githubusercontent.com/GdWidnyana/Analisis-Data-Sepeda-GdWidnyana/main/dashboard/clean_day.csv"

try:
    all_df = pd.read_csv(url)
except pd.errors.ParserError as e:
    print(f"Error parsing CSV: {e}")
except Exception as e:
    print(f"Error: {e}")

# Konversi kolom 'date' menjadi tipe datetime
all_df['date'] = pd.to_datetime(all_df['date'])

# Filter data
min_date = all_df['date'].dt.date.min()
max_date = all_df['date'].dt.date.max()

with st.sidebar:
    # Menambahkan logo
    image_url = "https://github.com/GdWidnyana/Analisis-Data-Sepeda-GdWidnyana/blob/main/dashboard/sepeda.jpg"
    st.image(image_url, use_column_width=True)

    # Memilih Start Date secara terpisah
    start_date = st.date_input(
        label='Start Date',
        min_value=min_date,
        max_value=max_date,
        value=min_date  # Set nilai default menjadi min_date
    )

    # Memilih End Date secara terpisah
    end_date = st.date_input(
        label='End Date',
        min_value=min_date,
        max_value=max_date,
        value=max_date  # Set nilai default menjadi max_date
    )

# Konversi start_date dan end_date menjadi datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan rentang tanggal
main_df = all_df[(all_df["date"] >= start_date) & 
                 (all_df["date"] <= end_date)]


# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
yearly_rent_df = create_yearly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Membuat judul dashboard
# Membuat judul dashboard di tengah
st.markdown("<h1 style='text-align: center; color: black;'>Analisis Data Bike Sharing</h1>", unsafe_allow_html=True)


st.write("------------------------------------------------")

# Membuat jumlah penyewa sepeda per hari
st.subheader('Penyewaan Harian')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual Customer', value=daily_rent_casual)
    
with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered Customer', value=daily_rent_registered)
    
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total Customer', value=daily_rent_total)

st.write("------------------------------------------------") 
# Membuat jumlah penyewa sepeda per bulan
st.subheader('Grafik Jumlah Sewa Sepeda setiap Bulan')
fig = px.line(
    monthly_rent_df,
    x=monthly_rent_df.index,
    y='count',
    markers=True,
    labels={'x': 'Month', 'count': 'Total Rental'},
    title='Sewa sepeda per bulan',
    template='plotly'
)
fig.update_traces(line=dict(color='green'))
st.plotly_chart(fig)

# Membuat jumlah penyewa sepeda per tahun
all_df['month'] = pd.Categorical(all_df['month'], categories=
    ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    ordered=True)

monthly_counts = all_df.groupby(by=["month", "year"]).agg({
    "count": "sum"
}).reset_index()

st.write("------------------------------------------------")

st.subheader("Tren sewa grafik per bulan untuk setiap tahun")
fig = px.line(
    monthly_counts,
    x='month',
    y='count',
    color='year',
    markers=True,
    labels={'count': 'Total Rental'},
    title='Jumlah sewa setiap bulan berdasarkan tahun ',
    template='plotly'
)
st.plotly_chart(fig)

st.write("------------------------------------------------")

# Visualisasi 1: Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca
st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
fig = px.bar(
    weather_rent_df,
    x=weather_rent_df.index,  # Menggunakan indeks untuk x-axis
    y='count',
    labels={'count': 'Jumlah Sewa', 'weather': 'Cuaca'},
    title="Jumlah sewa setiap cuaca",
    template='plotly',
    color=weather_rent_df.index,  # Warna berdasarkan kondisi cuaca
    color_continuous_scale=px.colors.sequential.Viridis
)
fig.update_layout(xaxis_title='Cuaca')  # Menambahkan label untuk sumbu x
st.plotly_chart(fig)

all_df['date'] = pd.to_datetime(all_df['date'])
all_df['season'] = all_df['date'].dt.strftime('%B')  # Assume you have a season column

# Create a dataframe for season-wise rentals
season_rent_df = all_df.groupby('season').agg({'registered': 'sum', 'casual': 'sum'}).reset_index()

st.write("------------------------------------------------")

# Visualisasi 2: Jumlah Penyewaan Sepeda Berdasarkan Musim
st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Musim')

fig = px.bar(
    season_rent_df,
    x='season',
    y=['registered', 'casual'],  # Menampilkan jumlah penyewa terdaftar dan kasual
    labels={'season': 'Musim', 'value': 'Jumlah sewa'},
    title="Jumlah sewa setiap musim",
    template='plotly',
    color_discrete_sequence=px.colors.qualitative.Plotly  # Warna yang berbeda untuk setiap kategori
)

# Update layout to group bars instead of stacking
fig.update_layout(barmode='group')

# Display the plot
st.plotly_chart(fig)

st.write("------------------------------------------------")

# Visualisasi 3: Jumlah Penyewaan Sepeda per Jam
st.subheader('Tren Jumlah Penyewaan Sepeda per Jam')
hourly_counts = all_df.groupby('hour')['count'].mean().reset_index()
fig = px.line(
    hourly_counts,
    x='hour',
    y='count',
    markers=True,
    labels={'hour': 'hour', 'count': 'jumlah sewa'},
    title="perkembangan jumlah sewa setiap jam ",
    template='plotly'
)
st.plotly_chart(fig)


st.write("------------------------------------------------")

# Visualisasi 4: Hubungan Suhu, Kelembaban, dan Kecepatan Angin dengan Jumlah Penyewaan
st.subheader('Hubungan Suhu, Kelembaban, dan Kecepatan Angin dengan Jumlah Penyewaan')
fig_temp = px.scatter(
    all_df, x='temp', y='count',
    labels={'temp': 'Suhu', 'count': 'jumlah sewa'},
    title='Hubungan suhu dan jumlah sewa',
    template='plotly'
)
st.plotly_chart(fig_temp)

fig_hum = px.scatter(
    all_df, x='hum', y='count',
    labels={'hum': 'Kelembaban', 'count': 'jumlah sewa'},
    title='Hubungan Kelembaban dan jumlah sewa',
    template='plotly'
)
st.plotly_chart(fig_hum)

fig_windspeed = px.scatter(
    all_df, x='windspeed', y='count',
    labels={'windspeed': 'kecepatan angin', 'count': 'jumlah sewa'},
    title='Hubungan kecepatan angin dan jumlah sewa',
    template='plotly'
)
st.plotly_chart(fig_windspeed)

st.write("------------------------------------------------")

# Visualisasi 5: Perbandingan Jumlah Penyewaan Sepeda pada Hari Libur dan Bukan Hari Libur
st.subheader('Perbandingan Jumlah Penyewaan Sepeda pada Hari Libur dan Bukan Hari Libur')
all_df['holiday'] = all_df['holiday'].map({0: 'Not Holiday', 1: 'Holiday'})

# Menghitung total penyewa untuk masing-masing kategori
holiday_counts = all_df.groupby('holiday')['count'].sum().reset_index()

fig = px.bar(
    holiday_counts,  # Menggunakan data agregat
    x='holiday',
    y='count',
    text='count',  # Menampilkan jumlah di atas batang
    labels={'holiday': 'Type of Day', 'count': 'Number of Renters'},
    title="Comparison of Rents on Holiday and Weekday",
    template='plotly',
    color='holiday',
    color_discrete_map={'Not Holiday': '#636EFA', 'Holiday': '#EF553B'}  # Assign specific colors
)

# Mengatur layout untuk menampilkan teks di atas batang
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')  # Menyembunyikan teks yang terlalu kecil

st.plotly_chart(fig)

# Preprocessing
all_df['date'] = pd.to_datetime(all_df['date'])
all_df['year'] = all_df['date'].dt.year
all_df['month'] = all_df['date'].dt.month
all_df['day'] = all_df['date'].dt.day

# Create RFM metrics
rfm_df = all_df.groupby('registered').agg({
    'date': 'max',             # Last rental date
    'count': 'sum'             # Total rentals
}).reset_index()

# Rename the columns
rfm_df.columns = ['customer_id', 'last_rental_date', 'total_rentals']

# Calculate Recency, Frequency, and Monetary
today = all_df['date'].max()  # Consider the last date in the dataset as 'today'
rfm_df['recency'] = (today - rfm_df['last_rental_date']).dt.days
rfm_df['frequency'] = rfm_df['total_rentals']
rfm_df['monetary'] = rfm_df['total_rentals']  # Assume monetary value is the same as the rental count for this example

# Drop unnecessary columns
rfm_df = rfm_df[['customer_id', 'recency', 'frequency', 'monetary']]

st.write("------------------------------------------------")

# Streamlit application for RFM Analysis
st.header('🚴AnalisiS RFM (Recency Frequency Monetary) 🧑‍💻')

# Display RFM table
st.subheader('RFM Table')
st.dataframe(rfm_df)

# Visualization of RFM
fig = px.scatter(rfm_df,
                 x='recency', 
                 y='frequency',
                 size='monetary',
                 hover_name='customer_id',
                 title='RFM Analysis',
                 labels={'recency': 'Recency (Days)', 'frequency': 'Frequency', 'monetary': 'Monetary'})
st.plotly_chart(fig)

st.write("------------------------------------------------")

# Additional visualizations
st.subheader('Frequency Distribution')
fig_freq = px.histogram(rfm_df, x='frequency', nbins=30, title='Frequency Distribution')
st.plotly_chart(fig_freq)

st.write("------------------------------------------------")

st.subheader('Recency Distribution')
fig_recency = px.histogram(rfm_df, x='recency', nbins=30, title='Recency Distribution')
st.plotly_chart(fig_recency)

# Define categories for RFM
def categorize_rfm(row):
    # Define Recency categories
    if row['recency'] <= 30:
        r_category = 'Very Recent'
    elif row['recency'] <= 60:
        r_category = 'Recent'
    elif row['recency'] <= 90:
        r_category = 'Less Recent'
    else:
        r_category = 'Not Recent'

    # Define Frequency categories
    if row['frequency'] >= 50:
        f_category = 'High Frequency'
    elif row['frequency'] >= 20:
        f_category = 'Medium Frequency'
    else:
        f_category = 'Low Frequency'

    # Define Monetary categories
    if row['monetary'] >= 1000:
        m_category = 'High Value'
    elif row['monetary'] >= 500:
        m_category = 'Medium Value'
    else:
        m_category = 'Low Value'

    return pd.Series([r_category, f_category, m_category])

# Apply categorization to create segments
rfm_df[['R_category', 'F_category', 'M_category']] = rfm_df.apply(categorize_rfm, axis=1)
rfm_df['segment'] = rfm_df['R_category'] + ' / ' + rfm_df['F_category'] + ' / ' + rfm_df['M_category']

st.write("------------------------------------------------")

# Streamlit application for Clustering
st.header('🚴‍♂️ Klasterisasi Pelanggan berdasarkan analisis RFM 🧑‍💻')

# Display Clustering Table
st.subheader('Clustering Table')
st.dataframe(rfm_df)

# Visualizing RFM categories
category_counts = rfm_df['segment'].value_counts().reset_index()
category_counts.columns = ['Segment', 'Count']
fig_segments = px.bar(category_counts, x='Segment', y='Count', title='Counts of Customer Segments')
st.plotly_chart(fig_segments)

st.write("------------------------------------------------")
# Bagian untuk analisis Korelasi
st.header('🚴‍♂️ Korelasi Fitur-Fitur yang berhubungan dengan Count (Jumlah Sewa Sepeda) 🧑‍💻')

# Filter hanya kolom numerik
numerical_df = all_df.select_dtypes(include=['float64', 'int64'])

# Menghitung matriks korelasi dari dataset numerik
correlation_matrix = numerical_df.corr()

# Mengambil korelasi terhadap 'count' dan mengurutkannya
correlation_with_count = correlation_matrix['count'].sort_values(ascending=False)

# Mengubah ke DataFrame untuk mempermudah visualisasi
correlation_df = correlation_with_count.reset_index()
correlation_df.columns = ['Feature', 'Correlation']

# Membuat diagram batang interaktif menggunakan Plotly
fig = px.bar(
    correlation_df,
    x='Feature',
    y='Correlation',
    color='Correlation',
    color_continuous_scale='RdBu',
    title='Korelasi Fitur-Fitur terhadap Count',
    labels={'Correlation': 'Nilai Korelasi', 'Feature': 'Fitur'},
    template='plotly'
)

# Menambahkan sorting berdasarkan nilai korelasi
fig.update_layout(xaxis={'categoryorder': 'total descending'})

# Menampilkan grafik pada Streamlit
st.plotly_chart(fig)

st.write('### Analisis Korelasi Fitur')
st.write("Fitur dengan korelasi tinggi terhadap count menunjukkan keterkaitan yang kuat dengan jumlah sewa sepeda, sedangkan fitur dengan korelasi rendah memiliki hubungan yang lemah.")

# Mendapatkan fitur dengan korelasi tertinggi dan terendah terhadap 'count'
top_correlated_features = correlation_with_count.head(5)  # 5 fitur dengan korelasi tertinggi
bottom_correlated_features = correlation_with_count.tail(5)  # 5 fitur dengan korelasi terendah

# Menampilkan deskripsi fitur dengan korelasi tertinggi dan terendah
st.write('### Fitur dengan Korelasi Tertinggi terhadap Count:')
st.write("Fitur berkorelasi tinggi memiliki keterhubungan kuat terhadap fitur count")
for feature, score in top_correlated_features.items():
    st.write(f"- **{feature}**: {score:.2f}")

st.write('### Fitur dengan Korelasi Terendah terhadap Count:')
st.write("Fitur berkorelasi rendah memiliki keterhubungan lemah terhadap fitur count")
for feature, score in bottom_correlated_features.items():
    st.write(f"- **{feature}**: {score:.2f}")

st.caption('Copyright (c) I Gede Widnyana 2024')
