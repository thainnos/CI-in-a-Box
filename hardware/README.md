# Hardware

This section shows the hardware selection of the platform.
It is the first stop in the Getting Started process.
In general the hardware of the platform is built as follows:
 - 2x Server
 - Router
 - Switch
 - Embedded Hardware and/or Edge Devices
 - Mobile Rack Case

Two servers are used so a physically separate nodes for Gitlab, Jenkins, etc.
can be tested in addition to virtualized environments.
A Router is added so a whole separate network with DNS, proper DHCP, NAT, etc. can be done.
A Switch is needed for obvious reasons.
Embedded Hardware is added for testing the hardware in the CICD environments.
Edge devices are needed to function as the connection node between the Pipeline and the embedded hardware.
The whole thing should be built into a rack case like the ones from Thomann to be mobile and easy-to-use.

## Version 1
The Version 1 (or V1) of the platform is focused on being low-cost and budget friendly.
The idea behind this is to enable smaller businesses to be able to afford it without any issues or bigger cuts in budgeting.
Price target for the platform is 5000€ which at the time of development could be reached.
The embedded hardware (especially the mid and low level) can be skipped while ordering or changed depending to the custom needs.

|            Category            | Amount | Article                                              | Price per |                    Notes                    |
| :----------------------------: | -----: | ---------------------------------------------------- | --------: | :-----------------------------------------: |
|             Server             |     2x | Supermicro 2U 523L-505B Intel Xeon Single CPU E-2000 |  1214.05€ | Intel Xeon E-2226G, 2x 16GB (ECC DDR4 2666) |
|             Switch             |     1x | TP-Link TL-SG3428                                    |   129.90€ |                                             |
|             Router             |     1x | PC Engines APU.2E4 Board                             |   200.00€ |                                             |
|           Rack Case            |     1x | Thon Triple Door Live Rack 10U 45 RA                 |   279.00€ |                                             |
| Embedded Hardware - High Level |     2x | Raspberry Pi 4 Model B 4GB                           |    60.00€ |                                             |
| Embedded Hardware - Mid Level  |     1x | STM NUCLEO-F439ZI                                    |    22.95€ |                                             |
|                                |     1x | STM B-L475E-IOT01A2                                  |    49.70€ |                                             |
|                                |     2x | STM NUCLEO-F103RB                                    |    10.76€ |                                             |
| Embedded Hardware - Low Level  |     2x | ESP32 DevKitC-32D                                    |     8.47€ |                                             |
|                                |     2x | ESP32-S2 Saola-1R                                    |     6.78€ |                                             |
|                                |     1x | ESP32 Ethernet-Kit VE                                |    46.59€ |                                             |
|                                |     1x | Raspberry Pi Pico RP2040                             |     2.95€ |                                             |
|             Cable              |     4x | Cat.6a Ultra Flex Patch Cable 0.25m                  |     4.75€ |                                             |
|                                |     6x | Cat.6a Ultra Flex Patch Cable 0.5m                   |     5.00€ |                                             |
|                                |     4x | Cat.6a Ultra Flex Patch Cable 1m                     |     6.50€ |                                             |
|                                |     1x | Cat.6a Ultra Flex Patch Cable 2m                     |     7.95€ |                                             |
|       Power Distribution       |     1x | Intellinet 19" 1U 8 Socket PDU                       |    20.27€ |                                             |
|                                |     2x | Anker PowerPort 6 (6xPort USB Charger)               |    32.99€ |                                             |
|                                |        |                                                      |           |                                             |
|                                |        | Total:                                               |  3500.41€ |                                             |

Prices are from July 2021 and may be different now.
The Mid and Low Level Embedded Hardware can be skipped depending on personal preference and needs.

## Version 2
The Version 2 (or V2) of the platform is aimed to have more performance, be more user friendly and work as a workshop platform.
The servers will be self-built, since they need to be higher performing while still being short depth and silent.
A Raspberry Pi Rackmount with PoE and SSD storage will be used for more convenient usage and better stability.

|      Category      | Amount | Article                                                  | Price per | Price total |                                                                        Notes                                                                        |
| :----------------: | -----: | -------------------------------------------------------- | --------: | ----------: | :-------------------------------------------------------------------------------------------------------------------------------------------------: |
|       Server       |     2x | Sliger CX3152A Short Depth 3U Case                       |   224.33€ |     448.66€ |                                  360mm AiO Support, [Link](https://www.sliger.com/products/rackmount/3u/cx3152a/)                                   |
|                    |     2x | Supermicro H11SSL-i Mainboard                            |   427,71€ |     855.43€ |                                         [Link](https://www.supermicro.com/en/products/motherboard/H11SSL-i)                                         |
|                    |     2x | AMD EPYC 7302P                                           |   727.73€ |    1455.48€ |                                             [Link](https://www.amd.com/de/products/cpu/amd-epyc-7302p)                                              |
|                    |     2x | 2TB WD Red SSD SN700 NVMe                                |   170.57€ |     341.14€ |                          [Link](https://www.westerndigital.com/products/internal-drives/wd-red-sn700-nvme-ssd#WDS200T1R0C)                          |
|                    |     2x | be quiet! Straight Power 11 650W PSU                     |   103.23€ |     206.45€ |                                                 [Link](https://www.bequiet.com/de/powersupply/1770)                                                 |
|                    |    16x | Mushkin Proline DIMM 32GB, DDR4-3200, CL22-22-22-52, ECC |   117.56€ |    1880.96€ |                      [Link](https://www.poweredbymushkin.com/Home/index.php/catalog/memory/proline/item/1536-mpl4e320nf32g28)                       |
|                    |     2x | Alphacool Eisbaer Pro Aurora 360 CPU AiO                 |   151.25€ |     302.50€ |                                 Supports SP3 Socket, [Link](https://www.alphacool.com/detail/index/sArticle/27124)                                  |
|       Router       |     1x | Zimaboard 432                                            |   155.24€ |     155.24€ |                                                 [Link](https://www.zimaboard.com/zimaboard/product)                                                 |
|       Switch       |     1x | Ubiquiti UniFiSwitch 24, 24x RJ-45, 2x SFP, PoE+, Gen2   |   419.24€ |     419.24€ |                           [Link](https://eu.store.ui.com/collections/unifi-network-routing-switching/products/usw-24-poe)                           |
|     Rack Case      |     1x | Thon Triple Door Live Rack 10U 45                        |   261.34€ |     261.34€ |                                         [Link](https://www.thomann.de/de/thon_tripledoor_liverack_10he.htm)                                         |
|                    |     1x | Thon Top Tray 1U                                         |    15.97€ |      15.97€ |                                               [Link](https://www.thomann.de/de/thon_top_tray_1u.htm)                                                |
|    Edge Devices    |     4x | Raspberry Pi 4 4GB                                       |    68.00€ |     272.00€ |                                        [Link](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)                                         |
|                    |     1x | UCTRONICS Pi Rack Pro                                    |   262.24€ |     262.24€ | [Link](https://www.uctronics.com/raspberry-pi/1u-rack-mount/uctronics-pi-rack-pro-for-raspberry-pi-4b-19-1u-rack-mount-support-for-4-2-5-ssds.html) |
|                    |     4x | TeamGroup T-Force Vulcan G SSD 512GB, SATA               |    27.00€ |     108.00€ |                                            [Link](https://www.teamgroupinc.com/en/product/vulcan-g-ssd)                                             |
|                    |     4x | PoE+ HAT for Raspberry Pi 4                              |    18.40€ |      73.61€ |                                             [Link](https://www.raspberrypi.com/products/poe-plus-hat/)                                              |
|     LAN Cables     |     5x | SlimWire Pro+ STP schwarz 0.15 m                         |     4.40€ |      22.00€ |                        High-Flex Flat Band Cable, [Link](https://slimwire.de/slimwire-pro-stp/12/slimwire-pro?number=A4038)                         |
|                    |     5x | SlimWire Pro+ STP schwarz 0.3 m                          |     4.60€ |      23.00€ |                                      [Link](https://slimwire.de/slimwire-pro-stp/12/slimwire-pro?number=A4200)                                      |
|                    |     6x | SlimWire Pro+ STP schwarz 0.5 m                          |     4.90€ |      29.40€ |                                      [Link](https://slimwire.de/slimwire-pro-stp/12/slimwire-pro?number=A3565)                                      |
|                    |     4x | SlimWire Pro+ STP schwarz 1.0 m                          |     5.80€ |      23.20€ |                                      [Link](https://slimwire.de/slimwire-pro-stp/12/slimwire-pro?number=A3566)                                      |
|                    |     1x | SlimWire Pro+ STP schwarz 2.0 m                          |     7.50€ |       7.50€ |                                      [Link](https://slimwire.de/slimwire-pro-stp/12/slimwire-pro?number=A3567)                                      |
| Power Distribution |     1x | Intellinet 19" 1U Rackmount Aluminium PDU, 8 Sockets     |    16.50€ |      16.50€ |                     [Link](https://intellinetnetwork.de/products/intellinet-de-19-8-fach-steckdosenleiste-schutzkontakt-713986)                     |
|                    |        |                                                          |           |             |                                                                                                                                                     |
|                    |        |                                                          |    Total: |    7179.86€ |                                                                                                                                                     |

All Prices are before taxes and from November 2022 to January 2023, therefore they may be different now.

## What's next?
Once the parts are ordered and the platform assembled, the next step is to set up the automated [infrastructure](../infrastructure/README.md).