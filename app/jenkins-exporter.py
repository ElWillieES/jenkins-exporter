import os
import sys
import datetime

from util.config import (get_jenkins_config_file, get_cli_params)
from jenkins.jenkins import (export_all_jenkins_users, export_all_jenkins_plugins, export_all_jenkins_jobs, export_all_jenkins_jobs_builds, export_all_jenkins_rbas_global_roles, export_all_jenkins_rbas_project_roles)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Get command line parameters
    config_file, action = get_cli_params(sys.argv[1:])

    # Create the export and/or config directories if doesnt exists
    export_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/export/"
    config_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/config/"
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    if not os.path.exists(export_path):
        os.makedirs(export_path)
        print("{} - INFO - The directory ""{}"" has been created".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), export_path))
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        print("{} - INFO - The directory ""{}"" has been created".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), config_path))

    # Execute the action requested
    elif action == "export_all_jenkins_users":
        jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token = get_jenkins_config_file(config_path + config_file)
        export_all_jenkins_users(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, export_path + "{}-jenkins-users-{}.csv".format(current_date, jenkins_site))

    elif action == "export_all_jenkins_plugins":
        jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token = get_jenkins_config_file(config_path + config_file)
        export_all_jenkins_plugins(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, export_path + "{}-jenkins-plugins-{}.csv".format(current_date, jenkins_site))

    elif action == "export_all_jenkins_jobs":
        jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token = get_jenkins_config_file(config_path + config_file)
        jobs_list = export_all_jenkins_jobs(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, export_path + "{}-jenkins-jobs-{}.csv".format(current_date, jenkins_site))
        export_all_jenkins_jobs_builds(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, jobs_list, export_path + "{}-jenkins-jobs-builds-{}.csv".format(current_date, jenkins_site))

    elif action == "export_all_jenkins_rbas_global_roles":
        jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token = get_jenkins_config_file(config_path + config_file)
        export_all_jenkins_rbas_global_roles(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, export_path + "{}-jenkins-rbas-global-roles-{}.csv".format(current_date, jenkins_site))

    elif action == "export_all_jenkins_rbas_project_roles":
        jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token = get_jenkins_config_file(config_path + config_file)
        export_all_jenkins_rbas_project_roles(jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token, export_path + "{}-jenkins-rbas-project-roles-{}.csv".format(current_date, jenkins_site))




