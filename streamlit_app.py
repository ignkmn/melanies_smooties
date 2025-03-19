# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smooties :cup_with_straw:")
st.write("Choose the fruit you want ")

#option = st.selectbox('What is your favorite fruit?',('Banana', 'Strawberry', 'Peach'))
#st.write('Your favorite fruit is ', option)
name_on_order = st.text_input('Your name? ')
st.write('Your name on Smooties: ' + name_on_order)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect('Choose upt to 5 ingredients'
                                 , my_dataframe
                                 , max_selections=5)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)

    ingredient_string = ''
    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen + ' '

    #st.write(ingredient_string)

    my_insert_stat = """insert into SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER) values('""" + ingredient_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stat)
    #st.stop()
    if ingredient_string:
        time_to_insert = st.button('Submit Order')
        if time_to_insert:
            session.sql(my_insert_stat).collect()
            st.success('Your Smoothie is ordered, '+ name_on_order + '!!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
#sf_dt = st.dataframe(data=smoothiefroot_response.json(),use_container_witdh=True)
