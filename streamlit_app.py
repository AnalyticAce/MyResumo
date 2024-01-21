from helper.toast_message import get_random_toast
from helper.tools import get_file_data, pdf_to_text, load_lottie
from helper.openai_utils import *
from helper.html_pdf import *
import streamlit as st
import tempfile, os
import random
import time
from streamlit_lottie import st_lottie


st.set_page_config(
    page_title="MyResumo",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# with open("style.css") as f:
#     st
# load lottie files
# lottie_1 = load_lottie("https://lottie.host/dfe3e0ef-4fb3-4798-9f82-fc99376d49c4/gPgz773jxN.json")
# lottie_2 = load_lottie("https://lottie.host/a3af983f-6f84-4ad1-a8e7-f005d779faba/DPrE5rtPvz.json")
# lottie_3 = load_lottie('https://lottie.host/a3571103-ff5b-453c-9117-d4f441880eb2/4qGZQ5PSek.json')
# lottie_4 = load_lottie('https://lottie.host/0cb6a992-b081-4183-9316-65bd6021a623/ZDEWF6R55F.json')
# lottie_5 = load_lottie("https://lottie.host/d45005f6-3383-4016-825f-f0448df04c74/eSlPEZ9dfK.json")
# lottie_6 = load_lottie('https://lottie.host/d7d89f38-1f7f-4554-b08e-944f582f015d/ruDEKuRXKZ.json')

# lottie = [lottie_1, lottie_2, lottie_4, lottie_5]

# Check if the 'page' key exists in the session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    if 'first_time' not in st.session_state:
        message, icon = get_random_toast()
        st.toast(message, icon=icon)
        st.session_state.first_time = False

    # col1, col2, col3 = st.columns([1,2,1])

    # with col2:
    #     #st_lottie(random.choice(lottie), height=300, key="lottie")
    #     st_lottie(lottie_5, height=300, key="lottie")
        
    with st.sidebar:
        st.header("👨‍💻 About the Author")
        st.write("""
        **DOSSEH Shalom** is a Problem Solver, Fintech enthusiast, coder and innovator. Driven by passion and a love to solve real life problems, he created this app to make job search more interactive and easier.

        Connect, contribute, or just say hi!
        """)

        st.divider()
        st.subheader("🔗 Connect with Me", anchor=False)
        st.markdown(
            """
            - 🐙 [Source Code](https://github.com/Sven-Bo/streamlit-quiztube/)
            - 👔 [LinkedIn](https://www.linkedin.com/in/shalom-dosseh-4a484a262/)
            """
        )

        st.divider()
        st.write("Made with ♥ in Cotonou, Benin Republic")

    st.title("Search Job. :blue[MyRe]:red[sumo]. Get Hired", anchor=False)
    st.write("""
    Are you looking for a way to make your resume stand out from the crowd ? Do you want to impress your potential employers with your skills and achievements ? If yes, then **MyResumo** is the perfect tool for you!

    **How does it work?** 🤔
    1. Enter your OpenAI API Key.
    2. Press the start button and follow the instructions.

    ⚠️ **Important:** Your OpenAI API KEY must be valid and belong to the :red[GPT 3.5 or 4 model] to move to the generate step.

    Once you've input the your API KEY, voilà ! Dive deep into the generation of your Resume by pressing the ***:red[Start]*** Button and follow the intructions to build your tailored Resume . Let's transform your Experiences & Skills to art! 
    """)

    with st.expander("💡 Video Tutorial"):
        with st.spinner("Loading video.."):
            st.video("https://youtu.be/yzBr3L2BIto", format="video/mp4", start_time=0)

    with st.form("user_input"):
        OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", placeholder="SK-XXXX", type='password')
        submitted = st.form_submit_button("Start", type="primary")

    if submitted:
        if not OPENAI_API_KEY:
            st.info("Please fill out the OpenAI API Key to proceed. If you don't have one, you can obtain it [here](https://platform.openai.com/account/api-keys).")
            st.stop()

        st.session_state.OPENAI_API_KEY = OPENAI_API_KEY
        
        # Set the 'page' key to 'generate' and rerun the script
        st.session_state.page = 'generate'
        st.rerun()

# Display the generate page
elif st.session_state.page == 'generate':
    OPENAI_API_KEY = st.session_state.get('OPENAI_API_KEY')
    
    if not OPENAI_API_KEY:
        st.warning("OpenAI API Key not found. Please enter the key on the home page.")
        st.stop()

    st.title('***Upload your Resume***')
    st.write("**:red[Must Know]** : In this Section you are required to upload an already made resume or a pdf file with all necessary informations **:blue[Skills]**, **:blue[Experiences]**, **:blue[Educations]**, **:blue[Projects]**, **:blue[Certifications]**, **:blue[Languages]**, **:blue[etc...]**")
    st.write("***:blue[Tip]*** : If you don't have a resume you can download the template below and fill out the template below with your informations")
    #st.markdown(get_file_data('template.pdf', 'Resume Template'), unsafe_allow_html=True)
    uploaded_file = st.file_uploader("***Choose a PDF file***", type="pdf")
    
    if uploaded_file is not None:
        # Read the file from the UploadedFile object
        file_bytes = uploaded_file.read()
        
        # Create a temporary file and write the contents of the uploaded file to it
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file_bytes)
        temp_file.close()

        # Now you can use the path of the temp_file with your pdf_to_text function
        text = pdf_to_text(temp_file.name)
            
        for tx in text:
            print(tx)
                
        st.success('File Uploaded Successfully')

        os.unlink(temp_file.name)

    
    st.title('***Add a Job Description***')
    st.write("**:red[Must Know]** : In this Section you are required to paste the **:blue[job description]** of the job you are applying too")
    job_description = st.text_area('***Enter the job description here***', height=300)
        
    
    st.title('***Choose the Tone of your Resume***')
    st.write("**:red[Must Know]** : In this Section you are asked to choose the tone of the resume that will be generated")
    resume_tone = st.selectbox("Select a Resume Tone", ["Creative", "Balanced", "Professional", "Expert"])

    st.title('***Choose the Tone of your Resume Template***')
    st.write("**:red[Must Know]** : In this Section you should choose the template you want")
    st.write("**:blue[See More]** : Click on the links below to see the templates, [Template 1](https://drive.google.com/file/d/1TNbjuxwviQE_cqV9dMNfZqXxxMGAGdN1/view?usp=sharing) and [Template 2](https://drive.google.com/file/d/1QGlNrMSPW_BYuXGsvK4g_5T85rY9-IYV/view?usp=sharing)")
    resume_template = st.radio("Select a Resume Template", ["Template 1", "Template 2"])
    
    if resume_template == "Template 1":
        print("hello")
    else:
        st.info("Template 2 is not available for the moment")
    
    st.divider()
    generation = st.button('***:blue[Generate Yo]:red[ur Resume]***', help='Hover over me!')
    
    if generation:
        print('Done')
        st.session_state.page = 'loading'
        st.rerun()
    #if generation:
    #    resume_content = temp_file
    #    tone = resume_tone
    #    resume_prompt = prompt_generate(resume_content, job_description, tone, OPENAI_API_KEY)
    #    if resume_template == "Template 1":
    #        resume_html = template_one_html(resume_prompt)
    #        save_resume = html_to_pdf(resume_html)
    #        st.success('Your Resume is Successfully Generated')
    #    else:
    #        st.info("Template 2 is not available for the moment")
    #"""    
# elif st.session_state.page == 'loading':
    
#     st_lottie(lottie_5, speed=1, key="animation")
#     time.sleep(10)
#     #st_lottie(lottie_6, speed=1, key="done")
#     #time.sleep(3)
#     st.session_state.page = 'done'
#     st.experimental_rerun()

# elif st.session_state.page == 'done':
#     col1, col2, col3 = st.columns([1,2,1])

#     with col1:
#         st_lottie(lottie_6, height=300, speed=1, key="done")
#         file_data = get_file_data('uploaded_file.pdf')
#         st.download_button('Download PDF File', file_data, 'Resume.pdf', 'application/pdf')