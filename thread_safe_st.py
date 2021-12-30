from streamlit.ReportThread import add_report_ctx

# Your thread creation code:
thread = threading.Thread(target=runInThread, args=(onExit, PopenArgs))
add_report_ctx(thread)
thread.start()