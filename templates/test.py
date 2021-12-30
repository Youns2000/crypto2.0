import streamlit as st
import numpy as np
import time

delay_time = st.number_input("Delay", value=2)
run = st.checkbox("Run")
status_text = st.empty()
chart = st.line_chart(np.random.randn(10, 2))
full_replacement_chart = st.empty()

while run:
    new_rows = np.random.randn(10, 2)

    # Update status text.
    status_text.text("The latest random number is: %s" % new_rows[-1, 1])

    # Append data to the chart.
    chart.add_rows(new_rows)

    # Just replace the chart
    full_replacement_chart.line_chart(new_rows)

    # Wait
    time.sleep(delay_time)