# import streamlit as st
# # import pandas as pd
# # import numpy as np
# from request import url
# import requests
# from sql_table import returnRows
# from gemini_sql import generateQuery

# # Page config
# st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Sidebar
# st.sidebar.title("Chat Options")
# if st.sidebar.button("🆕 New Chat"):
#     st.session_state.messages = []  # Clear chat history
#     st.rerun()

# # Chat header
# st.title("🤖 FLoatchat")

# # Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Chat input
# if prompt := st.chat_input("Type your message..."):
#     # Store user message
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Use the payload from sql_table.py as input, but override the question with user's prompt
#     payload = {"question": prompt}
#     response = requests.post(url, json=payload)
#     response = response.json()
    
#     local_payload = payload.copy()
#     local_payload["question"] = prompt
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         message_placeholder.markdown("Response Loading...")    
    

#     # Generate response using logic similar to summary.py
#     arr = [
#         f"""
#         {returnRows(response)}
#         """
#     ]

#     prompt_for_query = [
#         """
#         YOU ARE A DATA ANALYZER FOR THE SQL QUERY RESPONSE THAT YOU GET AS A QUERY\n
#         THE DATA PROVIDED IS OCEAN ARGO DATA, SO BE CONTEXTUAL AROUND IT\n
#         BE REALISTIC DONT HALLUCINATE OR CREATE NEW DATA, STICK TO WHAT IS PROVIDED\n
#         ENSURE QUALITY OUTPUTS\n
#         ALTHOUGH YOU ARE A DATA ANAYLZER FOR SQL, DONT INCLUDE WORDS RELATED TO SQL like:\n
#         --Example 1---
#         INCORRECT: The provided SQL query result, a data tuple `(10.523094611450471, 971.2524209537997)` rather say:\n
#         CORRECT: The provided resultant is, a data tuple `(10.523094611450471, 971.2524209537997)`\n
#         --Example 2--- 
#         INCORRECT: Based on the characteristic structure and typical ranges of Ocean Argo data parameters, this specific data point from the SQL query most probably represents an **ocean temperature of approximately 10.52 degrees Celsius, observed at a depth/pressure of roughly 971.25 meters** within an Argo float's vertical measurement profile.\n
#         CORRECT: Based on the characteristic structure and typical ranges of Ocean Argo data parameters, this specific data point most probably represents an **ocean temperature of approximately 10.52 degrees Celsius, observed at a depth/pressure of roughly 971.25 meters** within an Argo float's vertical measurement profile.\n
#         """
#     ]

#     prompt_summarizer = [
#         """

#         GENERAL INFO : YOU ARE DEALING WITH OCEAN ARGO DATA SQL SUMMARIZED\n
#         ROLE:YOU ARE A SQL DATA ANALYSIS TO SUMMARIZER & YOU ARE ACTUALLY AN API ENDPOINT RESPONSE FOR A CHATTING APPLICATION, SO IN THAT CONTEXT SUMMARIZE, DON'T BE TOO MUCH THEORTICAL IN YOUR ANSWERS, BUT THAT DOESNT MEAN THAT YOU ARE ESSENTIAL NOT SUMMARIZING THE DATA ANALYSIS\n
#         SUMMARIZE VERY ACCURATELY, BUT DON'T LOOSE THE ESSENCE MEANING, THE QUERY THAT YOU GET IN YOUR INPUT, WOULD BE A BIT LARGE, SO WHILE SUMMARIZING JUST DONT SHORTEN TO SOMETHING VERY SHORT,\n
#         RATHER, KEEP THE LANGUAGE, KEEP THE WORDINGS, KEEP THE TERMINOLOGIES, KEEP THE REPORT ANALYSIS IN THE MAIN PICTURE.\n
#         ALSO YOU MAY RECEIVE SOME TERMS LIKE "DATA ANALYSIS" or "SQL QUERY" - YOUR MAIN JOB IS TO TURN THAT OVER SUCH THAT, USER WHO SEE YOUR RESPONSE, MUST RELATED IT TWO HUNDRED PERCENT WITH THE DATA\n
#         MAKE IT ALL AROUND THE OCEAN ARGO DATA TERMINLOGIES, WORDINGS, PARAMETERS, AND STATISTICAL ANALYSIS\n
#         VERY IMP- DO NOT LOOSE UPON THE ESSENCE OF STATISTICAL ANAYLSIS SUMMARIZED TEXT CONTEXT\n
#         BUT, ALSO ENSURE THAT YOU ARE NOT HALLUCINATING UPON ANY DATA
#         """
#     ]
    
#     analyzed = generateQuery(prompt_for_query,arr[0])
#     response_from_model = generateQuery(prompt_summarizer,analyzed)

#     # Store assistant message
#     st.session_state.messages.append({"role": "assistant", "content": response_from_model})
#     with st.chat_message("assistant"):
#         st.markdown(response_from_model)

# # ----------- Visualization Button -----------
# # 

import streamlit as st
import pandas as pd
import numpy as np
from sql_table import returnRows, insert_chat_history
from gemini_sql import generateQuery
from request import url
import requests
import plotly.express as px # Import plotly

# Page config
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_plot_data" not in st.session_state: # Initialize plot data
    st.session_state.current_plot_data = None

# Sidebar
st.sidebar.title("Chat Options")
if st.sidebar.button("🆕 New Chat"):
    st.session_state.messages = []  # Clear chat history
    st.rerun()

# Chat header
st.title("🤖 FLoatchat")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Handle basic greetings
    if prompt.lower() in ["hi", "hello", "hey"]:
        response_from_model = "Hello! How can I help you with Ocean Argo data today?"
        # No loading message needed for instant responses
    else:
        # Display a loading message
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Response Loading...")

        payload = {"question":prompt}
        # Use the payload from sql_table.py as input, but override the question with user's prompt
        local_payload = payload.copy()
        local_payload["question"] = prompt

        # Make an HTTP POST request to the /query endpoint
        try:
            api_response = requests.post(url, json=local_payload)
            api_response.raise_for_status()  # Raise an exception for HTTP errors
            dynamic_response = api_response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the backend: {e}")
            # If there's an error, we don't proceed with LLM processing
            response_from_model = "I'm sorry, I'm having trouble connecting to the data analysis service right now. Please try again later."
            dynamic_response = None # Ensure dynamic_response is reset if error occurs

        # Initialize plot_data_for_session to None for non-greeting responses
        plot_data_for_session = None

        # Only proceed with LLM if there was no API error and dynamic_response is available
        if dynamic_response:
            raw_data_for_plot = returnRows(dynamic_response) # Get all rows
            if raw_data_for_plot and len(raw_data_for_plot[0]) >= 2: # Ensure data is present and has at least 2 columns
                # Assuming first column is depth/x-axis and second is value/y-axis
                # More robust column naming might be needed based on actual SQL queries
                try:
                    plot_data_for_session = pd.DataFrame(raw_data_for_plot, columns=["Depth/Pressure", "Value"])
                    st.session_state.current_plot_data = plot_data_for_session
                except Exception as e:
                    st.warning(f"Could not create DataFrame for plotting: {e}")
                    st.session_state.current_plot_data = None
            else:
                st.session_state.current_plot_data = None

            # Generate response using logic similar to summary.py
            arr = [
                f"""
                {returnRows(dynamic_response)}
                """
            ]

            prompt_for_query = [
                """
                YOU ARE A DATA ANALYZER FOR THE SQL QUERY RESPONSE THAT YOU GET AS A QUERY\n
                THE DATA PROVIDED IS OCEAN ARGO DATA, SO BE CONTEXTUAL AROUND IT\n
                BE REALISTIC DONT HALLUCINATE OR CREATE NEW DATA, STICK TO WHAT IS PROVIDED\n
                ENSURE QUALITY OUTPUTS\n
                ALTHOUGH YOU ARE A DATA ANAYLZER FOR SQL, DONT INCLUDE WORDS RELATED TO SQL like:\n
                --Example 1---
                INCORRECT: The provided SQL query result, a data tuple `(10.523094611450471, 971.2524209537997)` rather say:\n
                CORRECT: The provided resultant is, a data tuple `(10.523094611450471, 971.2524209537997)`\n
                --Example 2--- 
                INCORRECT: Based on the characteristic structure and typical ranges of Ocean Argo data parameters, this specific data point from the SQL query most probably represents an **ocean temperature of approximately 10.52 degrees Celsius, observed at a depth/pressure of roughly 971.25 meters** within an Argo float's vertical measurement profile.\n
                CORRECT: Based on the characteristic structure and typical ranges of Ocean Argo data parameters, this specific data point most probably represents an **ocean temperature of approximately 10.52 degrees Celsius, observed at a depth/pressure of roughly 971.25 meters** within an Argo float's vertical measurement profile.\n
                """
            ]

            prompt_summarizer = [
                """


                GENERAL INFO : YOU ARE DEALING WITH OCEAN ARGO DATA SQL SUMMARIZED\n
                ROLE:YOU ARE A SQL DATA ANALYSIS TO SUMMARIZER & YOU ARE ACTUALLY AN API ENDPOINT RESPONSE FOR A CHATTING APPLICATION, SO IN THAT CONTEXT SUMMARIZE, DON'T BE TOO MUCH THEORTICAL IN YOUR ANSWERS, BUT THAT DOESNT MEAN THAT YOU ARE ESSENTIAL NOT SUMMARIZING THE DATA ANALYSIS\n
                SUMMARIZE VERY ACCURATELY, BUT DON'T LOOSE THE ESSENCE MEANING, THE QUERY THAT YOU GET IN YOUR INPUT, WOULD BE A BIT LARGE, SO WHILE SUMMARIZING JUST DONT SHORTEN TO SOMETHING VERY SHORT,\n
                RATHER, KEEP THE LANGUAGE, KEEP THE WORDINGS, KEEP THE TERMINOLOGIES, KEEP THE REPORT ANALYSIS IN THE MAIN PICTURE.\n
                ALSO YOU MAY RECEIVE SOME TERMS LIKE "DATA ANALYSIS" or "SQL QUERY" - YOUR MAIN JOB IS TO TURN THAT OVER SUCH THAT, USER WHO SEE YOUR RESPONSE, MUST RELATED IT TWO HUNDRED PERCENT WITH THE DATA\n
                MAKE IT ALL AROUND THE OCEAN ARGO DATA TERMINLOGIES, WORDINGS, PARAMETERS, AND STATISTICAL ANALYSIS\n
                VERY IMP- DO NOT LOOSE UPON THE ESSENCE OF STATISTICAL ANAYLSIS SUMMARIZED TEXT CONTEXT\n
                BUT, ALSO ENSURE THAT YOU ARE NOT HALLUCINATING UPON ANY DATA
                """
            ]
            
            analyzed = generateQuery(prompt_for_query,arr[0])
            response_from_model = generateQuery(prompt_summarizer,analyzed)
        else:
            # If dynamic_response is None due to an API error, response_from_model is already set
            pass # No change needed, error message already set
    
    # Store assistant message
    st.session_state.messages.append({"role": "assistant", "content": response_from_model})
    with st.chat_message("assistant"):
        # If it was a greeting, message_placeholder was not created, so directly markdown
        if prompt.lower() in ["hi", "hello", "hey"]:
            st.markdown(response_from_model)
        else:
            # If it was a regular query, use the placeholder to update
            message_placeholder.markdown(response_from_model)

    # Store the interaction in the database
    insert_chat_history(prompt, response_from_model)

# ----------- Visualization Button -----------

if st.button("📊 Visualize"):
    st.subheader("Data Visualization")
    if st.session_state.current_plot_data is not None and not st.session_state.current_plot_data.empty:
        fig = px.line(
            st.session_state.current_plot_data,
            x="Depth/Pressure",
            y="Value",
            title="Data Profile Visualization"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No plottable data available from the last query.")