FROM python:3.9.5-buster
RUN python3 -m venv /venv
RUN . /venv/bin/activate
WORKDIR /demo-app
ENV PYTHONPATH "${PYTHONPATH}:/demo-app"
COPY / ./demo-app
RUN pip install --no-cache-dir -r demo-app/requirements.txt
EXPOSE 8000
EXPOSE 50470
#use "-i <corporate_repo_link>" in above line if needed in your org
CMD ["python", "demo-app/main.py"]
