import streamlit as st

class AppSection:
    def __init__(self) -> None:
        """
        Initializes an instance of the AppSection class.
        """
        pass

    def app_config(self) -> None:
        """
        Configures the Streamlit app settings.
        """
        st.set_page_config(
            page_title="MyResumo",
            page_icon="🧠",
            layout="centered",
            initial_sidebar_state="collapsed"
        )
        with open("Helper/style/project.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def side_info(self) -> None:
        """
        Displays the sidebar information.
        """
        with st.sidebar:
            st.header("👨‍💻 About the Author")
            st.write(
            """
            **DOSSEH Shalom** is a Problem Solver, Fintech enthusiast, coder and innovator. Driven by passion and a love to solve real life problems, he created this app to make job search more interactive and easier.

            Connect, contribute, or just say hi!
            """)

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
            st.write("Made with ♥ in Cotonou, Benin Republic")

    def app_intro(self) -> None:
        """
        Displays the app introduction section.
        """
        st.title("Search Job. :blue[MyRe]:red[sumo] . Get Hired", anchor=False)
        st.write("""
        Are you looking to elevate your resume and capture the attention of your dream employer? **MyResumo** is here to transform your job application process!

        **How does it work?** 🤔
        1. You can watch the video tutorial below to get started.
        2. Hit the :red[Start] button and let the magic unfold.

        ⚠️ **Important:** MyResumo is porweb by :red[Mixtral-8x22b-Instruct model], the first open-source model to achieve GPT-4 level performance on MT Bench, with an impressive context length of over 65,536 tokens.

        Voilà, You're all set! Press the ***:red[Start]*** Button and embark on the journey to craft a resume that's as unique as your professional story. Let's turn your skills and experiences into a masterpiece!
        """)

    def username(self) -> str:
        """
        Displays the username input section.
        """
        st.title('***Enter your Name***')
        st.write("**:red[Must Know]** : In this Section you are asked to enter your name")
        user_name = st.text_input('***Enter your Name***', help='Enter your Name')
        st.info("***:blue[Tip]*** : Your name will be used to name the generated resume under the following format :red[*username_genenated.pdf*]",icon='ℹ️')
        return user_name

    def uploadfile(self) -> str:
        """
        Displays the file upload section.
        """
        st.title('***Upload your Resume***')
        "**:red[Must Know]** : In this Section you are required to upload an already made resume or a pdf file with all necessary informations **:blue[Skills]**, **:blue[Experiences]**, **:blue[Educations]**, **:blue[Projects]**, **:blue[Certifications]**, **:blue[Languages]**, **:blue[etc...]**"
        st.info("***:blue[Tip]*** : If you don't have a [:red[RESUME]](https://drive.google.com/file/d/1TNbjuxwviQE_cqV9dMNfZqXxxMGAGdN1/view?usp=drive_link) you can download the template below and fill out the template below with your informations",icon='ℹ️')
        uploaded_file = st.file_uploader("***Choose a PDF file***", type="pdf")
        return uploaded_file

    def description(self) -> str:
        """
        Displays the job description input section.
        """
        st.title('***Add a Job Description***')
        st.write("**:red[Must Know]** : In this Section you are required to paste the **:blue[job description]** of the job you are applying too")
        with st.expander(":smile: **Good to Know**"):
            st.info("""When entering the job description, be sure to include key details such as required skills, responsibilities, qualifications, 
            and any other relevant information. Providing a comprehensive job description will help tailor your resume more effectively to the position 
            you're applying for. Remember, clarity and specificity in your job description will result in a more targeted and impactful resume. :memo:""")
            
        job_description = st.text_area('***Enter the job description here***', height=300)
        return job_description

    def resume_option(self) -> str:
        """
        Displays the resume tone selection section.
        """
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
        return resume_tone

    def language_opt(self) -> str:
        """
        Displays the language selection section.
        """
        st.title('***Choose a Language***')
        st.write("**:red[Must Know]** : In this Section you are asked to choose a language in which your resume that will be generated")
        st.info('Advice: It is adviced to choose the source language of the resume uploaded', icon="ℹ️")
        language = st.selectbox("Select a Language", ["English", "French"])
        return language

    def resume_temp(self) -> str:
        """
        Displays the resume template selection section.
        """
        st.title('***Choose the a Template Resume***')
        st.write("**:red[Must Know]** : In this Section you should choose the template you want")
        st.write("**:blue[See More]** : Click on the links below to see the templates, [Template 1](https://drive.google.com/file/d/1TNbjuxwviQE_cqV9dMNfZqXxxMGAGdN1/view?usp=sharing) and [Template 2](https://drive.google.com/file/d/1QGlNrMSPW_BYuXGsvK4g_5T85rY9-IYV/view?usp=sharing)")
        resume_template = st.radio("Select a Resume Template", ["Template 1", "Template 2"])
        return resume_template

    def colorpicker(self) -> str:
        """
        Displays the color picker section.
        """
        st.title('***Choose a Color Scheme***')
        st.write("**:red[Must Know]** : In this Section you are asked to choose a color scheme for your resume")
        st.info('Advice: Choose colors that align with your personal brand or the industry you are applying to.', icon="ℹ️")
        color_code = st.color_picker("Choose a Color", "#000000")
        st.write('The current color is', color_code)
        with st.expander(":smile: **Good to Know**"):
            st.write('***:red[Notice]*** : The color selection will be applied to the section headers.')
            st.image('Images/color_picker.png')
        return color_code