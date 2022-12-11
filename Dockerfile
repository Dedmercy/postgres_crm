FROM postgres:14.5

WORKDIR /

RUN apt-get update && apt-get -y install git build-essential postgresql-server-dev-14

RUN apt-get remove -y git build-essential postgresql-server-dev-14 && \
	apt-get autoremove --purge -y && \
	apt-get clean && \
	apt-get purge

COPY init-db /docker-entrypoint-initdb.d
