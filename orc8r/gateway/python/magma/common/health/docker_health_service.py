#!/usr/bin/env python3

"""
Copyright (c) 2016-present, Facebook, Inc.
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. An additional grant
of patent rights can be found in the PATENTS file in the same directory.
"""

from datetime import datetime

import dateutil.parser
import docker
from magma.common.health.health_service import GenericHealthChecker
from magma.common.health.entities import Errors, Version, ServiceHealth


class DockerHealthChecker(GenericHealthChecker):

    def get_error_summary(self, service_names):
        res = {}
        for service_name in service_names:
            client = docker.from_env()
            container = client.containers.get(service_name)

            res[service_name] = Errors(log_level='-', error_count=0)
            for line in container.logs().decode('utf-8').split('\n'):
                if service_name not in line:
                    continue
                # Reset the counter for restart/start
                if 'Starting {}...'.format(service_name) in line:
                    res[service_name].error_count = 0
                elif 'ERROR' in line:
                    res[service_name].error_count += 1
        return res

    def get_magma_services_summary(self):
        services_health_summary = []
        client = docker.from_env()

        for container in client.containers.list():
            service_start_time = dateutil.parser.parse(
                container.attrs['State']['StartedAt']
            )
            current_time = datetime.now(service_start_time.tzinfo)
            time_running = current_time - service_start_time
            services_health_summary.append(ServiceHealth(
                service_name=container.name,
                active_state=container.status,
                sub_state=container.status,
                time_running=str(time_running).split('.', 1)[0],
                errors=self.get_error_summary([container.name])[container.name],
            ))
        return services_health_summary

    def get_magma_version(self):
        client = docker.from_env()
        container = client.containers.get('magmad')

        return Version(version_code=container.attrs['Config']['Image'],
                       last_update_time='-')
