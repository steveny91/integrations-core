# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from datadog_checks.dev.utils import get_metadata_metrics

from .. import common
from ..test_e2e_core_metadata import assert_device_metadata
from .utils import (
    assert_common_metrics,
    assert_extend_cisco_cpu_memory,
    assert_extend_generic_bgp4,
    assert_extend_generic_if,
    assert_extend_generic_ip,
    assert_extend_generic_ospf,
    assert_extend_generic_tcp,
    assert_extend_generic_udp,
    create_e2e_core_test_config,
    get_device_ip_from_config,
)

pytestmark = [pytest.mark.e2e, common.py3_plus_only, common.snmp_integration_only]


def test_e2e_profile__cisco_generic(dd_agent_check):
    config = create_e2e_core_test_config('_cisco-generic')
    aggregator = common.dd_agent_check_wrapper(dd_agent_check, config, rate=True)

    ip_address = get_device_ip_from_config(config)
    common_tags = [
        'snmp_profile:cisco-generic',
        'snmp_host:_cisco-generic.device.name',
        'device_namespace:default',
        'snmp_device:' + ip_address,
    ] + []

    # --- TEST EXTENDED METRICS ---
    assert_extend_generic_if(aggregator, common_tags)
    assert_extend_generic_tcp(aggregator, common_tags)
    assert_extend_generic_udp(aggregator, common_tags)
    assert_extend_generic_ospf(aggregator, common_tags)
    assert_extend_generic_bgp4(aggregator, common_tags)
    assert_extend_generic_ip(aggregator, common_tags)
    assert_extend_cisco_cpu_memory(aggregator, common_tags)

    # --- TEST METRICS ---
    assert_common_metrics(aggregator, common_tags)

    tag_rows = [
        ['mem:13'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric('snmp.memory.free', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)

    tag_rows = [
        ['fru:16'],
        ['fru:19'],
        ['fru:20'],
        ['fru:23'],
        ['fru:30'],
        ['fru:4'],
        ['fru:5'],
        ['fru:6'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric('snmp.cefcFRUCurrent', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)
        aggregator.assert_metric(
            'snmp.cefcFRUPowerAdminStatus', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )
        aggregator.assert_metric(
            'snmp.cefcFRUPowerOperStatus', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )

    tag_rows = [
        ['cpu:712'],
        ['cpu:25166'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric('snmp.cpmCPUMemoryFree', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)
        aggregator.assert_metric('snmp.cpmCPUMemoryUsed', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)
        aggregator.assert_metric('snmp.cpmCPUTotal1minRev', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)
        aggregator.assert_metric(
            'snmp.cpmCPUTotalMonIntervalValue', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )

    aggregator.assert_metric('snmp.cieIfResetCount', metric_type=aggregator.COUNT, tags=common_tags)

    tag_rows = [
        ['temp_index:15', 'temp_state:6'],
        ['temp_index:20', 'temp_state:2'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric(
            'snmp.ciscoEnvMonTemperatureStatusValue', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )

    tag_rows = [
        ['power_source:2', 'power_status_descr:kept Jaded oxen Jaded their'],
        ['power_source:5', 'power_status_descr:their'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric(
            'snmp.ciscoEnvMonSupplyState', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )

    tag_rows = [
        ['cisco_env_mon_supply_state:critical', 'power_source:5', 'power_status_descr:their'],
        ['cisco_env_mon_supply_state:shutdown', 'power_source:2', 'power_status_descr:kept Jaded oxen Jaded their'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric(
            'snmp.ciscoEnvMonSupplyStatus', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )

    tag_rows = [
        ['fan_status_index:11'],
        ['fan_status_index:16'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric('snmp.ciscoEnvMonFanState', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)

    aggregator.assert_metric('snmp.cswStackPortOperStatus', metric_type=aggregator.GAUGE, tags=common_tags)

    tag_rows = [
        ['mac_addr:0x111111111111'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric('snmp.cswSwitchState', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)

    tag_rows = [
        ['fru:21'],
        ['fru:23'],
        ['fru:25'],
        ['fru:27'],
        ['fru:29'],
        ['fru:30'],
        ['fru:7'],
        ['fru:9'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric('snmp.cefcFanTrayOperStatus', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)

    tag_rows = [
        ['mem_pool_name:but their kept quaintly driving'],
        ['mem_pool_name:zombies kept their oxen'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric('snmp.ciscoMemoryPoolFree', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)
        aggregator.assert_metric(
            'snmp.ciscoMemoryPoolLargestFree', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )

    aggregator.assert_metric('snmp.ciscoMemoryPoolUsed', metric_type=aggregator.GAUGE, tags=common_tags)

    tag_rows = [
        ['connection_type:5'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric(
            'snmp.cfwConnectionStatCount', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )

    tag_rows = [
        ['hardware_desc:but acted quaintly their', 'hardware_type:8'],
        ['hardware_desc:zombies kept forward acted their forward', 'hardware_type:2'],
        ['hardware_desc:zombies oxen but', 'hardware_type:7'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric(
            'snmp.cfwHardwareStatusValue', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )

    tag_rows = [
        ['chassis_switch_id:17174'],
        ['chassis_switch_id:27415'],
        ['chassis_switch_id:41972'],
        ['chassis_switch_id:49126'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric('snmp.cvsChassisUpTime', metric_type=aggregator.GAUGE, tags=common_tags + tag_row)

    tag_rows = [
        ['rtt_index:2'],
        ['rtt_index:5'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric(
            'snmp.rttMonLatestRttOperCompletionTime', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )
        aggregator.assert_metric(
            'snmp.rttMonLatestRttOperSense', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )

    tag_rows = [
        ['rtt_index:26', 'rtt_state:5'],
        ['rtt_index:30', 'rtt_state:2', 'rtt_type:4'],
    ]
    for tag_row in tag_rows:
        aggregator.assert_metric(
            'snmp.rttMonCtrlOperTimeoutOccurred', metric_type=aggregator.GAUGE, tags=common_tags + tag_row
        )

    # --- TEST METADATA ---
    device = {
        'description': '_cisco-generic Device Description',
        'id': 'default:' + ip_address,
        'id_tags': ['device_namespace:default', 'snmp_device:' + ip_address],
        'ip_address': '' + ip_address,
        'name': '_cisco-generic.device.name',
        'profile': 'cisco-generic',
        'status': 1,
        'sys_object_id': '1.2.3.1005',
        'vendor': 'cisco',
    }
    device['tags'] = common_tags
    assert_device_metadata(aggregator, device)

    # --- CHECK COVERAGE ---
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())