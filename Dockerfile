
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
RUN pip3 install -r requirements.txt

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

