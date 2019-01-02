FROM kennethreitz/pipenv as release
ENV PORT '80'
RUN apt install -y wine-stable
COPY . /app
CMD python3 api.py
EXPOSE 80

FROM release as test
ENTRYPOINT ["pytest"]


FROM release
