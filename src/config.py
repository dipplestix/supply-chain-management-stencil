from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np


@dataclass
class Config:
    n_customers: int  # the number of customers
    n_facilities: int  # the number of facilities
    alloc_cost_cf: np.ndarray  # alloc_cost_cf[c][f] is the service cost paid each time customer c is served by facility f
    demand_c: np.ndarray  # demand_c[c] is the demand of customer c
    opening_cost_f: np.ndarray  # opening_cost_f[f] is the opening cost of facility f
    capacity_f: np.ndarray  # capacity_f[f] is the capacity of facility f
    n_max_vehicle_per_facility: int  # maximum number of vehicles to use at an open facility
    truck_dist_limit: float  # total driving distance limit for trucks
    truck_usage_cost: float  # fixed usage cost paid if a truck is used
    distance_cf: np.ndarray  # distance_cf[c][f] is the roundtrip distance between customer c and facility f

    @staticmethod
    def load(f) -> Config:
        """
        Loads a file describing a problem configuration
        """

        def parse_line(line: str, num_type=float) -> list:
            if len(line) == 0:
                return []
            if line[-1] == "\n":
                line = line[:-1]
            return [num_type(c) for c in re.split("\t| ", line) if c != ""]

        values = {}
        with open(f, "r") as f:
            header = f.readline()
            values["n_customers"], values["n_facilities"] = parse_line(header, int)
            values["n_max_vehicle_per_facility"] = values[
                "n_customers"
            ]  # at worst case visit every customer with one vehicle

            data = []
            for line in f.readlines():
                data.extend(parse_line(line))
            data = iter(data)

            values["alloc_cost_cf"] = np.zeros(
                (values["n_customers"], values["n_facilities"])
            )
            for c in range(values["n_customers"]):
                for f in range(values["n_facilities"]):
                    values["alloc_cost_cf"][c, f] = next(data)

            values["demand_c"] = np.zeros((values["n_customers"]))
            for c in range(values["n_customers"]):
                values["demand_c"][c] = next(data)

            values["opening_cost_f"] = np.zeros((values["n_facilities"]))
            for f in range(values["n_facilities"]):
                values["opening_cost_f"][f] = next(data)

            values["capacity_f"] = np.zeros((values["n_facilities"]))
            for f in range(values["n_facilities"]):
                values["capacity_f"][f] = next(data)

            values["truck_dist_limit"] = next(data)
            values["truck_usage_cost"] = next(data)

            values["distance_cf"] = np.zeros(
                (values["n_customers"], values["n_facilities"])
            )
            for c in range(values["n_customers"]):
                for f in range(values["n_facilities"]):
                    values["distance_cf"][c, f] = next(data)
        return Config(**values)
