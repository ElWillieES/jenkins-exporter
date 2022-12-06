import datetime
import json
import sys, getopt
import os


def show_help():
    print("jenkins-exporter is a free and open source tool intended to export some Jenkins data,")
    print("like users, jobs, builds, roles, and roles memberships.")
    print()
    print("Usage: jenkins-exporter.py -c <configfile> -a <action>")
    print()
    print("Mandatory arguments to long options are mandatory for short options too.")
    print("  -h, --help           Display this help and exit")
    print("  -c, --configfile     Jenkins config file. Must be located in the ./config directory")
    print("  -a, --action         Action to be executed. Exported data will be located in the ./export directory")
    print("                       The action selected must be one of the following:")
    print()
    print("                       export_all_jenkins_users")
    print("                       export_all_jenkins_plugins")
    print("                       export_all_jenkins_jobs")
    print("                       export_all_jenkins_rbas_global_roles")
    print("                       export_all_jenkins_rbas_project_roles")
    print()
    print("Examples:")
    print("jenkins-exporter.py -c jenkins_conn_myjenkins.json -a export_all_jenkins_users")
    print("jenkins-exporter.py --configfile jenkins_conn_myjenkins.json --action export_all_jenkins_users")
    print("jenkins-exporter.py --configfile=jenkins_conn_myjenkins.json --action=export_all_jenkins_users")
    print()
    print("More info at: https://github.com/ElWillieES/jenkins-exporter")
    print()


def get_cli_params(cli_args):
    config_file = ""
    action = ""

    try:
        opts, args = getopt.getopt(cli_args, "hc:a:", ["help", "configfile=", "action="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-c", "--configfile"):
            config_file = arg
        elif opt in ("-a", "--action"):
            action = arg

    if action != "" and action not in ("export_all_jenkins_users", "export_all_jenkins_plugins", "export_all_jenkins_jobs", "export_all_jenkins_rbas_global_roles", "export_all_jenkins_rbas_project_roles"):
        print("The action specified as parameter, is not valid.")
        print()
        action = ""

    if config_file == "" or action == "":
        show_help()
        sys.exit(2)

    return config_file, action

def get_config_file(config_filename):
    print("{} - INFO - Reading config file {}".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), config_filename))
    config = {}
    try:
        file = open(config_filename)
        config = json.load(file)
        file.close()
        return config
    except Exception as e:
        print("{} - ERROR - Error reading file {}".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), e))
        exit()

def get_jenkins_config_file(config_filename):

    config_conn = get_config_file(config_filename)
    jenkins_site = config_conn["jenkins-site"]
    jenkins_protocol = config_conn["jenkins-protocol"]
    jenkins_domain_name = config_conn["jenkins-domain-name"]
    jenkins_user = config_conn["jenkins-user"]
    jenkins_token = config_conn["jenkins-token"]

    return jenkins_site, jenkins_protocol, jenkins_domain_name, jenkins_user, jenkins_token
