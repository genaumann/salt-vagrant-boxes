"""
API scripts
"""

import os
import sys
import requests

base_url = "https://app.vagrantup.com/api/v2"
username = "genaumann"

session = requests.Session()
try:
  session.headers.update({"Authorization": f"Bearer {os.environ['VAGRANT_CLOUD_TOKEN']}"})
except KeyError:
  raise Exception("Set vagrant cloud token variable: $VAGRANT_CLOUD_TOKEN")

def get_boxes() -> dict[dict]:
  """
  Get all boxes of user
  """

  response = session.get(f"{base_url}/user/{username}")
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
    "box": {
      "username": username,
      "name": f"{box_name}-salt",
      "short_description": f"{box_name} Salt Formula testing",
      "is_private": False
    }
  }

  response = session.post(f"{base_url}/boxes", json=data)
  response.raise_for_status()

  try:
    print(f"Box {response.json()["tag"]} successfully created")
    return True
  except KeyError:
    raise Exception(f"Box {box_name} not created")

def get_versions(box_name : str) -> list:
  """
  Get all versions of a box
  """

  response = session.get(f"{base_url}/box/{username}/{box_name}-salt")
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
    if version["version"] == salt_version:
      return True
    
  return False

def rename_version(box_name : str, salt_version : str) -> bool:
  """
  Rename version for preserving conflicts
  """

  data = {
    "version": {
      "version": f"{salt_version}.old",
      "description": f"Deprecated - use {salt_version} instead"
    }
  }

  response = session.put(f"{base_url}/box/{username}/{box_name}-salt/version/{salt_version}", json=data)
  response.raise_for_status()

  try:
    print(f"{box_name} version changed from {salt_version} to {response.json()['version']}")
    return True
  except KeyError:
    raise Exception(f"Renaming of version {salt_version} from {box_name} failed")

def remove_version(box_name: str, salt_version: str) -> bool:
  """
  Remove deprecated version
  """

  response = session.delete(f"{base_url}/box/{username}/{box_name}-salt/version/{salt_version}")
  response.raise_for_status()

  try:
    print(f"Removed version {response.json()["version"]} from {box_name}")
    return True
  except KeyError:
    raise Exception(f"Failed to remove version {salt_version} of {box_name}")

if __name__ == "__main__":
  box_name = sys.argv[1]
  salt_version = sys.argv[2]
  if not check_box_exist(box_name):
    create_box(box_name)
    sys.exit(0)

  if check_version_exist(box_name, salt_version):
    rename_version(box_name, salt_version)

  if check_version_exist(box_name, f"{salt_version}.old"):
    remove_version(box_name, f"{salt_version}.old")

  sys.exit(0)
