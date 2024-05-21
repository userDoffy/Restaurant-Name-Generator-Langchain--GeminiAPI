import streamlit as st
import langchain_helper
import asyncio

st.title("Restaurant Name Generator")

cuisine=st.sidebar.text_input("Enter your Cuisine: ")

if cuisine:
    try:
        loop=asyncio.get_event_loop()
    except: 
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    response=loop.run_until_complete(langchain_helper.generate_restaurant_name_and_items(cuisine))
    print(response)

    st.header(response['restaurant_name'].strip())
    slogan=response['slogan'].strip()
    st.write("**Slogan:** "+slogan)
    menu_items=response['menu_items'].strip().split(',')
    st.write("**Menu Items**")
    for item in menu_items:
        st.write("-",item)
