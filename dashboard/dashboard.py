import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def main():
    df = pd.read_csv("./dashboard/main_data.csv")

    st.set_page_config(page_title="Beijing Air Quality Dashboard", page_icon="🌫️", layout="wide")
    sns.set_theme(style="darkgrid")
    st.title("Beijing Air Quality Dashboard")
    st.write("This dashboard shows the air quality in Beijing from 2013 to 2017.")

    st.markdown(
        """
        # About Me
        - **Nama:** Muhammad Nabil Saragih
        - **Email:** mnabilsaragih@gmail.com
        - **ID Dicoding:** nabilsaragih
        """
    )

    with st.sidebar:
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

        min_date = df["date"].min()
        max_date = df["date"].max()
        st.image("https://lh3.googleusercontent.com/NtORZkpsdeRJDkdA4DdUYwMUdpL1pNNO1HOVby1F6Qst1jwx6yVRkDmHJeaOtWzFLQWMPZxU_XFurb3646KdxYX8n7cYNoJeC0kpiVOhPWhayI5Z6e0X=w600")
        
        start_date, end_date = st.date_input(
            label='Rentang Waktu',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

        st.write("You have selected:", start_date, "to", end_date)

        df_filtered = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

        st.write("## Data Preview")
        st.write(df_filtered)

        st.write("## Data Summary")
        st.write(df_filtered.describe())

    st.write("## Bagaimana tingkat polusi berubah seiring waktu?")
    st.write("Grafik di bawah menunjukkan bagaimana tingkat polusi berdasarkan PM2.5 di Beijing selalu berubah di beberapa wilayah dari tahun 2013 hingga 2017.")
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title("Time Series Plot of PM2.5 for Each Station")
    sns.lineplot(x="year", y="PM2.5", hue="station", data=df_filtered, marker='o', errorbar=None, ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("PM2.5")
    ax.set_xticks(df['year'].unique())
    ax.set_xticklabels(df['year'].unique(), rotation=45)
    ax.legend(ncol=3)
    st.pyplot(fig)

    st.write("## Bagaimana perbandingan tingkat polusi udara di tiap wilayah?")
    st.write("Grafik di bawah ini memperlihatkan perbandingan tingkat polusi udara di Beijing berdasarkan rata-rata PM2.5 dari tahun 2013 hingga 2017.")
    average_pm25 = df.groupby('station')['PM2.5'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(x='station', y='PM2.5', data=average_pm25, palette='pastel', ax=ax)
    ax.set_yticks(range(0, 100, 5))
    ax.set_title("Average PM2.5 Levels by Station") 
    ax.set_xlabel("Station")
    ax.set_ylabel("Average PM2.5 Levels")
    st.pyplot(fig)

    st.write("## Distribusi tingkat polusi udara berdasarkan peta wilayah Beijing.")
    st.write("Peta di bawah ini menunjukkan distribusi tingkat polusi udara di Beijing berdasarkan rata-rata PM2.5 dari tahun 2013 hingga 2017.")
    fig, ax = plt.subplots()

    coordinates = {
        "Aotizhongxin": {
            "latitude": 39.9935,
            "longitude": 116.4850
        },
        "Changping": {
            "latitude": 40.2181,
            "longitude": 116.2055
        },
        "Dingling": {
            "latitude": 40.2950,
            "longitude": 116.2230
        },
        "Dongsi": {
            "latitude": 39.9356,
            "longitude": 116.4184
        },
        "Guanyuan": {
            "latitude": 39.9110,
            "longitude": 116.3350
        },
        "Gucheng": {
            "latitude": 39.9115,
            "longitude": 116.3080
        },
        "Huairou": {
            "latitude": 40.4310,
            "longitude": 116.6340
        },
        "Nongzhanguan": {
            "latitude": 39.9730,
            "longitude": 116.4550
        },
        "Shunyi": {
            "latitude": 40.1280,
            "longitude": 116.6540
        },
        "Tiantan": {
            "latitude": 39.8822,
            "longitude": 116.4142
        },
        "Wanliu": {
            "latitude": 39.9740,
            "longitude": 116.3080
        },
        "Wanshouxigong": {
            "latitude": 39.8950,
            "longitude": 116.3070
        }
    }

    coordinates = pd.DataFrame(coordinates).T.reset_index()
    coordinates.columns = ["station", "latitude", "longitude"]

    coordinates_and_pm25 = pd.merge(average_pm25, coordinates, on="station")

    beijing = gpd.read_file("https://raw.githubusercontent.com/d3cn/data/refs/heads/master/json/geo/china/province-city/beijing.geojson")
    beijing = beijing.to_crs("EPSG:4326")

    fig, ax = plt.subplots(figsize=(15, 8))
    beijing.plot(ax=ax, color="lightgrey")
    ax.set_title("Average PM2.5 Levels by Station in Beijing")
    ax.set_axis_off()

    scatter = ax.scatter(
        x=coordinates_and_pm25["longitude"],
        y=coordinates_and_pm25["latitude"],
        s=coordinates_and_pm25["PM2.5"] * 10,
        c=coordinates_and_pm25["PM2.5"],
        cmap="coolwarm",
        alpha=0.7,
        edgecolors="w",
        linewidth=1
    )

    for i, txt in enumerate(coordinates_and_pm25["station"]):
        ax.annotate(txt, (coordinates_and_pm25["longitude"][i], coordinates_and_pm25["latitude"][i]), fontsize=10)

    cbar = plt.colorbar(scatter)
    cbar.set_label("Average PM2.5 Levels")

    st.pyplot(fig)

if __name__ == '__main__':
    main()
