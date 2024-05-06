# Use the Anaconda base image
FROM continuumio/anaconda3

# Set the working directory in the container
WORKDIR /app

# Install necessary packages using Conda and Pip
RUN conda install -c pytorch faiss-cpu -y && \
    pip install flask numpy pandas

# Copy the application files into the container
COPY ./server.py /app/server.py
COPY ./faiss_indices /app/faiss_indices
COPY ./PMIDs /app/PMIDs

# Set environment variables
ENV FLASK_APP=/app/server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose port 5000 for communication with the Flask app
EXPOSE 5000

# Define the command that runs when the container starts
CMD ["flask", "run"]

# docker run -d --name faiss_cpt -p 5000:5000 faiss:latest