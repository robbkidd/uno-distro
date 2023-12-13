# Copyright Honeycomb
# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from opentelemetry.environment_variables import (
  OTEL_METRICS_EXPORTER,
  OTEL_TRACES_EXPORTER,
)
from opentelemetry.instrumentation.distro import BaseDistro
from opentelemetry.sdk._configuration import _OTelSDKConfigurator
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPERIMENTAL_RESOURCE_DETECTORS
from opentelemetry.sdk.resources import ResourceDetector, Resource

class UnoResourceDetector(ResourceDetector):
  def detect(self) -> "Resource":
    from uno import version
    return Resource({
        "telemetry.auto.name": "uno-distro",
        # sadly, the upstream distro's version wins for this key in transmitted telemetry 🤔
        "telemetry.auto.version": version.__version__,
    })

class UnoConfigurator(_OTelSDKConfigurator):
  pass

class UnoDistro(BaseDistro):
  """
  The Uno provided Distro configures a default set of
  configuration out of the box.
  """

	# Configure OpenTelemetry by manipulating the environment variables used by
  # the SDK auto-configuration.
  #
  # pylint: disable=no-self-use
  def _configure(self, **kwargs):

    ## CONFIGURE OUTPUT ##

    # enable debug to see data on console instead of sending to an OTLP receiver endpoint
    debug_enabled = os.environ.get("DEBUG", False)
    if debug_enabled:
      os.environ.setdefault(OTEL_TRACES_EXPORTER, "console")
    else:
      os.environ.setdefault(OTEL_EXPORTER_OTLP_PROTOCOL, "grpc")
      os.environ.setdefault(OTEL_TRACES_EXPORTER, "otlp")
      os.environ.setdefault(OTEL_METRICS_EXPORTER, "otlp")
      os.environ.setdefault(OTEL_EXPORTER_OTLP_ENDPOINT, "https://uno.custom.collector:443")

    ## CONFIGURE RESOURCE DETECTORS ##

    # accept detector that may be provided in the runtime environment
    otel_experimental_resource_detectors = os.environ.get(
      OTEL_EXPERIMENTAL_RESOURCE_DETECTORS, "otel,process,uno"
    ).split(",")

    # add the distro-desired detectors to any list that may have been provided
    for detector in ["process", "uno"]:
      if detector not in otel_experimental_resource_detectors:
        otel_experimental_resource_detectors.append(detector)

    # ensure our desired detectors are set in the environment
    os.environ[OTEL_EXPERIMENTAL_RESOURCE_DETECTORS] = ",".join(otel_experimental_resource_detectors)


