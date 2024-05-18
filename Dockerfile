
### Important Disclaimer

#This Docker image has not been thoroughly tested and is provided solely to facilitate the reproducibility of our work. We cannot guarantee that everything will function as expected and disclaim any responsibility for issues that may arise, including cybersecurity risks or data loss, from using this image.
# Use the official Ubuntu 22.04 LTS as a base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Update and install system packages
RUN apt-get update && \
    apt-get install -y \
    apt \
    curl \
    gcc \
    g++ \
    make \
    python3 \
    python3-pip \
    git \
    docker-ce \
    docker-compose-plugin \
    build-essential

# Install the specific versions of Python packages
RUN pip3 install \
    anaconda==0.0.1.1 \
    annotated-types==0.6.0 \
    anyio==4.3.0 \
    argon2-cffi==23.1.0 \
    attrs==23.2.0 \
    Babel==2.14.0 \
    beautifulsoup4==4.12.3 \
    bleach==6.1.0 \
    click==8.1.7 \
    decorator==5.1.1 \
    elastic-transport==8.13.0 \
    elasticsearch==8.13.0 \
    faiss-cpu==1.8.0 \
    Flask==3.0.3 \
    fsspec==2024.3.1 \
    huggingface-hub==0.22.2 \
    idna==3.3 \
    importlib-metadata==4.6.4 \
    joblib==1.4.0 \
    jsonschema==4.21.1 \
    jupyter==1.0.0 \
    jupyterlab==4.1.8 \
    MarkupSafe==2.1.5 \
    matplotlib==3.8.4 \
    more-itertools==8.10.0 \
    nbconvert==7.16.3 \
    numpy==1.26.4 \
    openai==1.23.3 \
    packaging==24.0 \
    pandas==2.2.2 \
    prompt-toolkit==3.0.43 \
    psutil==5.9.8 \
    pydantic==2.7.1 \
    Pygments==2.17.2 \
    regex==2024.4.16 \
    requests==2.31.0 \
    scikit-learn==1.4.2 \
    scipy==1.13.0 \
    sentence-transformers==2.7.0 \
    six==1.16.0 \
    tqdm==4.66.2 \
    traitlets==5.14.2 \
    transformers==4.40.0 \
    torch==2.2.2 \
    urllib3==1.26.5 \
    Werkzeug==3.0.2

# Clone the specified GitHub repository
RUN git clone https://github.com/slinusc/medical_RAG_system.git

# Set the working directory to the cloned repository
WORKDIR /medical_RAG_system

# Set environment variables
ENV OPENAI_API_KEY=your_openai_api_key
ENV ELASTIC_PASSWORD=your_elastic_password

# Run any additional setup or initialization scripts if needed
# For example: RUN ./setup.sh

# Expose ports if the application runs a web service, e.g., Flask
# EXPOSE 5000

# Set an entrypoint or command if needed, e.g., starting a web server or Jupyter notebook
# ENTRYPOINT ["python3", "app.py"]

# For a more complex setup, you might want to copy scripts, set environment variables, etc.

