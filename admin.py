import requests


def make_request(url):
    """_summary_: makes a request to the url

    Args:
        url (_type_): _description_
    """
    response = requests.get(url)
    return response.json()


drive_create = "https://admin.googleapis.com/admin/reports/v1/activity/users/all/applications/drive?eventName=create"


resp = make_request(drive_create)
