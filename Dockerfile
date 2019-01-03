FROM python:3 as release

# use pipenv to install dependencies
RUN pip install pipenv
WORKDIR /app
COPY Pipfile  Pipfile.lock ./
RUN pipenv install --deploy --system

# expose necessary port
ENV PORT '80'
EXPOSE ${PORT}

# define entrypoint
ENTRYPOINT ["python3",  "src/api.py"]

# copy the contents of the app
COPY src/ /app/src/

FROM release as test

# install dev dependencies as well
RUN pipenv install -d --system
ENV PYTHONPATH=/app/src
COPY test/ /test/
ENTRYPOINT [ "pytest", "/test" ]



FROM release
