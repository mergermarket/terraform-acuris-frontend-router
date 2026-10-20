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
    with open(f'test/modules/alb/files/{testname}.json', 'r') as f:
        data = json.load(f)
        i = 0
        for _, value in resource_changes.items():
            assert sorted(data.get('resource_changes')[i]) == sorted(value)
            i=+1


def test_create_alb(plan_runner):
    plan , resources = plan_runner(FIXTURES_DIR, targets=["module.alb_test"])

    assert len(resources) == 3
    assert_resource_changes_action(plan.resource_changes,"create", 3)
    assert_resource_changes('create_alb',plan.resource_changes)

def test_create_alb_with_tags(plan_runner):
    plan , resources = plan_runner(FIXTURES_DIR, targets=["module.alb_test_with_tags"])

    assert len(resources) == 3
    assert_resource_changes_action(plan.resource_changes,"create", 3)
    assert_resource_changes('create_alb_with_tags',plan.resource_changes)

def get_security_group_ingress(plan, module):
    sg = plan.resource_changes[f'module.{module}.aws_security_group.default']
    return {
        rule['from_port']: (rule['cidr_blocks'], rule['prefix_list_ids'])
        for rule in sg['change']['after']['ingress']
    }

def test_security_group_ingress_defaults_to_open(plan_runner):
    plan, _ = plan_runner(FIXTURES_DIR, targets=["module.alb_test"])

    assert get_security_group_ingress(plan, 'alb_test') == {
        80: (['0.0.0.0/0'], []),
        443: (['0.0.0.0/0'], []),
    }

def test_security_group_ingress_prefix_list_ids(plan_runner):
    plan, _ = plan_runner(FIXTURES_DIR, targets=["module.alb_test_with_ingress_prefix_list_ids"])

    prefix_list_ids = ['pl-0123456789abcdef0', 'pl-0fedcba9876543210']
    ingress = get_security_group_ingress(plan, 'alb_test_with_ingress_prefix_list_ids')
    assert sorted(ingress) == [80, 443]
    for port in (80, 443):
        cidr_blocks, ids = ingress[port]
        assert cidr_blocks == []
        assert sorted(ids) == prefix_list_ids
