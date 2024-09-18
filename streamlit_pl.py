import streamlit as st
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
import time
import gspread
import pandas as pd

# Show title and description.
st.title("📄 PensamientoLateral - Entrevistador - DevMode")
st.write(
    "Aplicación para enviar una entrevista a través de whatsapp y visualizar sus resultados"
)

# Authentication
proceed = False
password = st.text_input("App Password", type="password")

if not password:
    st.info("Por favor, ingrese la clave de la aplicación.", icon="🗝️")
else:
    if password != st.secrets["pl_password"]:
        st.info("La clave provista es incorrecta.", icon="🗝️")
    else: 
        proceed = True

# Flujo si la Authentication es correcta
if proceed == True:
    print("Autenticación en la App exitosa.")

    # Inicializar Twilio Client
    twilio_auth_token = st.secrets['TWILIO_AUTH_TOKEN']
    twilio_account_sid = st.secrets['TWILIO_ACCOUNT_SID']
    client = Client(twilio_account_sid, twilio_auth_token)
    if client:
        print("Inicialización de Twilio Client exitosa.")


    # Inicializar Gspread Client
    credentials_dict = {
        "type": st.secrets["TYPE"],
        "project_id": st.secrets["PROJECT_ID"],
        "private_key_id": st.secrets["PRIVATE_KEY_ID"],
        "private_key": st.secrets["PRIVATE_KEY"],
        "client_email": st.secrets["CLIENT_EMAIL"],
        "client_id": st.secrets["CLIENT_ID"],
        "auth_uri": st.secrets["AUTH_URI"],
        "token_uri": st.secrets["TOKEN_URI"],
        "auth_provider_x509_cert_url": st.secrets["AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": st.secrets["CLIENT_X509_CERT_URL"]
    }

    gc = gspread.service_account_from_dict(credentials_dict)
    if gc:
        print('Inicialización de Gspread Client exitosa.')


    # Obtener el worksheet que opera como base de datos
    key = "1a7NbCtYgD7okcroJmhV07yB3ZqA_FqzGdcvPWBZGg0E"
    sh = gc.open_by_key(key)
    worksheet = 1
    worksheet = sh.get_worksheet(worksheet)
    if worksheet:
        print("Google Sheet de resultados conectada.")

    # Obtener el worksheet que opera como referencia
    worksheet_2 = 0
    worksheet_2 = sh.get_worksheet(worksheet_2)
    if worksheet_2:
        print("Google Sheet de preguntas de refencia.")

    


    # Preparar el formulario de entrevista
    st.header("Enviar Entrevista vía WhatsApp")

    with st.form("envio_entrevista"):

        # Generar una caja de texto para colocar el número de teléfono
        phone_number = st.text_input("Número de Teléfono (con código de país)", placeholder="+5491161966992")
        #phone_number = '+5491141603674'

        # Generar una caja de texto para iniciar el mensaje
        body = st.text_input("Mensaje de la Entrevista", "Hola, soy Vecinal, un asistente virtual. \nTe escribo porque estoy evaluando los servicios de la Muni en el barrio. ¿Cómo estás?")

        # Crear el botón para el submit del form
        submit = st.form_submit_button("Enviar Entrevista")

        # Al presionar el botón de submit
        if submit:

            # Verificar que el número de teléfono sea adecuado
            if not phone_number.startswith("+") or not phone_number[1:].isdigit():
                st.error("Por favor, ingresa un número de teléfono válido con el código de país.")
            
            # Verificar que exista un mensaje a ser enviado
            elif not body:
                st.error("El mensaje no puede estar vacío.")

            else:

                message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=body,
                to=f'whatsapp:{phone_number}'
                )

                st.info("Mensaje enviado. Verificando estado...", icon="⏳")

                time.sleep(5)

                message_status = client.messages(message.sid).fetch().status

                if message_status == "delivered":
                    st.success("Mensaje recibido por el destinatario, entrevista iniciada.")
                elif message_status in ["sent", "queued"]:
                    st.warning(f"Mensaje enviado pero aún no se ha confirmado la entrega. Estado actual: {message_status}.")
                else:
                    st.error(f"Mensaje no recibido. Estado: {message_status}.")


                print(f"Status del mensaje: {message_status}")


    # Sección para mostrar resultados
    st.header("Resultados de las Entrevistas Enviadas")

    try:

        # Leer los datos de referencia del Google Sheets
        reference = worksheet_2.get_all_records()
        df2 = pd.DataFrame(reference)
        df2 = df2.astype(str)
        st.dataframe(df2)

        # Leer datos de Google Sheets
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        df = df.astype(str)
        st.dataframe(df)


    except Exception as e:
        st.error(f"No se pudo acceder a los datos de entrevistas anteriores. Estado: {str(e)}.")
        st.info("Aún no se han enviado entrevistas o hubo un error al acceder a los datos.")



