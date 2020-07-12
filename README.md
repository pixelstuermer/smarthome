# Smarthome

Side project to monitor the home.

## TL;DR

Tbd.

## About

Tbd.

## Features

Tbd.

## Components

This monorepo features all the required components of the smarthome side project.
It furthermore follows the [twelve factors microservice approach](https://12factor.net) and is therefore divided into the following sub projects, each of them being single deployment units:

- The [IoT Components](iot) which provide the sensor data
- The [Backing Services](services) to route and store the data
- The [Backend Components](backend) which have the logic to receive and provide the data
- The [Frontend Components](frontend) to display the data

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

- Follow the description of the [official documentation](https://www.rabbitmq.com/access-control.html#user-management) to set up users and passwords using the `rabbitmqctl` CLI
- The hashed passwords can then be found inside the RabbitMQ container
  - Use `docker exec -it rabbitmq /bin/bash` to have an interactive bash shell on the container
  - Then run `cat /etc/rabbitmq/definitions.json` to show the created users and hashed passwords
  - Copy the content of the `definitions.json` of the container into the `definitions.json` of this project

The `build.sh` shell script can then simply be executed to build the Docker image from the underlying `Dockerfile`.
And the `run.sh` script finally starts a Docker container for the RabbitMQ message broker and publishes the required ports `1883` (MQTT) and `15672` (management web UI).

Setting up the PostgreSQL Docker container follows almost the same steps, although the setup of the users and passwords is different:

- To define the password of the default `postgres` user, simply set the `POSTGRES_PASSWORD` environment variable with the respective password on your host system
- To set up other users and hashed passwords, the `V0.0.1__setup.sql` must be adopted
  - The `CREATE ROLE` SQL command sets up users with defined passwords
  - For the sake of security, the passwords in this repository are MD5-hashed

The process with the `build.sh` and `run.sh` is the same as already described above.
When starting the PostgreSQL Docker container, the port `5432` gets published.

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

- Official RabbitMQ Docker [documentation](https://hub.docker.com/_/rabbitmq    )
- Official PostgreSQL Docker [documentation](https://hub.docker.com/_/postgres)

## License

[MIT](LICENSE)
