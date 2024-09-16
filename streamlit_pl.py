import streamlit as st
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse


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


if proceed == True:
    print("Clave exitosa")

    # Twilio Client
    twilio_auth_token = st.secrets['TWILIO_AUTH_TOKEN']
    twilio_account_sid = st.secrets['TWILIO_ACCOUNT_SID']

    client = Client(twilio_account_sid, twilio_auth_token)
    
    if client:
        print("Twilio client exitoso.")

    st.header("Enviar Entrevista vía WhatsApp")

    with st.form("envio_entrevista"):

        phone_number = st.text_input("Número de Teléfono (con código de país)", placeholder="+34123456789")
        #phone_number = '+5491161966992'
        #phone_number = '+5491141603674'

        body = st.text_area("Mensaje de la Entrevista", "Hola, soy Vecinal, tienes unos minutos para responder algunas preguntas?")

        submit = st.form_submit_button("Enviar Entrevista")

        if submit:
            message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=body,
            to=f'whatsapp:{phone_number}'
            )

            print(message.sid)



# Stream the response to the app using `st.write_stream`.
#st.write_stream()