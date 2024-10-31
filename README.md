# Example Release Upload

This is an example of [creating a new release](https://keygen.sh/docs/api/releases/#releases-create)
and [uploading artifacts](https://keygen.sh/docs/api/artifacts/#artifacts-create)
using Keygen's distribution API.

## Running the example

First up, configure a few environment variables:

```bash
# Your Keygen product token
# You can generate a product token via, 
# - your admin dashboard here: https://app.keygen.sh/tokens
# - the API: https://keygen.sh/docs/api/tokens/#tokens-create
export KEYGEN_PRODUCT_TOKEN="A_KEYGEN_PRODUCT_TOKEN"

# Your Keygen account ID. Find yours at https://app.keygen.sh/settings
export KEYGEN_ACCOUNT_ID="YOUR_KEYGEN_ACCOUNT_ID"

# Your Keygen product ID
export KEYGEN_PRODUCT_ID="YOUR_KEYGEN_ACCOUNT_ID"
```

You can either run each line above within your terminal session before
starting the app, or you can add the above contents to your `~/.bashrc`
file and then run `source ~/.bashrc` after saving the file.

Next, install dependencies with [`pip`](https://packaging.python.org/):

```bash
pip install -r requirements.txt
```

```bash
# build the package you will upload in the example
cd examples/keygen-hello-world

# build a wheel and source distribution
python setup.py bdist_wheel sdist
```

To create and upload a new release, run the program:
```bash
python main.py
```

The script will create a new `1.0.0` release and then upload 2 artifacts:

- `keygen_hello_world-1.0.0-py3-none-any.whl`
- `keygen-hello-world-1.0.0.tar.gz`

After uploading the artifacts, the release will be published.

You can now pip install the uploaded python package release:

Export your license token and account slug:
```bash
# A license token, https://app.keygen.sh/licenses
export KEYGEN_LICENSE_TOKEN="YOUR_KEYGEN_LICENSE_TOKEN"

# Your Keygen account slug, https://app.keygen.sh/settings
export KEYGEN_ACCOUNT_SLUG="YOUR_KEYGEN_ACCOUNT_SLUG"
```

Then install the package:
```bash
# TODO - this does not work for me - what am I doing wrong?
pip install --index-url https://license:$KEYGEN_LICENSE_TOKEN@pypi.pkg.keygen.sh/$KEYGEN_ACCOUNT_SLUG/simple keygen-hello-world 
```

Or put this in your `requirements.txt` file:
```txt
# TODO - this does not work for me - what am I doing wrong?
--index-url https://license:${KEYGEN_LICENSE_TOKEN}@pypi.pkg.keygen.sh/${KEYGEN_ACCOUNT_SLUG}/simple 
keygen-hello-world
```

## Questions?

Reach out at [support@keygen.sh](mailto:support@keygen.sh) if you have any
questions or concerns!
