# Base image selection
FROM python:3.11.7-bookworm

# Set working directory in container
WORKDIR /app

# Set up networking to container
EXPOSE 8501

# Copy local files to the container location
COPY ./documentation-helper .

# Set up environment
RUN mkdir /app/langchain-docs
RUN apt update && apt install -y wget
RUN pip install pipenv
# Download langchain documentation
RUN wget -r -A.html -P ./langchain-docs https://api.python.langchain.com/en/latest/index.html

# Set up dependencies for the documentation helper flask server
RUN pipenv --python /usr/local/bin/python
RUN pipenv install

# Upload langchain docs to Pinecone
RUN pipenv python setup_ingestion.py

# Container start command
CMD [ "pipenv", "run", "streamlit", "run", "app.py" ]
