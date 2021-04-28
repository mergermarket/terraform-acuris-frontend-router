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