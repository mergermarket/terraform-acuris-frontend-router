import os
import json
import pytest


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'infra')

def assert_resource_changes_action(resource_changes, action, length):
    resource_changes_create = [
        value for _, value in resource_changes.items()
        if value.get('change').get('actions') == [action]
    ]
    assert len(resource_changes_create) == length

def assert_resource_changes(testname, resource_changes):
    with open(f'test/modules/fastly-frontend/files/{testname}.json', 'r') as f:
        data = json.load(f)
        i = 0
        for _, value in resource_changes.items():
            assert sorted(data.get('resource_changes')[i]) == sorted(value)
            i=+1

def test_create_fastly_service(plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})
    plan, resources = plan_runner(
        FIXTURES_DIR,
        targets=["module.fastly"],
        domain_name="www.domain.com", 
        backend_address="1.1.1.1", 
        env="ci")

    assert len(resources) == 1
    assert_resource_changes_action(plan.resource_changes,"create", 1)
    assert_resource_changes('create_fastly_service',plan.resource_changes)


def test_create_fastly_service_creates_redirection(plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})
    plan, resources = plan_runner(
        FIXTURES_DIR,
        targets=["module.fastly"],
        domain_name="www.domain.com", 
        backend_address="1.1.1.1",
        bare_redirect_domain_name="domain.com" ,
        env="any")

    assert len(resources) == 2
    assert_resource_changes_action(plan.resource_changes,"create", 2)
    assert_resource_changes('create_fastly_service_creates_redirection',plan.resource_changes)


def test_disable_force_ssl(plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})
    plan, resources = plan_runner(
        FIXTURES_DIR,
        targets=["module.fastly_disable_force_ssl"],
        domain_name="www.domain.com", 
        backend_address="1.1.1.1", 
        force_ssl="false",
        env="ci")

    assert len(resources) == 1
    assert_resource_changes_action(plan.resource_changes,"create", 1)
    assert_resource_changes('disable_force_ssl',plan.resource_changes)

def test_custom_timeouts(plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})
    plan, resources = plan_runner(
        FIXTURES_DIR,
        targets=["module.fastly_custom_timeouts"],
        domain_name="www.domain.com", 
        backend_address="1.1.1.1", 
        connect_timeout="12345",
        first_byte_timeout="54321",
        between_bytes_timeout="31337",
        env="ci")

    assert len(resources) == 1
    assert_resource_changes_action(plan.resource_changes,"create", 1)
    assert_resource_changes('custom_timeouts',plan.resource_changes)

def test_use_ssl(plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})
    plan, resources = plan_runner(
        FIXTURES_DIR,
        targets=["module.fastly_ssl_cert_hostname"],
        domain_name="www.domain.com", 
        backend_address="1.1.1.1", 
        ssl_cert_hostname="test-hostname",
        env="ci")

    assert len(resources) == 1
    assert_resource_changes_action(plan.resource_changes,"create", 1)
    assert_resource_changes('test_use_ssl',plan.resource_changes)

def test_shield_set(plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})
    plan, resources = plan_runner(
        FIXTURES_DIR,
        targets=["module.fastly_set_shield"],
        domain_name="www.domain.com", 
        backend_address="1.1.1.1", 
        shield="test-shield",
        env="ci")

    assert len(resources) == 1
    assert_resource_changes_action(plan.resource_changes,"create", 1)
    assert_resource_changes('shield_set',plan.resource_changes)

def test_custom_surrogate_header(plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})
    plan, resources = plan_runner(
        FIXTURES_DIR,
        targets=["module.fastly_set_surrogate_key"],
        domain_name="www.domain.com", 
        backend_address="1.1.1.1", 
        surrogate_key_name="my-custom-surrogate-key",
        env="ci")

    assert len(resources) == 1
    assert_resource_changes_action(plan.resource_changes,"create", 1)
    assert_resource_changes('custom_surrogate_header',plan.resource_changes)