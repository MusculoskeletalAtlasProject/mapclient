import webbrowser


def create_github_issue(text=""):
    """
    Open the url for creating a new GitHub issue in the MAP-Client repository and auto-fill the issue description with the text supplied.
    """
    url = "https://github.com/MusculoskeletalAtlasProject/mapclient/issues/new"
    url += "?body=" + text
    webbrowser.open(url)


def create_wrike_ticket():
    url = "https://www.wrike.com/frontend/requestforms/index.html?token=eyJhY2NvdW50SWQiOjMyMDM1ODgsInRhc2tGb3JtSWQiOjU5NTQxOH0JNDg0N" \
          "zEzOTAxODIxNgllZTg2ZDg5NmNkMDQ3YjJkMWM2Njg5ZWI5YTQ2NjMxNGJkZjZiOWQwYjZkZmU2NTk1YzU0MWVlN2EyZjQ5M2Ux"
    webbrowser.open(url)
