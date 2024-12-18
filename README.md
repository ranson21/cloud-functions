# Cloud Functions

![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white) ![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)

Cloud functions for use with the major cloud providers (GCP, AWS, Azure) which can be zipped and uploaded to cloud storage. The current deployment supports Google Cloud Build (GCP) to zip each cloud function individually and upload them to the cloud storage bucket.

## Prerequisites

- Python 3.x with pip
- Node.js and npm
- Make
- Google Cloud SDK (for deployment)

## Project Structure

```
.
├── functions/
│   ├── nodejs/       # Node.js cloud functions
│   └── python/       # Python cloud functions
├── Makefile         # Build and development automation
└── config/          # Cloud Build configuration
```

## Usage

### Local Development

The project includes a Makefile to simplify local development and testing. Here are the main commands:

```bash
# Install all dependencies (both Python and Node.js)
make install-deps

# Run a Python function locally
make run-python FUNCTION=your_function_name

# Run a Node.js function locally
make run-node FUNCTION=your_function_name

# Run all tests
make test

# View all available commands
make help
```

### Manual Local Testing

You can also run the functions directly using their respective runtimes:

```bash
# Example: Running a Python function
cd functions/python/disable-billing
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
deactivate
```

### Deployment

To deploy using Google Cloud Build:

```bash
gcloud builds submit ./config
```

This will:
1. Zip each cloud function individually
2. Upload them to the specified cloud storage bucket
3. Deploy them according to the configuration

## Available Make Commands

- `make install-deps`: Install all dependencies
- `make install-python`: Install only Python dependencies
- `make install-node`: Install only Node.js dependencies
- `make run-python FUNCTION=function_name`: Run a Python function locally
- `make run-node FUNCTION=function_name`: Run a Node.js function locally
- `make test`: Run all tests
- `make test-python`: Run Python tests only
- `make test-node`: Run Node.js tests only
- `make clean`: Clean up temporary files and dependencies

## License

[MIT](./LICENSE)