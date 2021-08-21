import streamlit as st
from streamlit import caching
import streamlit.components.v1 as components

from datetime import datetime, date, time, timedelta
import pandas as pd
import glob
import os

# Custom Functions
from main import bse_data

# streamlit
st.set_page_config(page_title='App', page_icon=':moneybag:', layout='wide', initial_sidebar_state='expanded')
st.sidebar.title(':shark:' + ' Dashboard')
@st.cache(suppress_st_warning=True)
def footer():
    with st.sidebar.expander("Credits"):
        st.success('Created by VH')
        components.html(
        """
        <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="hirawat" data-color="#FFDD00" data-emoji="☕"  data-font="Poppins" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
        """,
        height=100
        )

matching_keywords = ["Presentation", "DRHP", "FDA", "Transcript", "Press Release", "Amalgamation", "Buyback", "Contract", "Delisting", "Demerger", "Preference Shares", "Annual Report", "Result", "Board Meeting", "Dividend"]
segments = ["Equity", "Debt/Others", "MF/ETFs"]
# Widget
with st.sidebar.form("Input", clear_on_submit=False):
    segment = segments[0]
    from_date = date.today()
    to_date = date.today()
    date = from_date.strftime("%d %B %Y")
    st.write("Segment :", segment)
    st.write('Date :', date)
    #st.write('From Date', from_date)
    #st.write('To Date', to_date)
    button = st.form_submit_button("Reload")

fd = from_date.strftime("%d/%m/%Y")
td = to_date.strftime("%d/%m/%Y")

@st.cache(suppress_st_warning=True)
def get_data():
    with st.spinner(text='In progress'):
        path, timestamp = bse_data(fd, td, segment)
    return path, timestamp


#with st.spinner(text='In progress...'):
#    st.info("The code might take some time to run for the first time."+ ":dragon:")
def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    #text = link.split('=')[1]
    return f'<a target="_blank" href="{link}">Click Here</a>'


def keywords(df):
    df_new = df.copy()

    return df_new


# Main function
def main():
    path_csv, timestamp = get_data()
    df = pd.read_csv(path_csv)
    st.sidebar.write(len(df), "Announcements for Today")
    if len(df) == 0:
        st.info("No Announcements for Today. :fire: Select a Different Date and Rerun. :clown:")
        footer()
    else:
        time = timestamp.strftime('%X')
        st.sidebar.write("Last Updated at :", time) #'%I %M %p'
        footer()
        # Create Matching Keywords Column
        keywords = st.multiselect("Announcements Category", matching_keywords, default=matching_keywords)
        output_set = set()
        for var in df["More Info"]:
            if var == keywords:
                output_set.add(set)


        dfc = df.copy()
        # Data Analysis
        #df = df1
        # remove ruplicate links
        dfnew = dfc.drop_duplicates(["PDF"])
        # link is the column with hyperlinks
        dfnew['PDF'] = dfnew['PDF'].apply(make_clickable)
        dfnew1 = dfnew.to_html(escape=False)



        st.write(dfnew1, unsafe_allow_html=True)
        dir = os.getcwd() + "/data/*.html"
        file_list = glob.glob(dir)
        #files = []
        #for f in file_list:
        #    files = files.append(os.path.basename(f))

        c1, c2, c3 = st.columns(3)
        c1.success("Data Saved : " + path_csv)
        old_file = c2.selectbox("Select from previous files", file_list)
        load = c3.button("Load")

        if load:
            dfold = pd.read_html(old_file)
            st.write(dfold)


if __name__ == '__main__':
    main()
