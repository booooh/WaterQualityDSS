<<<<<<< HEAD
<<<<<<< HEAD
FROM python:3 as base
=======
FROM python:3 as release
>>>>>>> Added unit tests to docker file

# use pipenv to install dependencies
RUN pip install pipenv
WORKDIR /app
COPY Pipfile  Pipfile.lock ./
<<<<<<< HEAD

FROM base as base-with-deps
RUN pipenv install --deploy --system

FROM base as base-with-devel-deps
RUN pipenv install -d --system

FROM base-with-deps as release
# expose necessary port
ENV PORT '80'
EXPOSE ${PORT}

# define entrypoint
ENTRYPOINT ["python3",  "src/api.py"]

# copy the contents of the app
COPY src/ /app/src/

FROM base-with-devel-deps as test
# copy the contents of the app
COPY src/ /app/src/

ENV PYTHONPATH=/app/src
COPY test/ /test/
ENTRYPOINT [ "pytest", "/test" ]
=======
FROM kennethreitz/pipenv as release
=======
RUN pipenv install --deploy --system

# expose necessary port
>>>>>>> Added unit tests to docker file
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


>>>>>>> Update Dockerfile

FROM release
