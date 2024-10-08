import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def main():
    df = pd.read_csv("dashboard\main_data.csv")

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
        st.write(df)

        st.write("## Data Summary")
        st.write(df.describe())

    st.write("## PM2.5 Data")
    fig, ax = plt.subplots()
    sns.lineplot(data=df_filtered, x="date", y="PM2.5", ax=ax)
    st.pyplot(fig)

    st.write("## PM10 Data")
    fig, ax = plt.subplots()
    sns.lineplot(data=df_filtered, x="date", y="PM10", ax=ax)
    st.pyplot(fig)

    st.write("## O3 Data")
    fig, ax = plt.subplots()
    sns.lineplot(data=df_filtered, x="date", y="O3", ax=ax)
    st.pyplot(fig)

    st.write("## NO2 Data")
    fig, ax = plt.subplots()
    sns.lineplot(data=df_filtered, x="date", y="NO2", ax=ax)
    st.pyplot(fig)

    st.write("## SO2 Data")
    fig, ax = plt.subplots()
    sns.lineplot(data=df_filtered, x="date", y="SO2", ax=ax)
    st.pyplot(fig)

    st.write("## CO Data")
    fig, ax = plt.subplots()
    sns.lineplot(data=df_filtered, x="date", y="CO", ax=ax)
    st.pyplot(fig)

    st.pyplot(plt)

if __name__ == '__main__':
    main()
