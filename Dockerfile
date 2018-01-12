FROM python:3.5
ADD . /
RUN pip install -r requirements.txt  --cache-dir /pip-cache
RUN python -m spacy download en

RUN python -m rasa_nlu.train -c nlu_model_config.json --fixed_model_name current
RUN python -m rasa_core.train -s data/stories.md -d domain.yml -o models/dialouge --epochs 300

EXPOSE 5050           
#CMD ["python", "server.py"]"#
#CMD ["python", "server.py"]
CMD ["python", "customrunner.py"]
