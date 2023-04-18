FROM python:3.7.3-slim
COPY ./ /app
WORKDIR /app
RUN pip install iris/intersystems_irispython-3.2.0-py3-none-any.whl
RUN pip install flask
RUN pip install flask_material
RUN pip install nltk==3.5
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]