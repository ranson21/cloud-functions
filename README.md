# Cloud Functions

![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white) 	![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)

Cloud functions for use with the major cloud providers (GCP, AWS, Azure) which can be zipped and uploaded to cloud storage. The current deployment supports Google Cloud Build (GCP) to zip each cloud function individually and upload them to the cloud storage bucket.

## Usage

**Local**

You can run the scripts locally for testing and development by using the correct runtime (i.e. python, nodejs, etc.). Below is an example of testing a python function:

```bash
# Change to the cloud function directory
cd functions/python/disable-billing

# Load the python virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the function
python3 main.py

# Exit back to the local shell
deactivate
```

**Deployment**

```bash
gcloud builds submit ./config
```

## License

[MIT](./LICENSE)