# Use the official Python image as the base image
FROM python:3.14

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies (if you have a requirements.txt file)
RUN pip install -r requirements.txt

# Set the command to run your Python script (replace "your_script.py" with your actual Python file)
CMD ["python", "sp500exporter.py"]