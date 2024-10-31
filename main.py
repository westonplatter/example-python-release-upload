import json
from loguru import logger
import os
from pathlib import Path
import platform
import requests
import sys

def to_error_message(errs):
  """
  Formats an array of error dicts into an error message string. Returns an error message.
  """

  return ', '.join(map(lambda e: f"{e['title']}: {e['detail']}", errs))

def create_release(version, channel, name=None, tag=None):
  """
  Creates a new release for the configured product. Returns a release object.
  """

  res = requests.post(
    f"https://api.keygen.sh/v1/accounts/{os.environ['KEYGEN_ACCOUNT_ID']}/releases",
    headers={
      'Authorization': f"Bearer {os.environ['KEYGEN_PRODUCT_TOKEN']}",
      'Content-Type': 'application/vnd.api+json',
      'Accept': 'application/vnd.api+json',
      'Keygen-Version': '1.3'
    },
    data=json.dumps({
      'data': {
        'type': 'releases',
        'attributes': {
          'version': version,
          'channel': channel,
          'name': name,
          'tag': tag
        },
        'relationships': {
          'product': {
            'data': { 'type': 'product', 'id': os.environ['KEYGEN_PRODUCT_ID'] }
          }
        }
      }
    })
  )

  release = res.json()

  if 'errors' in release:
    errs = release['errors']

    logger.error(f'[error] Release failed: errors={to_error_message(errs)}')

    sys.exit(1)
  else:
    logger.info(f"[info] Created: release={release['data']['id']} link={release['data']['links']['self']}")

  return release['data']

def publish_release(release):
  """
  Publishes a release. Returns a release object.
  """

  res = requests.post(
    f"https://api.keygen.sh/v1/accounts/{os.environ['KEYGEN_ACCOUNT_ID']}/releases/{release['id']}/actions/publish",
    headers={
      'Authorization': f"Bearer {os.environ['KEYGEN_PRODUCT_TOKEN']}",
      'Accept': 'application/vnd.api+json',
      'Keygen-Version': '1.3'
    }
  )

  release = res.json()

  if 'errors' in release:
    errs = release['errors']

    logger.error(f'[error] Publish failed: errors={to_error_message(errs)}')

    sys.exit(1)
  else:
    logger.info(f"[info] Published: release={release['data']['id']} link={release['data']['links']['self']}")

  return release['data']

def upload_artifact_for_release(release, filename, filetype, filesize, platform, arch, data=None):
  """
  Uploads an artifact for the given release. Returns an artifact object.
  """

  res = requests.post(
    f"https://api.keygen.sh/v1/accounts/{os.environ['KEYGEN_ACCOUNT_ID']}/artifacts",
    allow_redirects=False,
    headers={
      'Authorization': f"Bearer {os.environ['KEYGEN_PRODUCT_TOKEN']}",
      'Content-Type': 'application/vnd.api+json',
      'Accept': 'application/vnd.api+json',
      'Keygen-Version': '1.3'
    },
    data=json.dumps({
      'data': {
        'type': 'artifacts',
        'attributes': {
          'filename': filename,
          'filesize': filesize,
          'filetype': filetype,
          'platform': platform,
          'arch': arch
        },
        'relationships': {
          'release': {
            'data': { 'type': 'release', 'id': release['id'] }
          }
        }
      }
    })
  )

  artifact = res.json()

  if 'errors' in artifact:
    errs = artifact['errors']

    logger.error(f'[error] Upload failed: errors={to_error_message(errs)}')

    sys.exit(1)
  else:
    logger.info(f"[info] Uploaded: artifact={artifact['data']['id']} link={artifact['data']['links']['self']}")

  # Follow redirect and upload file to storage provider
  upload_url = res.headers['location']

  if data:
    requests.put(upload_url,
      headers={ 'Content-Type': 'text/plain' },
      data=data
    )

  return artifact['data']


if __name__ == '__main__':
  release = create_release(
    name='keygen-hello-world',
    version='1.0.0',
    channel='stable'
  )

  with open('examples/keygen-hello-world/dist/keygen_hello_world-1.0.0-py3-none-any.whl', mode='rb') as f:
    filename = Path(f.name).name
    stat = os.stat(f.name)

    artifact = upload_artifact_for_release(
      filename=filename,
      filesize=stat.st_size,
      filetype='whl',
      platform=f"{platform.system()} {platform.release()}",
      arch=platform.processor(),
      release=release,
      data=f
    )

  with open('examples/keygen-hello-world/dist/keygen-hello-world-1.0.0.tar.gz', mode='rb') as f:
    filename = Path(f.name).name
    stat = os.stat(f.name)

    artifact = upload_artifact_for_release(
      filename=filename,
      filesize=stat.st_size,
      filetype='tar.gz',
      platform=f"{platform.system()} {platform.release()}",
      arch=platform.processor(),
      release=release,
      data=f
    )

  publish_release(release)