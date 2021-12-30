import time
import streamlit as st

text = "Welcome to the first day... of the rest... of your life"


t = st.empty()
for i in range(len(text) + 1):
    t.markdown("## %s..." % text[0:i])

    
    time.sleep(0.1)