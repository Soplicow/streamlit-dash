# Use an official lightweight Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port Dash runs on (default: 8050)
EXPOSE 8050

# Define the command to run the app
CMD ["python", "app.py"]
