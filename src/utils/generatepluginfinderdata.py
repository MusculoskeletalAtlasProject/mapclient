import os

from utils.plugindata import MAPPlugin, read_step_info, get_remote_database, write_step_database, save_plugin_icon, \
    authenticate_github_user, get_plugin_sources, get_remote_database_timestamp, read_line

from github import Github
from github.GithubException import UnknownObjectException, RateLimitExceededException


def check_plugins_for_updates():
    def check_plugin_info():
        name = repo.name
        updated_at = repo.updated_at.timestamp()
        if (name not in plugin_data.keys()) or (data_timestamp < updated_at):
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
                    version = get_latest_version(step_path)
                    plugin_data[name] = MAPPlugin(formatted_name, category, icon_name, url, version)
                    break
            if not step_file:
                print(f"GitHub repository \"{repo.full_name}\" in not a valid MAP-Client plugin.")

    # TODO: Once all MAP plugins have versioned-releases, update this with a version retrieval directly from the repo.
    def get_latest_version(step_path):
        init_file_path = os.path.dirname(step_path) + "/__init__.py"
        init_file = repo.get_contents(init_file_path).decoded_content.decode()
        version = ""
        lines = iter(init_file.splitlines())
        for line in lines:
            line = line.strip()
            if line.startswith("__version__"):
                version = read_line(line, "=")

        return version

    plugin_sources = get_plugin_sources()
    plugin_orgs = plugin_sources["plugin_organizations"]
    plugin_repos = plugin_sources["plugin_repositories"]
    plugin_data = get_remote_database()
    data_timestamp = get_remote_database_timestamp()

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
                g = authenticate_github_user()

    write_step_database(plugin_data)


if __name__ == '__main__':
    check_plugins_for_updates()
