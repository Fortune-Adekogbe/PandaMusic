import os
import boto3
from botocore.exceptions import NoCredentialsError
from kafka import KafkaProducer
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client('s3')

def upload_to_s3(image_path, bucket):
    object_name = image_path.split('/')[1]
    
    try:
        s3_client.upload_file(image_path, bucket, object_name)
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    finally:
        if os.path.isfile(image_path):
            os.remove(image_path[:-3]+'wav')
            os.remove(image_path)
    return object_name

def check_file(key, bucket='panda-spectrogram'):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except Exception as e:
        return False

def upload_and_produce(image_path, topic, bucket):
    producer = KafkaProducer(
        bootstrap_servers='127.0.0.1:19092'
    )
    object_name = upload_to_s3(image_path, bucket)
    if isinstance(object_name, str):
        producer.send(topic, key=bucket.encode(), value=object_name.encode())
        producer.flush()
    
def generate_spectrogram(file_path, image_path):
    y, sr = librosa.load(file_path, duration=10.0) 
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,fmax=8000)
    log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
    plt.figure(figsize=(12,8))
    plt.axis('off')
    librosa.display.specshow(log_spectrogram, sr=sr, x_axis='time', y_axis='mel', fmax=8000)

    plt.savefig(image_path)
    plt.close()
    return image_path