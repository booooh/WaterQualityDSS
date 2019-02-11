FROM python:3 as base

RUN mkdir /model
COPY w2_exe_linux_par /model/

# use pipenv to install dependencies
RUN pip install pipenv
WORKDIR /app
COPY Pipfile  Pipfile.lock ./

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

# ignore collections warning about deprecation warning, there's nothing we can do about that for now
ENTRYPOINT [ "pytest", "/test", "-W", "ignore::DeprecationWarning" ]

FROM release
