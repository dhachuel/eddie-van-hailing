# Use an official Python runtime as a parent image
FROM pypy:3-onbuild

# Set the working directory to /app
WORKDIR /eddie

# Copy the current directory contents into the container at /app
ADD . /eddie

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME venv

# Run app.py when the container launches
CMD [ "gunicorn -b 0.0.0.0:8000", "eddie.app:api" ]