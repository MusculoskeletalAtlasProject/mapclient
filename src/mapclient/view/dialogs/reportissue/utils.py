import webbrowser


def create_github_issue(text=""):
    """
    Open the url for creating a new GitHub issue in the MAP-Client repository and auto-fill the issue description with the text supplied.
    """
    url = "https://github.com/MusculoskeletalAtlasProject/mapclient/issues/new"
    url += "?body=" + text
    webbrowser.open(url)


def create_wrike_ticket():
    url = "https://www.wrike.com/form/eyJhY2NvdW50SWQiOjMyMDM1ODgsInRhc2tGb3JtSWQiOjU5NTQxOH0JNDg2ODkwNzc5NjU5NAlmODVjYjQ4MTAyYTU2MjdjMmY5ZWQwZGMyMjc5OTEzZTljZGFiZWRjYmY2MmIyZDRjZmVmZmMxNmYwNGU2MzEy"
    webbrowser.open(url)
