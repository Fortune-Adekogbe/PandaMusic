import os
import streamlit as st
from kafka import KafkaProducer


def produce(file_path, topic):
    try:
        print("Creates a Producer instance and send message...", end="")
        producer = KafkaProducer(bootstrap_servers='127.0.0.1:19092')#, api_version=(2, 0, 2))

        producer.send(topic, value=file_path.encode())

        # Ensure all messages have been sent
        producer.flush()
        print("Done.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


st.title('PandaMusic File Uploader')

uploaded_file = st.file_uploader("Choose an audio file (wav)", type=['wav'])

if uploaded_file is not None:
    try:
        dir_path = 'filestore'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(os.path.join(dir_path, uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success("Saved File")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    if produce(f"filestore/{uploaded_file.name}", topic='music_ingested'):
        st.success("Sent file path to Kafka")
    else:
        st.error("Failed to send file path to Kafka")
