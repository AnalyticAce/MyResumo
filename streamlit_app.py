from helper.toast_message import get_random_toast
from helper.tools import get_file_data, pdf_to_text, load_lottie
from helper.openai_utils import *
# from helper.html_pdf import *
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

with open("Templates/style/project.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
# load lottie files
# lottie_1 = load_lottie("https://lottie.host/dfe3e0ef-4fb3-4798-9f82-fc99376d49c4/gPgz773jxN.json")
# lottie_2 = load_lottie("https://lottie.host/a3af983f-6f84-4ad1-a8e7-f005d779faba/DPrE5rtPvz.json")
# lottie_3 = load_lottie('https://lottie.host/a3571103-ff5b-453c-9117-d4f441880eb2/4qGZQ5PSek.json')
# lottie_4 = load_lottie('https://lottie.host/0cb6a992-b081-4183-9316-65bd6021a623/ZDEWF6R55F.json')
lottie_5 = load_lottie("https://lottie.host/d45005f6-3383-4016-825f-f0448df04c74/eSlPEZ9dfK.json")
# lottie_6 = load_lottie('https://lottie.host/d7d89f38-1f7f-4554-b08e-944f582f015d/ruDEKuRXKZ.json')
# lottie = [lottie_1, lottie_2, lottie_4, lottie_5]

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    if 'first_time' not in st.session_state:
        message, icon = get_random_toast()
        st.toast(message, icon=icon)
        st.session_state.first_time = False

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        #st_lottie(random.choice(lottie), height=300, key="lottie")
        st_lottie(lottie_5, height=300, key="lottie")
        
    with st.sidebar:
        st.header("👨‍💻 About the Author")
        """
        **DOSSEH Shalom** is a Problem Solver, Fintech enthusiast, coder and innovator. Driven by passion and a love to solve real life problems, he created this app to make job search more interactive and easier.

        Connect, contribute, or just say hi!
        """

        st.divider()
        st.subheader("🔗 Connect with Me", anchor=False)
        st.markdown(
            """
            - 🐙 [Source Code](https://github.com/AnalyticAce/MyResumo)
            - 👔 [Contact me](https://www.linkedin.com/in/shalom-dosseh-4a484a262/)
            - 🍕 [Buy me a Pizza](https://www.buymeacoffee.com/dossehdossB)
            """
        )

        st.divider()
        "Made with ♥ in Cotonou, Benin Republic"

    st.title("Search Job. :blue[MyRe]:red[sumo] . Get Hired", anchor=False)
    """
    Are you looking for a way to make your resume stand out from the crowd ? Do you want to impress your potential employers with your skills and achievements ? If yes, then **MyResumo** is the perfect tool for you!

    **How does it work?** 🤔
    1. Enter your OpenAI API Key.
    2. Press the start button and follow the instructions.

    ⚠️ **Important:** Your OpenAI API KEY must be valid and belong to the :red[GPT 3.5 or 4 model] to move to the generate step.

    Once you've input the your API KEY, voilà ! Dive deep into the generation of your Resume by pressing the ***:red[Start]*** Button and follow the intructions to build your tailored Resume . Let's transform your Experiences & Skills to art! 
    """

    with st.expander("💡 Video Tutorial"):
        with st.spinner("Loading video.."):
            st.video("https://youtu.be/Tt08KmFfIYQ?si=e4iMZrdq16-cTO1z", format="video/mp4", start_time=0)

    with st.form("user_input"):
        OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", placeholder="SK-XXXX", type='password')
        submitted = st.form_submit_button("Start", type="primary")

    if submitted:
        if not OPENAI_API_KEY:
            st.warning("Please fill out the OpenAI API Key to proceed. If you don't have one, you can obtain it [here](https://platform.openai.com/account/api-keys).", icon='🔥')
            st.stop()
        if not is_valid_openai_key(OPENAI_API_KEY):
            st.error("Your API key is invalid. If you don't have one, you can obtain it [here](https://platform.openai.com/account/api-keys).", icon="🚨")
            st.stop()
        
        st.session_state.OPENAI_API_KEY = OPENAI_API_KEY
        
        st.session_state.page = 'generate'
        st.rerun()

elif st.session_state.page == 'generate':
    OPENAI_API_KEY = st.session_state.get('OPENAI_API_KEY')
    
    if not OPENAI_API_KEY:
        st.warning("OpenAI API Key not found. Please enter the key on the home page.", icon="🔥")
        st.stop()

    st.title('***Upload your Resume***')
    
    "**:red[Must Know]** : In this Section you are required to upload an already made resume or a pdf file with all necessary informations **:blue[Skills]**, **:blue[Experiences]**, **:blue[Educations]**, **:blue[Projects]**, **:blue[Certifications]**, **:blue[Languages]**, **:blue[etc...]**"
    
    st.info("***:blue[Tip]*** : If you don't have a [:red[RESUME]](https://drive.google.com/file/d/1TNbjuxwviQE_cqV9dMNfZqXxxMGAGdN1/view?usp=drive_link) you can download the template below and fill out the template below with your informations",icon='ℹ️')
    
    uploaded_file = st.file_uploader("***Choose a PDF file***", type="pdf")
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file_bytes)
        temp_file.close()
        text = pdf_to_text(temp_file.name)
        
        st.success('File Uploaded Successfully')
        os.unlink(temp_file.name)

    st.title('***Add a Job Description***')
    st.write("**:red[Must Know]** : In this Section you are required to paste the **:blue[job description]** of the job you are applying too")
    with st.expander(":smile: **Good to Know**"):
        st.info("""When entering the job description, be sure to include key details such as required skills, responsibilities, qualifications, 
        and any other relevant information. Providing a comprehensive job description will help tailor your resume more effectively to the position 
        you're applying for. Remember, clarity and specificity in your job description will result in a more targeted and impactful resume. :memo:""")
        
    job_description = st.text_area('***Enter the job description here***', height=300)

    st.title('***Choose the Tone of your Resume***')
    st.write("**:red[Must Know]** : In this Section you are asked to choose the tone of the resume that will be generated")
    resume_tone = st.selectbox("Select a Resume Tone", ["Professional", "Creative", "Balanced",  "Expert"])
    if resume_tone == 'Professional':
        st.info("Professional tone is suitable for formal settings where professionalism is emphasized.", icon="ℹ️")
    elif resume_tone == 'Creative':
        st.info("Creative tone allows for showcasing creativity and personality in your resume.", icon="ℹ️")
    elif resume_tone == 'Balanced':
        st.info("Balanced tone strikes a mix between professionalism and creativity, suitable for various industries.", icon="ℹ️")
    elif resume_tone == "Expert":
        st.info("Expert tone is ideal for highlighting specialized expertise and technical skills in your resume.", icon="ℹ️")

    st.title('***Choose a Language***')
    st.write("**:red[Must Know]** : In this Section you are asked to choose a language in which your resume that will be generated")
    st.info('Advice: It is adviced to choose the source language of the resume uploaded', icon="ℹ️")
    language = st.selectbox("Select a Language", ["English", "French"])
    
    st.title('***Choose the a Template Resume***')
    st.write("**:red[Must Know]** : In this Section you should choose the template you want")
    st.write("**:blue[See More]** : Click on the links below to see the templates, [Template 1](https://drive.google.com/file/d/1TNbjuxwviQE_cqV9dMNfZqXxxMGAGdN1/view?usp=sharing) and [Template 2](https://drive.google.com/file/d/1QGlNrMSPW_BYuXGsvK4g_5T85rY9-IYV/view?usp=sharing)")
    resume_template = st.radio("Select a Resume Template", ["Template 1", "Template 2"])
    
    if resume_template == "Template 1":
        pass
    else:
        st.info("Template 2 is not available for the moment")
    
    st.divider()
    generation = st.button('***:blue[Generate Yo]:red[ur Resume]***', help='Hover over me!')

    if generation:
        if 'temp_file' not in locals() or not temp_file:
            st.warning("Please upload a file before generating your resume.", icon='📑')
            st.stop()
        
        if not job_description:
            st.warning("Please enter the job description before generating your resume.", icon='📑')
            st.stop()
        
        with st.status("***:blue[Generating Resume 📑...]***"):
            "**:red[Reading Resume informations 🕵️‍♂️...]**"
            
            resume_content = temp_file.name
            
            "**:blue[Fetching Job Description 📑.]**"
            
            "**:red[Applying Resume Tone  🗣️.]**"
            
            tone = resume_tone
            
            "**:blue[Generating Resume 🔃...]**"
            
            resume_prompt = generate_resume_prompt(resume_content, job_description, tone, OPENAI_API_KEY, language)
            
            "**:red[Resume Generated 🔃...]**"
            st.write(resume_prompt)
        if resume_template == "Template 1":
            st.success('Your Resume is Successfully Selected')
            pass
            #resume_html = template_one_html(resume_prompt)
            #print(resume_html)
            #save_resume = html_to_pdf(resume_html)
            
        else:
            st.info("Template 2 is not available for the moment")

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
