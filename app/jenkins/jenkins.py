import datetime
from util.export import (export_csv)
import requests
from requests.auth import HTTPBasicAuth


def export_all_jenkins_users(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, export_filename):
    users_list = []
    users_count = 0
    fake_user = 1

    print('{} - INFO - Reading Jenkins users from Jenkins API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), jenkins_site))
    users_response = requests.get(
        '{}://{}/asynchPeople/api/json?pretty=true'.format(jenkins_protocol, jenkins_domain_name),
        auth=HTTPBasicAuth(jenkins_user, jenkins_token)
    ).json()

    for user in users_response["users"]:
        user_absolute_url = user['user']['absoluteUrl']
        tmp = user_absolute_url.split("/")
        user_name = tmp[-1]
        user_email = ""

        user_response = requests.get(
            '{}://{}/user/{}/api/json?pretty=true'.format(jenkins_protocol, jenkins_domain_name, user_name),
            auth=HTTPBasicAuth(jenkins_user, jenkins_token)
        ).json()
        fake_user = 1
        for user_details in user_response["property"]:
            if user_details['_class'] == "hudson.tasks.Mailer$UserProperty":
                user_email = user_details['address']
            if user_details['_class'] == "hudson.security.HudsonPrivateSecurityRealm$Details":
                fake_user = 0

        users_list.append({
            'date': datetime.datetime.now().strftime("%Y%m%d"),
            'user_name': user_name,
            'user_email': user_email,
            'userAbsoluteUrl': user_absolute_url,
            'userFullName': user['user']['fullName'],
            'fake_user': fake_user
        })
        users_count = users_count + 1

    print('{} - INFO - Total: {} users'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(users_count)))

    export_csv(
        export_filename,
        users_list,
        ['date', 'user_name', 'user_email', 'user_absolute_url', 'user_full_name', 'fake_user'],
        ['date', 'user_name', 'user_email', 'userAbsoluteUrl', 'userFullName', 'fake_user']
    )

    return users_list


def export_all_jenkins_plugins(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, export_filename):
    plugins_list = []
    plugins_count = 0

    print('{} - INFO - Reading Jenkins plugins from Jenkins API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), jenkins_site))
    plugins_response = requests.get(
        '{}://{}/pluginManager/api/json?depth=1&pretty=true'.format(jenkins_protocol, jenkins_domain_name),
        auth=HTTPBasicAuth(jenkins_user, jenkins_token)
    ).json()

    for plugin in plugins_response["plugins"]:

        plugins_list.append({
            'date': datetime.datetime.now().strftime("%Y%m%d"),
            'short_name': plugin['shortName'],
            'long_name': plugin['longName'],
            'version': plugin['version'],
            'active': plugin['active'],
            'enabled': plugin['enabled']
        })
        plugins_count = plugins_count + 1

    print('{} - INFO - Total: {} plugins'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(plugins_count)))

    export_csv(
        export_filename,
        plugins_list,
        ['date', 'short_name', 'long_name', 'version', 'active', 'enabled'],
        ['date', 'short_name', 'long_name', 'version', 'active', 'enabled']
    )

    return plugins_list


def export_all_jenkins_jobs(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, export_filename):
    jobs_list = []
    jobs_count = 0

    print('{} - INFO - Reading Jenkins jobs from Jenkins API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), jenkins_site))
    jobs_response = requests.get(
        '{}://{}/api/json?tree=jobs[*]&pretty=true'.format(jenkins_protocol, jenkins_domain_name),
        auth=HTTPBasicAuth(jenkins_user, jenkins_token)
    ).json()

    for job in jobs_response["jobs"]:

        jobs_list.append({
            'date': datetime.datetime.now().strftime("%Y%m%d"),
            'name': job['name'],
            'display_name': job['displayName'],
            'description': job['description']
        })
        jobs_count = jobs_count + 1

    print('{} - INFO - Total: {} jobs'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(jobs_count)))

    export_csv(
        export_filename,
        jobs_list,
        ['date', 'name', 'display_name', 'description'],
        ['date', 'name', 'display_name', 'description']
    )

    return jobs_list


def export_all_jenkins_jobs_builds(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, jobs_list, export_filename):

    print('{} - INFO - Reading Jenkins jobs builds from Jenkins API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), jenkins_site))
    jobs_builds_list = []
    for job in jobs_list:
        jobs_builds_count = 0

        jobs_builds_response = requests.get(
            '{}://{}/job/{}/api/json?tree=allBuilds[*]&pretty=true'.format(jenkins_protocol, jenkins_domain_name, job['name']),
            auth=HTTPBasicAuth(jenkins_user, jenkins_token)
        ).json()

        for job_build in jobs_builds_response["allBuilds"]:

            jobs_builds_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'name': job['name'],
                'display_name': job_build['displayName'],
                'description': job_build['description'],
                'duration': job_build['duration'],
                'estimated_duration': job_build['estimatedDuration'],
                'full_display_name': job_build['fullDisplayName'],
                'id': job_build['id'],
                'number': job_build['number'],
                'result': job_build['result'],
                # 'in_progress': job_build['inProgress'],
                'timestamp': job_build['timestamp']
            })
            jobs_builds_count = jobs_builds_count + 1

        print('{} - INFO - Total of {} builds for job {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(jobs_builds_count), job['name']))

    export_csv(
        export_filename,
        jobs_builds_list,
        ['date', 'name', 'display_name', 'description', 'duration', 'estimated_duration', 'full_display_name', 'id', 'number', 'result', 'timestamp'],
        ['date', 'name', 'display_name', 'description', 'duration', 'estimated_duration', 'full_display_name', 'id', 'number', 'result', 'timestamp']
    )

    return jobs_list


def export_all_jenkins_rbas_global_roles(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, export_filename):
    rbas_global_roles_list = []
    rbas_global_roles_count = 0
    rbas_global_roles_membership_count = 0

    print('{} - INFO - Reading Jenkins RBAS Global Roles from Jenkins API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), jenkins_site))
    rbas_global_roles_response = requests.get(
        '{}://{}/role-strategy/strategy/getAllRoles?type=globalRoles'.format(jenkins_protocol, jenkins_domain_name),
        auth=HTTPBasicAuth(jenkins_user, jenkins_token)
    ).json()

    for rbas_global_role in rbas_global_roles_response:
        for rbas_global_role_member in rbas_global_roles_response[rbas_global_role]:
            rbas_global_roles_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'role-name': rbas_global_role,
                'member': rbas_global_role_member
            })
            rbas_global_roles_membership_count = rbas_global_roles_membership_count + 1
        rbas_global_roles_count = rbas_global_roles_count + 1

    print('{} - INFO - Total {} Global Roles and {} memberships'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(rbas_global_roles_count), str(rbas_global_roles_membership_count)))

    export_csv(
        export_filename,
        rbas_global_roles_list,
        ['date', 'role-name', 'member'],
        ['date', 'role-name', 'member']
    )

    return rbas_global_roles_list


def export_all_jenkins_rbas_project_roles(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, export_filename):
    rbas_project_roles_list = []
    rbas_project_roles_count = 0
    rbas_project_roles_membership_count = 0

    print('{} - INFO - Reading Jenkins RBAS Project Roles from Jenkins API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), jenkins_site))
    rbas_project_roles_response = requests.get(
        '{}://{}/role-strategy/strategy/getAllRoles?type=projectRoles'.format(jenkins_protocol, jenkins_domain_name),
        auth=HTTPBasicAuth(jenkins_user, jenkins_token)
    ).json()

    for rbas_project_role in rbas_project_roles_response:
        for rbas_project_role_member in rbas_project_roles_response[rbas_project_role]:
            rbas_project_roles_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'role-name': rbas_project_role,
                'member': rbas_project_role_member
            })
            rbas_project_roles_membership_count = rbas_project_roles_membership_count + 1
        rbas_project_roles_count = rbas_project_roles_count + 1

    print('{} - INFO - Total {} Project Roles and {} memberships'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(rbas_project_roles_count), str(rbas_project_roles_membership_count)))

    export_csv(
        export_filename,
        rbas_project_roles_list,
        ['date', 'role-name', 'member'],
        ['date', 'role-name', 'member']
    )

    return rbas_project_roles_list
