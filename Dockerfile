FROM kennethreitz/pipenv
ENV PORT '80'
RUN apt install -y wine-stable
COPY . /app
CMD python3 api.py
EXPOSE 80