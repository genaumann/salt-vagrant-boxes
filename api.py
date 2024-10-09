"""
API scripts
"""

import os
import sys
import requests

base_url = "https://api.cloud.hashicorp.com/vagrant/2022-09-30/registry"
username = "genaumann"

session = requests.Session()

def login() -> bool:
  """
  Login to hcp
  """

  client_id = os.environ.get("HCP_CLIENT_ID")
  client_secret = os.environ.get("HCP_CLIENT_SECRET")

  url = "https://auth.idp.hashicorp.com/oauth2/token"
  headers = {
      "Content-Type": "application/x-www-form-urlencoded"
  }
  data = {
      "client_id": client_id,
      "client_secret": client_secret,
      "grant_type": "client_credentials",
      "audience": "https://api.hashicorp.cloud"
  }

  response = requests.post(url, headers=headers, data=data)
  response.raise_for_status()

  session.headers.update({"Authorization": f"Bearer {response.json()['access_token']}"})

def get_boxes() -> dict[dict]:
  """
  Get all boxes of user
  """

  response = session.get(f"{base_url}/{username}/boxes")
  response.raise_for_status()
  return response.json()["boxes"]

def check_box_exist(box_name : str) -> bool:
  """
  Check box exist
  """

  boxes = get_boxes()

  for box in boxes:
    if box["name"] == f"{box_name}-salt":
      return True
    
  return False

def create_box(box_name : str) -> bool:
  """
  Create box
  """

  data = {
    "name": f"{box_name}-salt",
    "short_description": f"{box_name} Salt Formula testing",
    "is_private": False
  }

  response = session.post(f"{base_url}/{username}/boxes", json=data)
  response.raise_for_status()

  try:
    print(f"Box {response.json()["box"]["name"]} successfully created")
    return True
  except KeyError:
    raise Exception(f"Box {box_name} not created")

def get_versions(box_name : str) -> list:
  """
  Get all versions of a box
  """

  response = session.get(f"{base_url}/{username}/box/{box_name}-salt/versions")
  response.raise_for_status()

  try:
    return response.json()["versions"]
  except KeyError:
    raise Exception(f"Failed to get all versions of box {box_name}")

def check_version_exist(box_name : str, salt_version : str) -> bool:
  """
  Check a box version exist
  """

  versions = get_versions(box_name)
  for version in versions:
    if version["name"] == salt_version:
      return True
    
  return False

def rename_version(box_name : str, salt_version : str) -> bool:
  """
  Rename version for preserving conflicts
  """

  data = {
    "name": f"{salt_version}.old",
    "description": f"Deprecated - use {salt_version} instead",
    "state": "DEPRECATED"
  }

  response = session.put(f"{base_url}/{username}/box/{box_name}-salt/version/{salt_version}", json=data)
  response.raise_for_status()

  try:
    print(f"{box_name} version changed from {salt_version} to {response.json()["version"]["name"]}")
    return True
  except KeyError:
    raise Exception(f"Renaming of version {salt_version} from {box_name} failed")

def remove_version(box_name: str, salt_version: str) -> bool:
  """
  Remove deprecated version
  """

  response = session.delete(f"{base_url}/{username}/box/{box_name}-salt/version/{salt_version}")
  response.raise_for_status()

  print(f"Removed version {salt_version} from {box_name}")

if __name__ == "__main__":
  box_name = sys.argv[1]
  salt_version = sys.argv[2]

  try:
    login()
  except Exception as e:
    print(f"Failed to login: {e}")
    sys.exit(1)
    
  if not check_box_exist(box_name):
    create_box(box_name)
    sys.exit(0)

  if check_version_exist(box_name, salt_version):
    rename_version(box_name, salt_version)

  if check_version_exist(box_name, f"{salt_version}.old"):
    remove_version(box_name, f"{salt_version}.old")

  sys.exit(0)
