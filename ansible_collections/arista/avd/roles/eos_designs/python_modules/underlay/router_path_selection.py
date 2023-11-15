# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.utils import get

from .utils import UtilsMixin


class RouterPathSelectionMixin(UtilsMixin):
    """
    Mixin Class used to generate structured config for one key.
    Class should only be used as Mixin to a AvdStructuredConfig class
    """

    @cached_property
    def router_path_selection(self) -> dict | None:
        """
        Return structured config for router path-selection (DPS)
        """

        if not self.shared_utils.wan:
            return None

        router_path_selection = {}

        if self.shared_utils.type in ["pathfinders", "rr"]:
            router_path_selection["peer_dynamic_source"] = "stun"

        path_groups = []
        for transport in get(self.shared_utils.switch_data_combined, "transports", []):
            path_groups.append(
                {
                    "name": transport.get("name"),
                    "id": self._get_transport_id(transport),
                    # TODO CHANGE NEXT
                    "ipsec_profile": "AUTOVPNTUNNEL",
                    # TODO handle multiple interfaces
                    "local_interfaces": self._get_local_interfaces(transport),
                    "dynamic_peers": self._get_dynamic_peers(transport),
                    "static_peers": self._get_static_peers(transport),
                }
            )

        router_path_selection["path_groups"] = path_groups

        # TODO Load balance policy - for now one policy with all path_groups
        load_balance_policies = []
        load_balance_policies.append({"name": "LBPOLICY", "path_groups": [pg.get("name") for pg in path_groups]})
        router_path_selection["load_balance_policies"] = load_balance_policies

        # TODO DPS policies - for now adding one default one - MAYBE NEED TO REMOVED
        policies = [{"name": "dps-policy-default", "default_match": {"load_balance": "LBPOLICY"}}]
        router_path_selection["policies"] = policies

        # TODO - Adding default VRF here - check if it makes sense later
        vrfs = [{"name": "default", "path_selection_policy": "dps-policy-default"}]
        router_path_selection["vrfs"] = vrfs

        # TODO maybe strip empty
        return router_path_selection

    def _get_transport_id(self, transport: dict) -> int:
        """
        TODO - implement stuff from Venkit
        """
        # HACK
        if transport["name"] == "MPLS-1":
            return 100
        if transport["name"] == "MPLS-2":
            return 200
        if transport["name"] == "INTERNET":
            return 300
        return 666

    def _get_local_interfaces(self, transport: dict) -> dict | None:
        """
        TODO - handle multiples interfaces ?
        TODO - add STUN where required
        """
        return [{"name": transport.get("interface")}]

    def _get_dynamic_peers(self, transport: dict) -> dict | None:
        """
        TODO generate peer dynamic config
        """
        return None

    def _get_static_peers(self, transport: dict) -> dict | None:
        """
        TODO generate peer static config
        """
        return None
