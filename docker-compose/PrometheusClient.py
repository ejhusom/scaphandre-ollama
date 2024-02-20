#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect metrics from Prometheus.

Author:
    Erik Johannes Husom

Created:
    2024-02-20

"""
from prometheus_api_client import PrometheusConnect
import datetime

# Prometheus server URL
url = "http://localhost:9090"

# Create a PrometheusConnect instance
prom = PrometheusConnect(url=url, disable_ssl=True)

# Define your query
query = 'scaph_process_power_consumption_microwatts{cmdline=~".*ollama.*"}'

# Define the time range
# Adjust `start_time` and `end_time` as per your requirement
start_time = datetime.datetime.now() - datetime.timedelta(hours=1)  # 1 hour ago
end_time = datetime.datetime.now()

# Fetch metrics over the specified time range
metric_data = prom.get_metric_range_data(
    query=query,
    start_time=start_time,
    end_time=end_time,
    step='60s'  # Adjust the step size as needed
)

# Calculate energy consumption in Joules
# Assuming the power consumption metric is in microwatts, convert it to Watts by dividing by 1e6
# Energy (Joules) = Power (Watts) * Time (Seconds)
energy_consumption_joules = sum(
    [float(data['value'][1]) / 1e6 * 60 for metric in metric_data for data in metric['values']]
)

# Convert energy consumption to Watt-hours for convenience (1 Wh = 3600 J)
energy_consumption_wh = energy_consumption_joules / 3600

print(f"Total energy consumption: {energy_consumption_joules:.2f} Joules ({energy_consumption_wh:.2f} Watt-hours)")



