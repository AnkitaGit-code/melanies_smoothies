# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
#cnx = st.connection("snowflake")
#session = cnx.session()
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie ! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothies
    """
)
NAME_ON_ORDER = st.text_input("Name of Smoothie")
st.write("Name Of Smoothie will be", NAME_ON_ORDER)
cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True) 
#st.stop()
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
ingredients_list = st.multiselect(
    "Choose Upto 5 Ingredients",my_dataframe, max_selections=5
)

import requests
if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + 'Nutritional Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True) 

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string +"""','""" + NAME_ON_ORDER + """')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button ('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
