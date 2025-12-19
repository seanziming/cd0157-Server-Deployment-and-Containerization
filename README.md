# Deploying a Flask API

This project demonstrates containerization and deployment of a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild.

## Deployment Information

**Live API URL:** http://af09f696b8af34e179a41e5856cd3e6c-555148511.us-east-2.elb.amazonaws.com

**Project Status:** ✅ Successfully Deployed

**AWS Resources:**
- EKS Cluster: `simple-jwt-api` (Kubernetes 1.29, 2 nodes)
- Region: `us-east-2`
- CI/CD Pipeline: CodePipeline + CodeBuild
- Container Registry: Amazon ECR
- GitHub Repository: https://github.com/seanziming/cd0157-Server-Deployment-and-Containerization

## API Endpoints

The Flask app consists of a simple API with three endpoints:

- **`GET '/'`**: Health check endpoint
  ```bash
  curl http://af09f696b8af34e179a41e5856cd3e6c-555148511.us-east-2.elb.amazonaws.com/
  # Returns: "Healthy"
  ```

- **`POST '/auth'`**: Authentication endpoint - returns JWT token
  ```bash
  curl -X POST http://af09f696b8af34e179a41e5856cd3e6c-555148511.us-east-2.elb.amazonaws.com/auth \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"test"}'
  # Returns: {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}
  ```

- **`GET '/contents'`**: Protected endpoint - requires valid JWT
  ```bash
  TOKEN="your-jwt-token-here"
  curl http://af09f696b8af34e179a41e5856cd3e6c-555148511.us-east-2.elb.amazonaws.com/contents \
    -H "Authorization: Bearer $TOKEN"
  # Returns: {"email":"test@test.com","exp":1767365655,"nbf":1766156055}
  ``` 

The app relies on a secret set as the environment variable `JWT_SECRET` to produce a JWT. The built-in Flask server is adequate for local development, but not production, so you will be using the production-ready [Gunicorn](https://gunicorn.org/) server when deploying the app.



## Prerequisites

* Docker Desktop - Installation instructions for all OSes can be found <a href="https://docs.docker.com/install/" target="_blank">here</a>.
* Git: <a href="https://git-scm.com/downloads" target="_blank">Download and install Git</a> for your system. 
* Code editor: You can <a href="https://code.visualstudio.com/download" target="_blank">download and install VS code</a> here.
* AWS Account
* Python version between 3.7 and 3.9. Check the current version using:
```bash
#  Mac/Linux/Windows 
python --version
```
You can download a specific release version from <a href="https://www.python.org/downloads/" target="_blank">here</a>.

* Python package manager - PIP 19.x or higher. PIP is already installed in Python 3 >=3.4 downloaded from python.org . However, you can upgrade to a specific version, say 20.2.3, using the command:
```bash
#  Mac/Linux/Windows Check the current version
pip --version
# Mac/Linux
pip install --upgrade pip==20.2.3
# Windows
python -m pip install --upgrade pip==20.2.3
```
* Terminal
   * Mac/Linux users can use the default terminal.
   * Windows users can use either the GitBash terminal or WSL. 
* Command line utilities:
  * AWS CLI installed and configured using the `aws configure` command. Another important configuration is the region. Do not use the us-east-1 because the cluster creation may fails mostly in us-east-1. Let's change the default region to:
  ```bash
  aws configure set region us-east-2  
  ```
  Ensure to create all your resources in a single region. 
  * EKSCTL installed in your system. Follow the instructions [available here](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html#installing-eksctl) or <a href="https://eksctl.io/introduction/#installation" target="_blank">here</a> to download and install `eksctl` utility. 
  * The KUBECTL installed in your system. Installation instructions for kubectl can be found <a href="https://kubernetes.io/docs/tasks/tools/install-kubectl/" target="_blank">here</a>. 


## Initial setup

1. Fork the <a href="https://github.com/udacity/cd0157-Server-Deployment-and-Containerization" target="_blank">Server and Deployment Containerization Github repo</a> to your Github account.
1. Locally clone your forked version to begin working on the project.
```bash
git clone https://github.com/SudKul/cd0157-Server-Deployment-and-Containerization.git
cd cd0157-Server-Deployment-and-Containerization/
```
1. These are the files relevant for the current project:
```bash
.
├── Dockerfile 
├── README.md
├── aws-auth-patch.yml #ToDo
├── buildspec.yml      #ToDo
├── ci-cd-codepipeline.cfn.yml #ToDo
├── iam-role-policy.json  #ToDo
├── main.py
├── requirements.txt
├── simple_jwt_api.yml
├── test_main.py  #ToDo
└── trust.json     #ToDo 
```

     
## Project Steps Completed

✅ **1. Write a Dockerfile for a simple Flask API**
   - Dockerfile created with Python 3.7, Gunicorn server configuration

✅ **2. Build and test the container locally**
   - Docker image built and tested successfully
   - All pytest tests passing (5/5)

✅ **3. Create an EKS cluster**
   - Cluster name: `simple-jwt-api`
   - Kubernetes version: 1.29
   - Node count: 2 (t2.medium instances)
   - Region: us-east-2

✅ **4. Store a secret using AWS Parameter Store**
   - JWT_SECRET stored as SecureString
   - Accessible by CodeBuild during deployment

✅ **5. Create a CodePipeline pipeline triggered by GitHub checkins**
   - Pipeline name: `simple-jwt-api-pipeline-CodePipelineGitHub-SqZFbIUHBRUV`
   - Source: GitHub repository (master branch)
   - Automatic trigger on code push

✅ **6. Create a CodeBuild stage which will build, test, and deploy your code**
   - Tests run in pre_build phase
   - Docker image built and pushed to ECR
   - Deployment to EKS cluster
   - Service exposed via LoadBalancer

## Deployment Architecture

```
GitHub (Code Push)
    ↓
CodePipeline (Trigger)
    ↓
CodeBuild (Build & Test)
    ↓
ECR (Container Registry)
    ↓
EKS Cluster (Kubernetes)
    ↓
LoadBalancer (Public Access)
```

## Additional Configuration Files

- ✅ `aws-auth-patch.yml` - RBAC authorization for CodeBuild
- ✅ `buildspec.yml` - CodeBuild build specification
- ✅ `ci-cd-codepipeline.cfn.yml` - CloudFormation template for CI/CD
- ✅ `iam-role-policy.json` - IAM policy for kubectl role
- ✅ `trust.json` - IAM role trust policy
- ✅ `test_main.py` - Unit tests for Flask API

## Testing the Deployed API

### Using PowerShell:

```powershell
# Health check
curl http://af09f696b8af34e179a41e5856cd3e6c-555148511.us-east-2.elb.amazonaws.com/

# Get JWT token
$response = curl -Method POST -Uri "http://af09f696b8af34e179a41e5856cd3e6c-555148511.us-east-2.elb.amazonaws.com/auth" `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"email":"test@test.com","password":"test"}'
$token = ($response.Content | ConvertFrom-Json).token

# Access protected endpoint
curl -Uri "http://af09f696b8af34e179a41e5856cd3e6c-555148511.us-east-2.elb.amazonaws.com/contents" `
  -Headers @{"Authorization"="Bearer $token"}
```

### Using Bash/curl:

```bash
# Health check
curl http://af09f696b8af34e179a41e5856cd3e6c-555148511.us-east-2.elb.amazonaws.com/

# Get JWT token
export TOKEN=$(curl -X POST http://af09f696b8af34e179a41e5856cd3e6c-555148511.us-east-2.elb.amazonaws.com/auth \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test"}' | jq -r '.token')

# Access protected endpoint
curl http://af09f696b8af34e179a41e5856cd3e6c-555148511.us-east-2.elb.amazonaws.com/contents \
  -H "Authorization: Bearer $TOKEN"
```

## Kubernetes Resources

Check deployment status:
```bash
kubectl get pods
kubectl get service simple-jwt-api
kubectl get deployments
```

View logs:
```bash
kubectl logs -l app=simple-jwt-api
```

## Cleanup

To avoid ongoing AWS charges, delete resources:

```bash
# Delete CloudFormation stack (Pipeline, CodeBuild, ECR, S3)
aws cloudformation delete-stack --stack-name simple-jwt-api-pipeline --region us-east-2

# Delete EKS cluster
eksctl delete cluster --name simple-jwt-api --region us-east-2

# Delete Parameter Store secret
aws ssm delete-parameter --name JWT_SECRET --region us-east-2

# Delete IAM role
aws iam delete-role-policy --role-name UdacityFlaskDeployCBKubectlRole --policy-name eks-describe
aws iam delete-role --role-name UdacityFlaskDeployCBKubectlRole
```

