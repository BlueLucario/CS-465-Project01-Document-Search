# syntax=docker/dockerfile:1

FROM python:rc-buster
RUN pip install poetry
WORKDIR /app
COPY . .
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry install && poetry run python3 install_stopwords.py
CMD ["poetry", "run", "flask", "run", "--no-debugger", "--host=0.0.0.0"]
EXPOSE 5000