
# data-processing-spark-AWS-S3

This project ingests audio files, generates melspectrograms using Librosa, and uploads the image to AWS S3. The pipeline leverages Kafka for message passing and Spark for data processing. 

## Project Overview

The pipeline follows these steps:

1. An audio file is uploaded via a streamlit interface.
2. The uploaded file is saved to a known directory.
3. A Kafka producer sends a message containing the audio file path to the topic "music_ingested".
4. A Kafka consumer that's running in a while loop ingests the message, reading from the Redpanda Kafka server using Spark in Python.
5. The most recent message is selected and a check is performed to see if the file has been previously processed. If it has, it returns to the Kafka Consumer step, otherwise, it proceeds to the next step.
6. The audio file path is used to generate a melspectrogram using the Librosa library. The melspectrogram is saved to a directory.
7. The path of the melspectrogram image is sent to a function that uploads the image to AWS S3.
8. The image and audio file are deleted from the local system.

## Setup and Installation

### Prerequisites

Ensure you have the following set up:

1. An AWS account
2. Docker Engine version 24.0.2
3. A running instance of Redpanda version 23.1.8
4. Python Interpreter with version 3.11
5. Hadoop version 3.3.5 (with winutils for Windows users)
6. Java version 8

### Installing Dependencies

After cloning the repository, navigate to the project directory and install the necessary Python libraries in a virtual environment using pip:

```bash
python -m venv .venv
pip install -r requirements.txt
```

### Environment Setup

Next, you need to set up your Kafka and Spark environments:

- Start your Redpanda servers. Refer to [the documentation](https://docs.redpanda.com/docs/get-started/quick-start/) on how to do this.
- Ensure that Spark is correctly configured with your Python environment.

### AWS S3 Bucket Setup

Create a bucket in your S3 account named `panda-spectrogram`.

### AWS Environment Variables

Add your AWS Access Key ID, Secret Access Key, default region name to a `.env` file in the project folder.

## Running the Project

To run the project, first run the command below in a terminal:

```bash
streamlit run app.py
```
This opens the application via your browser from which you can upload a WAV audio file. 
Then, run the command below in another terminal:

```bash
python streaming.py
```