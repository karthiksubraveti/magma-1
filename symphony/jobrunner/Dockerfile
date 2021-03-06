# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# Multi stage application builder
FROM golang:1.14-alpine AS builder

# Install build tools
RUN apk add --no-cache git gcc musl-dev

# Download dependencies
WORKDIR /src/symphony
COPY go.* ./
RUN go mod download

# Copy shared components
COPY pkg /src/symphony/pkg
COPY graph /src/symphony/graph

# Build services
WORKDIR /src/symphony/jobrunner
COPY jobrunner .
RUN mkdir /build && go build -o /build ./cmd/...

# Create deployable image
FROM alpine

# Install runtime requirements
RUN apk add --no-cache musl curl

# Copy artifacts from builder
COPY --from=builder /build/* /bin/

ENTRYPOINT ["/bin/cmd"]
