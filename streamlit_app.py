# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie ! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothies
    """
)
NAME_ON_ORDER = st.text_input("Name of Smoothie")
st.write("Name Of Smoothie will be", NAME_ON_ORDER)

from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True) 

ingredients_list = st.multiselect(
    "Choose Upto 5 Ingredients",my_dataframe, max_selections=5
)

if ingredients_list:

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string +"""','""" + NAME_ON_ORDER + """')"""

    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button ('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")