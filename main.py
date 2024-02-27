from openai import OpenAI
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Make sure you have the API key in the environment variable; otherwise, this will be None.
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not found.")

# Set the API key for the OpenAI client
OpenAI.api_key = openai_api_key

# openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

system_instruction = """
                        Boolean Query Assistant Instructions:

                        This assistant is designed to help users construct Boolean queries strictly following the specified filtering instructions. 
                        The output from this assistant must be a Boolean query only, without additional descriptions, explanations, or extraneous text. 
                        The assistant recognizes specific keywords and applies filters as detailed below:

                        1. Current Job Title:
                          - Filter by current job title: "AS" (e.g., "AS Recruiter").
                          - Combine with "NOT"-filter: "AS NOT Senior".
                          - CAUTION: Excludes platforms without "Current Job Title" field (e.g., MeetUp).

                        2. Previous Job Title:
                          - Filter by previous job titles: "PREVIOUSLY_AS" (e.g., "PREVIOUSLY_AS Recruiter").
                          - Combine with "NOT"-filter: "PREVIOUSLY_AS NOT Senior".
                          - CAUTION: Excludes platforms without "Previous Job Title" field (e.g., MeetUp).

                        3. Current Employer:
                          - Filter by current employer: "AT" (e.g., "AT Talentwunder").
                          - Combine with "NOT"-filter: "AT NOT Talentwunder".
                          - CAUTION: Excludes platforms without "Current Employer" field (e.g., MeetUp).

                        4. Previous Employers:
                          - Filter by previous employers: "PREVIOUSLY_AT" (e.g., "PREVIOUSLY_AT Talentwunder").
                          - Combine with "NOT"-filter: "PREVIOUSLY_AT NOT Talentwunder".
                          - CAUTION: Excludes platforms without "Previous Employer" field (e.g., MeetUp).

                        5. Language Skills:
                          - Filter by language skill: "SPEAKS" (e.g., "SPEAKS English").
                          - CAUTION: Excludes platforms without "Languages spoken" field (e.g., MeetUp).

                        6. Gender:
                          - Filter by gender: "IS" (e.g., "IS FEMALE" or "IS MALE").
                          - This filter works in every network.

                        7. Change Probability:
                          - Filter by likelihood of job change: "CHANGE_PROBABILITY ABOVE" (e.g., "CHANGE_PROBABILITY ABOVE 55").
                          - 50 is neutral. Above 50 indicates a higher chance of changing jobs.

                        8. Moving Probability:
                          - Filter by likelihood to relocate: "MOBILITY ABOVE" (e.g., "CHANGE_PROBABILITY ABOVE 55").
                          - 50 is neutral. Above 50 indicates a higher chance of relocating.

                        9. Professional Experience:
                          - Filter by years of work experience: "YEARS_WORKING" (e.g., "YEARS_WORKING 2 TO 4").
                          - CAUTION: Excludes platforms without "Professional Experience" field (e.g., MeetUp).

                        10. Experience in Current Position:
                            - Filter by years in current job: "YEARS_IN_JOB" (e.g., "YEARS_IN_JOB 2 TO 4").
                            - CAUTION: Excludes platforms without "Previous Positions" field (e.g., MeetUp).

                        11. Candidates with Mail Address:
                            - Find candidates with a mail address: "HAS EMAIL" (e.g., "HAS EMAIL").
                            - This filter works with every platform.

                        12. Phone Number:
                            - Find candidates with a phone number: "HAS PHONE" (e.g., "HAS PHONE").
                            - This filter works with every platform.

                        13. Certain Professional Groups:
                            - Include or exclude specific groups using "IS"-filter (e.g., "IS FREELANCER" or "IS NOT FREELANCER" for freelancers).

                        14. Wildcards:
                            - Use wildcards (*) for auto-completion (e.g., "Manag*" for Managers and Management).
                            - CAUTION: Wildcards only at the end of terms; cannot combine wildcards and quotation marks.

                        15. Weight Factors:
                            - Enhance term relevance with ^ (e.g., "Java^4 OR J2EE" makes Java profiles four times more relevant than J2EE).
                            
                        Important Considerations:
                          - The assistant must use keywords accurately from the instructions for filter application.
                          - Outputs are strictly Boolean queries. Ensure proper use of keywords and negations as instructed.
                          - Pay attention to "CAUTION" notes, understanding platform-specific field availability.
                          - General search for terms, skills and job title variations are composed with AND/OR statements. But other keyword are used withoud AND/OR, and listing multiple names are divided with comma, there are no repeating of hte same keyword.
                            EXAMPLE: Python Developer AND (Machine Learning OR AI) AND SPEAKS (English, German) AND AT Berlin is not correct
                                     Python Developer AND (Machine Learning OR AI) AT Berlin SPEAKS (English, German) is correct
                          - Pay attention when location is mentioned to use IN.
                          - Always try not to return very short query.
                          """

# st.title('AI Boolean Query Generator')
# # Define the list of models for the dropdown
# model_options = [
#     "ft:gpt-3.5-turbo-1106:personal::8vA1pplg",
#     "gpt-4-0125-preview"
# ]

# # Create a dropdown for model selection
# selected_model = st.selectbox("Select the model:", model_options)

# # Create a text input field in Streamlit
# user_input = st.text_area("Enter your prompt:", height=150)

# # Create a button in Streamlit for generating text
# if st.button('Generate Text'):
#     if user_input:  # Check if the user has entered some text
#         with st.spinner('Generating text... Please wait'):
#           # Call the OpenAI API with the provided user prompt and selected model
#           completion = client.chat.completions.create(
#               model=selected_model,
#               messages=[
#                 {"role": "system", "content": system_instruction},
#                 {"role": "user", "content": user_input}
#             ]
#         )
        
#           # Extract and display only the message text
#           generated_text = completion.choices[0].message.content  # Correctly access the 'content' attribute
#           st.write(generated_text)  # Display the generated message text only
#     else:
#         st.write("Please enter a prompt.")

# Placeholder for a real authentication mechanism
def check_credentials(username, password):
    # Fetch the password from environment variables
    correct_password = os.getenv('USER_PASSWORD')
    return username == "talentwunder" and password == correct_password

# # Initialize or use existing session state for login status
# if 'logged_in' not in st.session_state:
#     st.session_state['logged_in'] = False

# # UI for login
# if not st.session_state.logged_in:
#     st.title("Login")
#     with st.form("login_form"):
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         login_button = st.form_submit_button("Login")
        
#         if login_button:
#             if check_credentials(username, password):
#                 st.session_state.logged_in = True
#                 st.success("Logged in successfully.")
#             else:
#                 st.error("Incorrect username or password.")

# # Main application UI
# if st.session_state.logged_in:
#     st.title('AI Boolean Query Generator')
#     model_options = [
#         "ft:gpt-3.5-turbo-1106:personal::8vA1pplg",
#         "gpt-4-0125-preview"
#     ]

#     # Create a dropdown for model selection
#     selected_model = st.selectbox("Select the model:", model_options)

#     # Create a text input field in Streamlit
#     user_input = st.text_area("Enter your prompt:", height=150)

#     # Create a button in Streamlit for generating text
#     if st.button('Generate Text'):
#         if user_input:  # Check if the user has entered some text
#             with st.spinner('Generating text... Please wait'):
#               # Call the OpenAI API with the provided user prompt and selected model
#               completion = client.chat.completions.create(
#                   model=selected_model,
#                   messages=[
#                     {"role": "system", "content": system_instruction},
#                     {"role": "user", "content": user_input}
#                 ]
#             )
            
#               # Extract and display only the message text
#               generated_text = completion.choices[0].message.content  # Correctly access the 'content' attribute
#               st.write(generated_text)  # Display the generated message text only
#         else:
#             st.write("Please enter a prompt.")
            
            
#     st.title("Login")
#     with st.form("login_form"):
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         login_button = st.form_submit_button("Login")
#         if login_button:
#             if check_credentials(username, password):
#                 st.session_state.logged_in = True
#                 st.success("Logged in successfully.")
#                 # Using st.experimental_rerun() to force the app to rerun might help, but use it judiciously.
#                 # st.experimental_rerun()
#             else:
#                 st.error("Incorrect username or password.")
                
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Function to display the login form
def display_login_form():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        if login_button:
            if check_credentials(username, password):
                st.session_state.logged_in = True
                st.success("Logged in successfully.")
                # Using st.experimental_rerun() to force the app to rerun might help, but use it judiciously.
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password.")
                
                
def display_main_app():
    st.title('AI Boolean Query Generator')
    model_options = ["ft:gpt-3.5-turbo-1106:personal::8vA1pplg", "gpt-4-0125-preview"]
    selected_model = st.selectbox("Select the model:", model_options)
    user_input = st.text_area("Enter your prompt:", height=150)

    if st.button('Generate Text'):
        if user_input:
            with st.spinner('Generating text... Please wait'):
                # Call the OpenAI API with the provided user prompt and selected model
                completion = client.chat.completions.create(
                  model=selected_model,
                  messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input}
                ]
            )
            
                # Extract and display only the message text
                generated_text = completion.choices[0].message.content  # Correctly a
                st.write(generated_text)

# Decide which part of the app to display based on login status
if not st.session_state.logged_in:
    display_login_form()
else:
    display_main_app()
    
    