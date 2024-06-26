# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# This file is autogenerated.
# To change this file you should edit assets/configuration/spec.yaml and then run the following commands:
#     ddev -x validate config -s <INTEGRATION_NAME>
#     ddev -x validate models -s <INTEGRATION_NAME>


def instance_aggregate_last_24_hours():
    return False


def instance_authenticator():
    return 'snowflake'


def instance_client_prefetch_threads():
    return 4


def instance_client_session_keep_alive():
    return False


def instance_database():
    return 'SNOWFLAKE'


def instance_disable_generic_tags():
    return False


def instance_empty_default_hostname():
    return False


def instance_login_timeout():
    return 60


def instance_min_collection_interval():
    return 3600


def instance_only_custom_queries():
    return False


def instance_schema_():
    return 'ACCOUNT_USAGE'


def instance_token_path():
    return '/path/to/token'


def instance_use_global_custom_queries():
    return 'true'
