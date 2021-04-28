import os
import pytest
import json

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'infra')
PLATFORM_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'platform-config/eu-west-1.json')


def assert_resource_changes_action(resource_changes, action, length):
    resource_changes_create = [
        value for _, value in resource_changes.items()
        if value.get('change').get('actions') == [action]
    ]
    assert len(resource_changes_create) == length

def assert_resource_changes(testname, resource_changes):
    with open(f'test/files/{testname}.json', 'r') as f:
        data = json.load(f)
        i = 0
        for _, value in resource_changes.items():
            assert sorted(data.get('resource_changes')[i]) == sorted(value)
            i=+1

def test_resources(e2e_plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})
    _, modules, resources = e2e_plan_runner(
        FIXTURES_DIR,
        tf_var_file=PLATFORM_CONFIG_FILE,
        env="dev", 
        fastly_domain="externaldomain.com", 
        alb_domain="domain.com",
        team="foobar", 
        component="foobar")

    assert len(modules) == 4
    assert len(resources) == 6

def test_create_public_alb_in_public_subnets(e2e_plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})

    env = 'testenv'
    component = 'testcomponent'
    team = 'testteam'

    plan, _, resources = e2e_plan_runner(
        FIXTURES_DIR,
        tf_var_file=PLATFORM_CONFIG_FILE,
        targets=['module.frontend_router.module.alb.aws_alb.alb'],
        env=env, 
        fastly_domain="externaldomain.com", 
        alb_domain="domain.com",
        team=team, 
        component=component)
    
    assert_resource_changes_action(plan.resource_changes,"create", 2)
    assert_resource_changes('create_public_alb_in_public_subnets',plan.resource_changes)
    
def test_create_public_alb_listener(e2e_plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})

    env = 'testenv'
    component = 'testcomponent'
    team = 'testteam'

    plan, _, resources = e2e_plan_runner(
        FIXTURES_DIR,
        tf_var_file=PLATFORM_CONFIG_FILE,
        targets=['module.frontend_router.module.alb.aws_alb_listener.https'],
        env=env, 
        fastly_domain="externaldomain.com", 
        alb_domain="domain.com",
        team=team, 
        component=component)
    
    assert_resource_changes_action(plan.resource_changes,"create", 4)
    assert_resource_changes('create_public_alb_listener',plan.resource_changes)


def test_create_public_alb_security_group(e2e_plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})

    env = 'testenv'
    component = 'testcomponent'
    team = 'testteam'

    plan, _, resources = e2e_plan_runner(
        FIXTURES_DIR,
        tf_var_file=PLATFORM_CONFIG_FILE,
        targets=['module.frontend_router.module.alb.aws_security_group.default'],
        env=env, 
        fastly_domain="externaldomain.com", 
        alb_domain="domain.com",
        team=team, 
        component=component)
    
    assert_resource_changes_action(plan.resource_changes,"create", 1)
    assert_resource_changes('create_public_alb_security_group',plan.resource_changes)


def test_fastly_shield(e2e_plan_runner):
    os.environ.update({'FASTLY_API_KEY': 'querty'})

    env = 'testenv'
    component = 'testcomponent'
    team = 'testteam'

    plan, _, resources = e2e_plan_runner(
        FIXTURES_DIR,
        tf_var_file=PLATFORM_CONFIG_FILE,
        targets=['module.frontend_router_shield.module.fastly.fastly_service_v1.fastly'],
        env=env, 
        fastly_domain="externaldomain.com",

        alb_domain="domain.com",
        shield='test-shield',
        team=team, 
        component=component)
    
    assert_resource_changes_action(plan.resource_changes,"create", 4)
    assert_resource_changes('fastly_shield',plan.resource_changes)

