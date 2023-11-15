# edge3

## Table of Contents

- [Management](#management)
  - [Management API HTTP](#management-api-http)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Configuration](#internal-vlan-allocation-policy-configuration)
- [IP Security](#ip-security)
  - [IKE policies](#ike-policies)
  - [IPSec profiles](#ipsec-profiles)
  - [Key controller](#key-controller)
  - [IP Security Configuration](#ip-security-configuration)
- [Interfaces](#interfaces)
  - [DPS Interfaces](#dps-interfaces)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
  - [VXLAN Interface](#vxlan-interface)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [Multicast](#multicast)
  - [IP IGMP Snooping](#ip-igmp-snooping)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)
  - [Router Path-selection](#router-path-selection)
- [STUN](#stun)
  - [STUN Client](#stun-client)
  - [STUN Device Configuration](#stun-device-configuration)

## Management

### Management API HTTP

#### Management API HTTP Summary

| HTTP | HTTPS | Default Services |
| ---- | ----- | ---------------- |
| False | True | - |

#### Management API VRF Access

| VRF Name | IPv4 ACL | IPv6 ACL |
| -------- | -------- | -------- |
| MGMT | - | - |

#### Management API HTTP Configuration

```eos
!
management api http-commands
   protocol https
   no shutdown
   !
   vrf MGMT
      no shutdown
```

## Internal VLAN Allocation Policy

### Internal VLAN Allocation Policy Summary

| Policy Allocation | Range Beginning | Range Ending |
| ------------------| --------------- | ------------ |
| ascending | 1006 | 1199 |

### Internal VLAN Allocation Policy Configuration

```eos
!
vlan internal order ascending range 1006 1199
```

## IP Security

### IKE policies

| Policy name | Local ID |
| ----------- | -------- |
| IKEAUTOVPN | 192.168.42.5 |

### IPSec profiles

| Profile name | IKE policy | SA policy | Connection | DPD Interval | DPD Time | DPD action | Mode |
| ------------ | ---------- | ----------| ---------- | ------------ | -------- | ---------- | ---- |
| AUTOVPNTUNNEL | IKEAUTOVPN | SAAUTOVPN | start | - | - | - | transport |

### Key controller

| Profile name |
| ------------ |
| AUTOVPNTUNNEL |

### IP Security Configuration

```eos
!
ip security
   !
   ike policy IKEAUTOVPN
      local-id 192.168.42.5
   !
   sa policy SAAUTOVPN
   !
   profile AUTOVPNTUNNEL
      ike-policy IKEAUTOVPN
      sa-policy SAAUTOVPN
      connection start
      shared-key 7 0112140D481F07
      dpd 10 50 clear
      mode transport
   !
   key controller
      profile AUTOVPNTUNNEL
```

## Interfaces

### DPS Interfaces

#### DPS Interfaces Summary

| Interface | IP address | Shutdown | MTU | Flow tracker(s) | TCP MSS Ceiling |
| --------- | ---------- | -------- | --- | --------------- | --------------- |
| Dps1 | - | - | - |  |  |

#### DPS Interfaces Device Configuration

```eos
!
interface Dps1
```

### Ethernet Interfaces

#### Ethernet Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet3 | WAN_INTERNET | routed | - | dhcp | default | - | False | - | - |
| Ethernet4 | Client LAN Network | routed | - | 192.168.3.1/24 | SE_LAB | - | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet3
   description WAN_INTERNET
   no shutdown
   no switchport
   ip address dhcp
   dhcp client accept default-route
!
interface Ethernet4
   description Client LAN Network
   no shutdown
   no switchport
   vrf SE_LAB
   ip address 192.168.3.1/24
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | EVPN_Overlay_Peering | default | 192.168.42.5/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | EVPN_Overlay_Peering | default | - |


#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description EVPN_Overlay_Peering
   no shutdown
   ip address 192.168.42.5/32
```

### VXLAN Interface

#### VXLAN Interface Summary

| Setting | Value |
| ------- | ----- |
| Source Interface | Loopback0 |
| UDP port | 4789 |

##### VRF to VNI and Multicast Group Mappings

| VRF | VNI | Multicast Group |
| ---- | --- | --------------- |
| SE_LAB | 201 | - |

#### VXLAN Interface Device Configuration

```eos
!
interface Vxlan1
   description edge3_VTEP
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vrf SE_LAB vni 201
```

## Routing

### Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |
| MGMT | False |
| SE_LAB | True |

#### IP Routing Device Configuration

```eos
!
ip routing
no ip routing vrf MGMT
ip routing vrf SE_LAB
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| MGMT | false |
| SE_LAB | false |

### Router BGP

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65000 | 192.168.42.5 |

| BGP Tuning |
| ---------- |
| update wait-install |
| no bgp default ipv4-unicast |
| maximum-paths 4 ecmp 4 |

#### Router BGP Peer Groups

##### PATHFINDERS

| Settings | Value |
| -------- | ----- |
| Address Family | wan |
| Remote AS | 65000 |
| Source | Loopback0 |
| Send community | all |
| Maximum routes | 12000 |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Encapsulation |
| ---------- | -------- | ------------- |
| PATHFINDERS | True | default |

#### Router BGP Path-Selection Address Family

##### Path-Selection Peer Groups

| Peer Group | Activate |
| ---------- | -------- |
| PATHFINDERS | True |

#### Router BGP Device Configuration

```eos
!
router bgp 65000
   router-id 192.168.42.5
   maximum-paths 4 ecmp 4
   update wait-install
   no bgp default ipv4-unicast
   neighbor PATHFINDERS peer group
   neighbor PATHFINDERS remote-as 65000
   neighbor PATHFINDERS update-source Loopback0
   neighbor PATHFINDERS password 7 <removed>
   neighbor PATHFINDERS send-community
   neighbor PATHFINDERS maximum-routes 12000
   !
   address-family evpn
      neighbor PATHFINDERS activate
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-PEERS activate
      no neighbor PATHFINDERS activate
   !
   address-family path-selection
      neighbor PATHFINDERS activate
      neighbor PATHFINDERS additional-paths receive
      neighbor PATHFINDERS additional-paths send any
```

## BFD

### Router BFD

#### Router BFD Multihop Summary

| Interval | Minimum RX | Multiplier |
| -------- | ---------- | ---------- |
| 300 | 300 | 3 |

#### Router BFD Device Configuration

```eos
!
router bfd
   multihop interval 300 min-rx 300 multiplier 3
```

## Multicast

### IP IGMP Snooping

#### IP IGMP Snooping Summary

| IGMP Snooping | Fast Leave | Interface Restart Query | Proxy | Restart Query Interval | Robustness Variable |
| ------------- | ---------- | ----------------------- | ----- | ---------------------- | ------------------- |
| Enabled | - | - | - | - | - |

#### IP IGMP Snooping Device Configuration

```eos
```

## VRF Instances

### VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |
| MGMT | disabled |
| SE_LAB | enabled |

### VRF Instances Device Configuration

```eos
!
vrf instance MGMT
!
vrf instance SE_LAB
```

### Router Path-selection

#### Path Groups

##### Path Group INTERNET

| Setting | Value |
| ------  | ----- |
| Path Group ID | 300 |
| IPSec profile | AUTOVPNTUNNEL |

###### Local Interfaces

| Interface name | Public address | STUN server profile(s) |
| -------------- | -------------- | ---------------------- |
| Ethernet3 | - |  |

###### Dynamic peers settings

| Setting | Value |
| ------  | ----- |
| IP Local | - |
| IPSec | - |

###### Static peers

| Router IP | Name | IPv4 address(es) |
| --------- | ---- | ---------------- |
| 192.168.42.2 | rr2 | 104.197.58.72 |

#### Load-balance policies

| Policy name | Path group(s) |
| ----------- | ------------- |
| LBPOLICY | INTERNET |

#### DPS policies

##### DPS policy dps-policy-default

| Rule ID | Application profile | Load-balance policy |
| ------- | ------------------- | ------------------- |
| Default Match | - | LBPOLICY |

##### DPS policy dps-policy-SE_LAB

| Rule ID | Application profile | Load-balance policy |
| ------- | ------------------- | ------------------- |
| Default Match | - | LBPOLICY |

#### VRFs configuration

| VRF name | DPS policy |
| -------- | ---------- |
| default | dps-policy-default |
| SE_LAB | dps-policy-SE_LAB |

#### Router Path-selection Device Configuration

```eos
!
router path-selection
   !
   path-group INTERNET id 300
      ipsec profile AUTOVPNTUNNEL
      !
      local interface Ethernet3
      !
      peer dynamic
      !
      peer static router-ip 192.168.42.2
         name rr2
         ipv4 address 104.197.58.72
   !
   load-balance policy LBPOLICY
      path-group INTERNET
   !
   policy dps-policy-default
      default-match
         load-balance LBPOLICY
   !
   policy dps-policy-SE_LAB
      default-match
         load-balance LBPOLICY
   !
   vrf default
      path-selection-policy dps-policy-default
   !
   vrf SE_LAB
      path-selection-policy dps-policy-SE_LAB
```

## STUN

### STUN Client

#### Server Profiles

| Server Profile | IP address |
| -------------- | ---------- |
| rr2-INTERNET | 104.197.58.72 |

### STUN Device Configuration

```eos
!
stun
   client
      server-profile rr2-INTERNET
         ip address 104.197.58.72
```
