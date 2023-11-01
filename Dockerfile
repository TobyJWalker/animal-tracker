
# Choose base image as python
FROM python:3.11

# install pipenv
RUN pip install pipenv

# copy to /app and set working directory
COPY . /app
WORKDIR /app

# Install dependencies
RUN pipenv install --system --deploy

# Set environment variables
ENV APP_ENV=production

# Expose port 7474
EXPOSE 7474

CMD ["python", "app.py"]