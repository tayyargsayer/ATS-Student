import os
import io
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from PyPDF2 import PdfReader
import fitz  # this is pymupdf


st.set_page_config(page_title="ATS Sistemi",
                   page_icon=":robot:",
                   initial_sidebar_state="expanded")

st.header("Uygulama v1")


genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

@st.cache_resource
def get_gemini_response(prompt):
    # Modelin Ayar Kısmı
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.90,
        "top_k": 64,
        "max_output_tokens": 18192,
        "response_mime_type": "text/plain",
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    prompt_token_count = model.count_tokens(prompt)

    response = model.generate_content(prompt)

    st.markdown(response.text)

    response_token_count = model.count_tokens(response.text)

    return response, prompt_token_count, response_token_count


@st.cache_resource
def read_pdf(file):
    pdfReader = PdfReader(file)
    count = len(pdfReader.pages)

    all_page_text = ""

    for i in range(count):  # for i in range (0, count-1) ///  for i in range (len(pdfReader.pages))
        page = pdfReader.pages[i]
        all_page_text += page.extract_text()

    return all_page_text


@st.cache_resource
def read_pdf_2(file_path):
    doc = fitz.open(file_path)
    images = []
    # count = len(doc)
    for i in range(len(doc)):  # for i in range(count)
        page = doc.load_page(i)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images



st.sidebar.header("ATS Sistemimize Hoşgeldiniz")

departman = st.selectbox("Lütfen Hedef Meslek Grubu Seçiniz", ["İnsan Kaynakları",
                                                         "Muhasebe",
                                                         "Yazılım Geliştirici",
                                                         "Satış",
                                                         "Reklamcılık",
                                                         "Pazarlama"])

deneyim_süresi = st.number_input(label="Adayın Toplam Deneyim Süresini belirtisin", min_value=1, max_value=10)

genre = st.sidebar.radio(
    "Döküman uzantınızı seçin!",
    ["PDF", "None PDF File"])

if genre == "PDF":

    yüklenen_pdf_dosyası = st.sidebar.file_uploader("CV Dosyası", type=["pdf"], accept_multiple_files=False)

    if yüklenen_pdf_dosyası is not None:

        on = st.sidebar.toggle("Text Hali")

        if on:
            pdf_text = read_pdf(yüklenen_pdf_dosyası)
            st.sidebar.write(pdf_text)

            prompt = pdf_text + f"""You are an experienced Human Resources Specialist. Staff will be recruited for {departman}. 
                    I want you to review the CV sample in the image and comment

                    You should pay attention to some points when commenting:
                        - Check whether the uploaded text is a CV, if the uploaded text is not a CV, give a warning message saying "Please upload a CV sample".
                        - Since the needs of each department are different, evaluate the compatibility between the specified department and the uploaded CV.
                        - Minimum required experince is must be 5 years. The users'experince time is {deneyim_süresi}year. If it is less then {deneyim_süresi} years, give info about it.
                        - Give me the percentage of  match if the resume matches the job description.
                        - After percentage, highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
                        - Final response should be in Markdown format, style is up to you, i count on you.
                        - Output must be in Turkish, other languages are not acceptable.
                        """

            çalıştır_butonu = st.sidebar.button("Çalıştır", key="text_pdf_button")

            if çalıştır_butonu:
                response, prompt_token_count, response_token_count = get_gemini_response(prompt)

                st.markdown(response.text)




        else:
            with open("temp.pdf", "wb") as f:
                f.write(yüklenen_pdf_dosyası.getbuffer())
            images = read_pdf_2("temp.pdf")
            st.sidebar.image(images[0], caption="Yüklenen Foto")

            prompt = images[0], f"""You are an experienced Human Resources Specialist. Staff will be recruited for {departman}. 
            I want you to review the CV sample in the image and comment
            You should pay attention to some points when commenting:
                - Check whether the uploaded image is a CV, if the uploaded image is not a CV, give a warning message saying "Please upload a CV sample".
                - Since the needs of each department are different, evaluate the compatibility between the specified department and the uploaded CV.
                - Minimum required experince is must be 5 years. The users'experince time is {deneyim_süresi}year. If it is less then {deneyim_süresi} years, give info about it.
                - Give me the percentage of  match if the resume matches the job description.
                - After percentage, highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
                - Final response should be in Markdown format, style is up to you, i count on you.
                - Output must be in Turkish, other languages are not acceptable.

                """

            çalıştır_butonu = st.sidebar.button("Çalıştır", key="görsel_pdf_button")

            if çalıştır_butonu:
                response, prompt_token_count, response_token_count = get_gemini_response(prompt)

                st.markdown(response.text)



else:
    user_image = st.sidebar.file_uploader("CV Fotoğrafı", type=["jpg", "png"], accept_multiple_files=False)
    if user_image is not None:
        st.sidebar.image(user_image, caption="Yüklenen Foto")

        original_image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": user_image.read(),
            }
        ]


        # prompt = original_image_parts[0],f"""
        # Sen, tecrübeli bir İnsan Kaynakları Uzmanısın. {departman} birimine eleman alımı yapılacak. Görseldeki CV örneğini incelemeni ve yorum yapmanı istiyorum.
        # Yorum yaparken bazı noktalara dikkat etmelisin:
        #     - Yüklenen görselin bir CV olup olmadığını kontrol et, eğer yüklenen görsel bir CV değilse "Lütfen CV örneği yükleyin" şeklinde bir uyarı mesajı ver.
        #     - Her departmanın ihtiyaçları farklı olduğu için, belirtilen departman ile yüklenen CV arasındaki uyumu değerlendir.
        # """

        prompt = original_image_parts[0], f"""You are an experienced Human Resources Specialist. Staff will be recruited for {departman}. 
        I want you to review the CV sample in the image and comment
        You should pay attention to some points when commenting:
            - Check whether the uploaded image is a CV, if the uploaded image is not a CV, give a warning message saying "Please upload a CV sample".
            - Since the needs of each department are different, evaluate the compatibility between the specified department and the uploaded CV.
            - Minimum required experince is must be 5 years. The users'experince time is {deneyim_süresi}year. If it is less then {deneyim_süresi} years, give info about it.
            - Give me the percentage of  match if the resume matches the job description.
            - After percentage, highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
            - Final response should be in Markdown format, style is up to you i count on you.

            """

    çalıştır_butonu = st.sidebar.button("Çalıştır")

    if çalıştır_butonu:
        response, prompt_token_count, response_token_count = get_gemini_response(prompt)
        st.write(f"Prompt token count: {prompt_token_count}")
        st.write(f"Response token count: {response_token_count}")

# st.write(f"Seçilen Departman: {departman}")


#   - Minimum required experince is must be 5 years. The users'experince time is {deneyim_süresi}year. If it is less then {deneyim_süresi} years, terminate the evaluation and don't continue next steps.
