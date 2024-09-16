import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader


# Show title and description.
st.title("📄 NefroBot - DevMode")
st.write(
    "Cargue un documento y GPT-4o-mini responderá! "
)

proceed = False
password = st.text_input("App Password", type="password")

if not password:
    st.info("Por favor, ingrese la clave de la aplicación.", icon="🗝️")
else:
    if password != st.secrets["app_password"]:
        st.info("La clave provista es incorrecta.", icon="🗝️")
    else: 
        proceed = True


if proceed == True:

    # Get the the OpenAI api key from secrets
    openai_api_key = st.secrets["openai_api_key"]

    if not openai_api_key:
        st.info("The app has not OpenAI api key.", icon="🗝️")
    else: 
        # Create an OpenAI client.
        client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Cargue un documento (.pdf)", type=("pdf")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Ahora realice una consulta sobre su documento!",
        placeholder="Por favor, resuma el contenido",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        #document = uploaded_file.read().decode()

        pdf_reader = PdfReader(uploaded_file)
        document_text = ""
        for page in pdf_reader.pages:
            document_text += page.extract_text() or ""


        messages = [
            {
                "role": "system",
                "content": """Eres un experto en nefrología pediátrica, entrenado para responder preguntas de médicos y estudiantes sobre publicaciones y consensos.
                IMPORTANTE: Tus respuestas deben estar justificadas, por lo que deberías citar entre paréntesis la página y el fragmento de texto al que haces referencia cuando respondes
                """
            },

            {
                "role": "user",
                "content": f"Aquí tiene el contenido del documento: {document_text} \n\n---\n\n La pregunta es la siguiente: {question}"
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.05,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)