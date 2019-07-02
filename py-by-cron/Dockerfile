FROM jupyter/all-spark-notebook
#FROM python

USER root

#http://qaru.site/questions/84319/how-to-run-a-cron-job-inside-a-docker-container
#https://habr.com/ru/company/redmadrobot/blog/305364/

RUN apt-get clean && apt-get update && apt-get install -y cron

RUN rm -rf /var/lib/apt/lists/*

COPY postgresql-42.2.5.jar postgresql-42.2.5.jar
COPY dump_postgres_with_spark.py dump_postgres_with_spark.py
COPY .cache/pip/http .cache/pip/http

COPY hello-cron /etc/cron.d/hello-cron

RUN chmod 0644 /etc/cron.d/hello-cron

RUN crontab /etc/cron.d/hello-cron

RUN touch /var/log/cron.log
RUN chmod 0777 /var/log/cron.log

#ENV SPARK_HOME /usr/local/spark
ENV SPARK_HOME /opt/conda/lib/python3.7/site-packages/spark

CMD ["/bin/bash", "-c", "chmod -R 0777 /home/jovyan && pip install pyspark && pip install findspark && touch /var/log/cron.log && cron && tail -f /var/log/cron.log"]
