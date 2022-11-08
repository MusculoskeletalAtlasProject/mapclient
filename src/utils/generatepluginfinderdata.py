import os
import time

from utils.plugindata import MAPPlugin, read_step_info, read_step_database, write_step_database, save_plugin_icon

from github import Github
from github.GithubException import UnknownObjectException, BadCredentialsException, RateLimitExceededException


# The following variables define where the Plugin Finder searches for plugin repositories.
plugin_organisations = ['mapclient-plugins']
plugin_repositories = []


def authenticate_github_user():
    try:
        token = os.environ["GITHUB_PAT"]
        g = Github(token)
        _ = g.get_user().name
        return g
    except (KeyError, BadCredentialsException):
        while True:
            try:
                token = input("GITHUB_PAT cannot be found or is invalid. Please provide a Personal Access Token for GitHub: ")
                g = Github(token)
                _ = g.get_user().name
                return g
            except BadCredentialsException:
                print("The Personal Access Token given is not valid.")


def check_plugins_for_updates(plugin_orgs, plugin_repos):
    def check_plugin_info():
        name = repo.name
        updated_at = repo.updated_at.timestamp()
        if True:
            step_paths = [
                f'mapclientplugins/{name}/step.py',
                f'mapclientplugins/{name}step/step.py',
                f'mapclientplugins/{name[name.find(".") + 1:]}/step.py',
                f'mapclientplugins/{name[name.find(".") + 1:]}step/step.py'
            ]
            step_file = None
            for step_path in step_paths:
                try:
                    step_file = repo.get_contents(step_path).decoded_content.decode()
                except UnknownObjectException:
                    continue
                else:
                    formatted_name, category, icon_path = read_step_info(step_file)
                    icon_name = save_plugin_icon(icon_path)
                    url = repo.url
                    plugin_data.get_plugins()[name] = MAPPlugin(formatted_name, category, icon_name, url)
                    break
            if not step_file:
                print(f"GitHub repository \"{repo.full_name}\" in not a valid MAP-Client plugin.")

    plugin_data = read_step_database()

    g = Github()
    i = 0
    while i < 2:
        try:
            for organisation in plugin_orgs:
                org = g.get_organization(organisation)
                for repo in org.get_repos():
                    check_plugin_info()

            for repository in plugin_repos:
                repo = g.get_repo(repository)
                check_plugin_info()

            break
        except RateLimitExceededException:
            i += 1
            if i < 2:
                print("GitHub API rate limit exceeded. GitHub personal access token required.")
                g = authenticate_github_user()

    write_step_database(plugin_data)


if __name__ == '__main__':
    check_plugins_for_updates(plugin_organisations, plugin_repositories)
