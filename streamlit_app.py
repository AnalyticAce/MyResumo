from Helper.tools import ToolKit, load_lottie
from Helper.generate import ResumeGenerator
from Helper.resume import create_pdf
from Helper.sections import AppSection
from Helper.vision import Vision
import tempfile, os, streamlit as st
from streamlit_lottie import st_lottie
from dotenv import load_dotenv

def setup():
    load_dotenv()
    API_KEY = os.getenv("OCTO_AI_TOKEN")
    app = AppSection()
    app.app_config()
    tool = ToolKit()
    lottie_5 = load_lottie("https://lottie.host/d45005f6-3383-4016-825f-f0448df04c74/eSlPEZ9dfK.json")
    return API_KEY, app, tool, lottie_5

def handle_home_page(tool : ToolKit, lottie_5: str, app: AppSection):
    if 'first_time' not in st.session_state:
        message, icon = tool.get_random_toast()
        st.toast(message, icon=icon)
        st.session_state.first_time = False

    _, col2, _ = st.columns([1,2,1])

    with col2:
        st_lottie(lottie_5, height=300, key="lottie")
    
    app.side_info()
    app.app_intro()
    # with st.expander("💡 Video Tutorial"):
    #     with st.spinner("Loading video.."):
    #         st.video("https://youtu.be/Tt08KmFfIYQ?si=t0cCNrtydsyHMg3y", format="video/mp4", start_time=0)
    
    submitted = st.button("Start", type="primary")

    if submitted:
        st.session_state.page = 'generate'
        st.rerun()

def handle_generate_page(app: AppSection, API_KEY: str) -> None:
    user_name = app.username()
    uploaded_file = app.uploadfile()

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file_bytes)
        temp_file.close()
        tool = ToolKit()
        vision = Vision(temp_file.name)
        images = vision.pdf_to_image()

        st.session_state.resume_content = images
        
        st.success('File Uploaded Successfully')
        os.unlink(temp_file.name)

    job_description = app.description()
    resume_tone = app.resume_option()
    language = app.language_opt()
    resume_template = app.resume_temp()
    color_code = app.colorpicker()
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
        
        generate_resume(temp_file, images, job_description, resume_tone, language, API_KEY, user_name, vision, tool, color_code)

def generate_resume(temp_file: str, images: str, job_description: str,
        resume_tone: str, language: str, API_KEY: str, user_name: str, 
        vision: str, tool: str, color_code: str) -> None:
    with st.progress(0, text="Generating Resume..."):
        if not temp_file:
            st.warning("Please upload a file before generating your resume.", icon='📑')
            st.stop()

        save_images_name = vision.save_images(images, temp_file.name)
        texts = vision.ocr_image(save_images_name)
        resume = " ".join(texts)
        vision.delete_image(save_images_name)
        st.progress(10, text="Parsing Your Resume...")
        prompt = tool.create_prompt("Utils/test.txt")
        st.progress(20, text="Creating Prompt...")
        description = job_description
        st.progress(30, text="Reading Resume informations...")
        tone = resume_tone
        st.progress(50, text="Generating Resume...")
        gen = ResumeGenerator(API_KEY, description)
        prompt_1 = tool.create_prompt("Utils/keywords.txt")
        key_words = gen.extract_keywords_ai(prompt_1)
        st.progress(65, text="Extract keywords from Job Description...")
        result = gen.generate_resume(prompt, resume,
                tone, language, key_words)
        st.progress(75, text="Retrieving Generated Resume...")
        if result is not None:
            new_resume = create_pdf(result, f"Data/{user_name.replace(' ', '_').lower()}_generated.pdf", color_code)
            st.progress(80, text="Creating Resume PDF...")
            st.progress(100, text="Done")
            if new_resume:
                st.success("Resume PDF created successfully! Please click the button below to download your resume.")
                with open(f"Data/{user_name.replace(' ', '_').lower()}_generated.pdf", "rb") as f:
                    pdf_data = f.read()
                st.download_button("Download Generated Resume", pdf_data, f"{user_name.replace(' ', '_').lower()}_generated.pdf", False)
                os.remove(f"Data/{user_name.replace(' ', '_').lower()}_generated.pdf")
            else:
                st.warning("Failed to generate the resume. Please try again.")

def main() -> None:
    API_KEY, app, tool, lottie_5 = setup()
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if st.session_state.page == 'home':
        handle_home_page(tool, lottie_5, app)
    elif st.session_state.page == 'generate':
        handle_generate_page(app, API_KEY)

if __name__ == "__main__":
    main()