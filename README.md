# Smarthome

Side project to monitor the home.

## TL;DR

Tbd.

## About

Tbd.

## Features

Tbd.

## Components

Tbd.

### IoT Components

Tbd.

#### Requirements

Tbd.

#### Setup

Tbd.

### Backing Services

RabbitMQ is used as a message broker middleware to transmit data from the IoT components to the backend.
The MQTT plugin is additionally utilized since the MQTT protocol is more lightweight than AMQP.
And a PostgreSQL database is used to store the data.

#### Requirements

The backing services (RabbitMQ and PostgreSQL) in this project are set up using Docker.
Nevertheless, any other form of provisioning is possible.

#### Setup

To set up the RabbitMQ Docker container, the following preparations must be made:

- Follow the description of the [official documentation](https://www.rabbitmq.com/access-control.html#user-management) to set up users and passwords using the `rabbitmqctl` CLI tool
- The hashed passwords can then be found inside the RabbitMQ container
  - Use `docker exec -it rabbitmq /bin/bash` to have an interactive bash shell on the container
  - Then run `cat /etc/rabbitmq/definitions.json` to show the created users and hashed passwords
  - Copy the content of the `definitions.json` of the container into the `definitions.json` of this project

The `build.sh` shell script can then simply be executed to build the Docker image from the underlying `Dockerfile`.
And the `run.sh` script finally starts a Docker container for the RabbitMQ message broker and publishes the required ports `1883` (MQTT) and `15672` (management web UI).

### Backend Components

Tbd.

#### Requirements

Tbd.

#### Setup

Tbd.

### Frontend Components

Tbd.

#### Requirements

Tbd.

#### Setup

Tbd.

## Credits And Related

Tbd.

## License

[MIT](LICENSE).
