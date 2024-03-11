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
                      Construct Boolean queries with precision by following these structured guidelines. Your output should exclusively be a Boolean query, free from any additional descriptions or extraneous text.

Query Construction Format:
Job Titles and Variations: Begin with a list of job titles relevant to the prompt, including variations. Separate these titles using "OR" to encompass a broad range of potential matches.
Related Skills and Expertise: Follow the job titles with a list of related skills, including both those directly mentioned in the prompt and those generally associated with the job titles and also skills related to the industry, if the industry is being mentioned in the original prompt. Use "AND" or "OR" to connect these skills, aiming to balance specificity with breadth.
Additional Criteria: Incorporate any other relevant criteria mentioned in the prompt, such as location, language skills, previous positions, and experience. Detail these elements in sequence, prioritizing their order based on the prompt's emphasis. Also, do not add location and gender if they are not explicitly mentioned in the prompt
Keywords and Filters:
Current Job Title: "AS" (e.g., "AS Developer"). Exclude with "NOT" (e.g., "AS NOT Senior").
Previous Job Title: "PREVIOUSLY_AS" for past titles. Exclude with "NOT" (e.g., "PREVIOUSLY_AS NOT Manager").
Employer: "AT" for current, "PREVIOUSLY_AT" for past employers. Combine with "NOT" for exclusions.
Language Skills: "SPEAKS" (e.g., "SPEAKS English").
Gender: "IS" (e.g., "IS FEMALE" or "IS MALE").
Job Change Likelihood: "CHANGE_PROBABILITY ABOVE" (e.g., "CHANGE_PROBABILITY ABOVE 55").
Relocation Likelihood: "MOBILITY ABOVE" (e.g., "MOBILITY ABOVE 55").
Professional Experience: "YEARS_WORKING" to specify range (e.g., "YEARS_WORKING 2 TO 4").
Position Tenure: "YEARS_IN_JOB" for current role duration.
Contact Info: "HAS EMAIL" and "HAS PHONE" for availability.
Professional Groups: Include or exclude with "IS" or "IS NOT" (e.g., "IS FREELANCER", "IS NOT STUDENT").
Wildcards: Use "" for partial matches (e.g., "Manag").
Term Relevance: Enhance with "^" (e.g., "Java^4 OR J2EE").
Important Notes:
Strict Adherence: Follow the structure and keyword usage precisely.
Accuracy: Use keywords exactly as specified, combining terms with "AND"/"OR" as needed without repeating the keyword for multiple values.
Location Usage: Use "IN" strictly for location mentions.
                      """
# Placeholder for a real authentication mechanism
def check_credentials(username, password):
    # Fetch the password from environment variables
    correct_password = os.getenv('USER_PASSWORD')
    return username == "talentwunder" and password == correct_password

                
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
    model_options = ["ft:gpt-3.5-turbo-1106:personal:v3:8xxaj6yT", "gpt-4-0125-preview"]
    selected_model = st.selectbox("Select the model:", model_options)
    user_input = st.text_area("Enter your prompt:", height=150)

    if st.button('Generate Text'):
        if user_input:
            with st.spinner('Generating text... Please wait'):
                # Call the OpenAI API with the provided user prompt and selected model
                completion = client.chat.completions.create(
                  model=selected_model,
                  temperature=0,
                  messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input},
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
    
    