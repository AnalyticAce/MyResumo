from Helper.tools import (
    pdf_to_text, load_lottie, create_prompt, get_pdf_download_link
)
from Helper.toast_message import get_random_toast
from Helper.generate import generate_resume
from Helper.resume import create_pdf
import streamlit as st
import tempfile, os
from streamlit_lottie import st_lottie

API_KEY = os.environ.get('OCTO_AI_TOKEN')

st.set_page_config(
    page_title="MyResumo",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

with open("helper/style/project.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
# load lottie files
lottie_5 = load_lottie("https://lottie.host/d45005f6-3383-4016-825f-f0448df04c74/eSlPEZ9dfK.json")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    if 'first_time' not in st.session_state:
        message, icon = get_random_toast()
        st.toast(message, icon=icon)
        st.session_state.first_time = False

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
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
            st.video("https://youtu.be/yzBr3L2BIto", format="video/mp4", start_time=0)

    submitted = st.button("Start", type="primary")

    if submitted:
        st.session_state.page = 'generate'
        st.rerun()

elif st.session_state.page == 'generate':
    
    st.title('***Enter your Name***')
    st.write("**:red[Must Know]** : In this Section you are asked to enter your name")
    user_name = st.text_input('***Enter your Name***', help='Enter your Name')
    st.info("***:blue[Tip]*** : Your name will be used to name the generated resume under the following format :red[*username_genenated.pdf*]",icon='ℹ️')
    
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

        st.session_state.resume_content = text
        
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
        template_1 = True
        st.success('Your Resume is Successfully Selected')
    else:
        st.info("Template 2 is not available for the moment")
    
    st.divider()
    generation = st.button('***:blue[Generate Yo]:red[ur Resume]***', help='Hover over me!')

    if generation and template_1:
        if 'temp_file' not in locals() or not temp_file:
            st.warning("Please upload a file before generating your resume.", icon='📑')
            st.stop()
        
        if not job_description:
            st.warning("Please enter the job description before generating your resume.", icon='📑')
            st.stop()
        
        with st.progress(0, text="Generating Resume..."):
            resume = pdf_to_text(temp_file.name)
            st.progress(10, text="Parsing Your Resume...")
            template = create_prompt("Utils/prompt.txt")
            st.progress(20, text="Creating Prompt...")
            description = job_description
            st.progress(30, text="Reading Resume informations...")
            tone = resume_tone
            st.progress(60, text="Generating Resume...")
            result = generate_resume(template, resume, description, tone, language, API_KEY)
            st.progress(85, text="Retrieving Generated Resume...")
            if result is not None:
                new_resume = create_pdf(result, f"Data/{user_name.replace(' ', '_').lower()}_generated.pdf", "helper/style/style.css")
                st.progress(90, text="Creating Resume PDF...")
                st.progress(100, text="Done")
                if new_resume:
                    st.success("Resume PDF created successfully! Please click the button below to download your resume.")
                    with open(f"Data/{user_name.replace(' ', '_').lower()}_generated.pdf", "rb") as f:
                        pdf_data = f.read()
                    st.download_button("Download Generated Resume", pdf_data, f"{user_name.replace(' ', '_').lower()}_generated.pdf", False)
                else:
                    st.warning("Failed to generate the resume. Please try again.")
