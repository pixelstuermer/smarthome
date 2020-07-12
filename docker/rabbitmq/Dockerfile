FROM rabbitmq:3.7-management
COPY ./config /etc/rabbitmq
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt
