# Golang image to build prom_alertconfig service
FROM golang:1.13-alpine3.11 as go

ENV GO111MODULE on
ENV GOBIN /build/bin
ENV PATH ${PATH}:${GOBIN}
# Use public go modules proxy
ENV GOPROXY https://proxy.golang.org

# Copy go.mod file to cache the downloads
COPY cloud/go/go.mod /gomod/cloud/go/
COPY gateway/go/go.mod /gomod/gateway/go/
COPY lib/go/go.mod /gomod/lib/go/
COPY lib/go/protos/go.mod /gomod/lib/go/protos/
WORKDIR /gomod/cloud/go

RUN go mod download

# Copy magma code
COPY cloud/go/ /go/src/magma/orc8r/cloud/go/
COPY gateway/go/ /go/src/magma/orc8r/gateway/go/
COPY lib/go/ /go/src/magma/orc8r/lib/go/

# Build alertmanager_configurer service
WORKDIR /go/src/magma/orc8r/cloud/go/services/metricsd/prometheus/configmanager/alertmanager/
RUN go build -i -o $GOBIN/alertmanager_configurer

# Build migration CLI
WORKDIR /go/src/magma/orc8r/cloud/go/services/metricsd/prometheus/configmanager/alertmanager/migration
RUN go build -i -o $GOBIN/migration

FROM alpine:3.11

COPY --from=go /build/bin/alertmanager_configurer /bin/alertmanager_configurer
COPY --from=go /build/bin/migration /bin/migration

# Copy config files
COPY cloud/docker/alertmanager-configurer/configs /etc/configs

ENTRYPOINT ["alertmanager_configurer"]
