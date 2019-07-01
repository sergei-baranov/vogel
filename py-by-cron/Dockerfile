FROM jupyter/all-spark-notebook
#FROM python

USER root

#http://qaru.site/questions/84319/how-to-run-a-cron-job-inside-a-docker-container
#https://habr.com/ru/company/redmadrobot/blog/305364/

RUN apt-get clean && apt-get update && apt-get install -y cron
#RUN apt-get update && apt-get -y install cron

RUN rm -rf /var/lib/apt/lists/*

COPY dump_postgres_with_spark.py dump_postgres_with_spark.py

# Copy hello-cron file to the cron.d directory
COPY hello-cron /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

# Apply cron job
RUN crontab /etc/cron.d/hello-cron

RUN touch /var/log/cron.log
RUN chmod 0777 /var/log/cron.log

#CMD echo "starting" && echo "continuing" && (cron) \
# && echo "tailing..." && : >> /var/log/cron.log && tail -f /var/log/cron.log

CMD ["/bin/bash", "-c", "touch /var/log/cron.log && cron && tail -f /var/log/cron.log"]
