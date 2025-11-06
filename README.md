# DevOps Learning Pipeline

This repository is designed as a hands-on learning environment for DevOps practices and tools. It provides a structured approach to understanding various aspects of the DevOps pipeline, from continuous integration to deployment, monitoring, and artifact management.

## Project Structure

```
devops-learning-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI pipeline configuration
├── sample-app/
│   ├── app.py                     # FastAPI sample application
│   ├── test_app.py               # Unit tests for the application
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Container configuration
├── pipeline/
│   └── jenkins/
│       └── Jenkinsfile           # Jenkins pipeline configuration
└── configs/
    └── kubernetes/
        └── deployment.yaml       # Kubernetes deployment configuration
```

## Detailed Component Description

### 1. Sample Application (`/sample-app/`)

#### `app.py`
- A FastAPI-based web service demonstration application
- Provides two endpoints:
  - `/`: Returns a greeting message
  - `/health`: Health check endpoint for monitoring
- Uses uvicorn as the ASGI server
- Runs on port 8000 by default

#### `test_app.py`
- Contains unit tests for the sample application
- Uses pytest framework
- Tests both endpoints for:
  - Correct HTTP response codes
  - Expected response payload
  - API contract validation

#### `requirements.txt`
Dependencies required for the application:
- `fastapi>=0.68.0`: Modern, fast web framework
- `uvicorn>=0.15.0`: ASGI server implementation
- `pytest>=6.2.4`: Testing framework
- `httpx>=0.18.2`: HTTP client for testing
- `requests>=2.26.0`: HTTP library for API requests

#### `Dockerfile`
- Base image: `python:3.9-slim` for minimal container size
- Sets up working directory as `/app`
- Installs dependencies from requirements.txt
- Exposes port 8000
- Configures the application to run with uvicorn

### 2. CI/CD Configurations

#### GitHub Actions (`.github/workflows/ci.yml`)
Defines the continuous integration pipeline with:
- Trigger conditions: push to main branch or pull requests
- Test job:
  - Sets up Python 3.9
  - Installs dependencies
  - Runs pytest suite
- Build job:
  - Builds Docker image
  - Placeholder for security scanning

#### Jenkins Pipeline (`pipeline/jenkins/Jenkinsfile`)
Defines a Jenkins pipeline with three stages:
1. Test Stage:
   - Installs Python dependencies
   - Runs pytest suite
2. Build Stage:
   - Builds Docker image with unique tag
3. Deploy Stage:
   - Placeholder for deployment steps
- Includes workspace cleanup in post-execution

### 3. Kubernetes Configuration (`configs/kubernetes/deployment.yaml`)

Defines two Kubernetes resources:

#### Deployment
- Specifies 3 replica pods for high availability
- Container configuration:
  - Uses the sample-app image
  - Exposes port 8000
  - Labels for service discovery

#### Service
- Type: LoadBalancer for external access
- Port mapping: 80 -> 8000
- Selector matches app labels for pod discovery

## Getting Started

### 1. Local Development
```bash
# Install dependencies
cd sample-app
pip install -r requirements.txt

# Run tests
pytest

# Start the application
python app.py
```

### 2. Docker Development
```bash
# Build container
docker build -t sample-app .

# Run container
docker run -p 8000:8000 sample-app
```

### 3. Kubernetes Deployment
```bash
# Apply configuration
kubectl apply -f configs/kubernetes/deployment.yaml

# Verify deployment
kubectl get deployments
kubectl get services
```

## Learning Path

1. **CI/CD Pipeline Understanding**
   - Study the GitHub Actions workflow
   - Examine the Jenkins pipeline structure
   - Compare different CI/CD approaches

2. **Container Management**
   - Learn Docker image building
   - Understand container configuration
   - Practice container orchestration

3. **Kubernetes Deployment**
   - Understand deployment strategies
   - Learn service configuration
   - Practice scaling and management

4. **Testing and Quality**
   - Write additional tests
   - Implement security scanning
   - Add code quality checks

## Extending the Pipeline

### Adding New Tools
1. Create appropriate configuration files
2. Add to existing CI/CD pipelines
3. Document setup and usage
4. Test integration

### Monitoring Integration
- Add Prometheus metrics
- Configure Grafana dashboards
- Set up alerting rules

### Security Additions
- Add vulnerability scanning
- Implement secret management
- Configure compliance checks

## Best Practices Demonstrated

1. **CI/CD**
   - Automated testing
   - Containerized builds
   - Pipeline as code

2. **Container**
   - Minimal base images
   - Clear build steps
   - Port exposure

3. **Kubernetes**
   - High availability setup
   - Service discovery
   - Load balancing

4. **Testing**
   - Unit test coverage
   - Integration testing
   - Health checks

## Contributing

Feel free to:
1. Add new pipeline tools
2. Improve existing configurations
3. Add monitoring solutions
4. Implement security scans
5. Enhance documentation

## Support

For questions or issues:
1. Create an issue in the repository
2. Provide clear reproduction steps
3. Include relevant logs and configurations

## License

This project is open-source and available under the MIT License.
 
## Using Cloudsmith as a Container Registry

This project includes a sample GitHub Actions `publish` job that can push Docker images to Cloudsmith. Cloudsmith supports container repositories and can act as your registry for images built in CI.

Quick steps to try Cloudsmith:

1. Create a repository in Cloudsmith (choose the Docker/Container type) and note your owner and repository name.
2. Create an API key in Cloudsmith ("API keys") with write/publish permissions.
3. In your GitHub repository, add the following secrets:
    - `CLOUDSMITH_API_KEY` — the API key value (secret)
    - `CLOUDSMITH_OWNER` — your Cloudsmith owner name
    - `CLOUDSMITH_REPO` — the repository name in Cloudsmith to push to

Local push example (for manual testing):

```bash
# Tag the image for Cloudsmith
docker tag sample-app:latest docker.cloudsmith.io/<OWNER>/<REPO>:v1.0.0

# Log in (replace <OWNER> and use your API key as the password)
docker login docker.cloudsmith.io -u <OWNER> -p <API_KEY>

# Push the image
docker push docker.cloudsmith.io/<OWNER>/<REPO>:v1.0.0
```

CI (GitHub Actions):
- The included `publish` job in `.github/workflows/ci.yml` will log in using your secrets, tag the image built by the `build` job and push it to Cloudsmith using the SHA as a tag. Make sure the secrets listed above are set in the GitHub repository settings.

Kubernetes usage notes:
- Update `configs/kubernetes/deployment.yaml` to point to the published image `docker.cloudsmith.io/<OWNER>/<REPO>:<TAG>`.
- If your Cloudsmith repository requires authentication, create a Kubernetes image pull secret and reference it in the manifest:

```bash
# Create a docker-registry secret in the namespace where you deploy
kubectl create secret docker-registry cloudsmith-registry-secret \
   --docker-server=docker.cloudsmith.io \
   --docker-username=<OWNER> \
   --docker-password=<API_KEY> \
   --docker-email=you@example.com
```

Then uncomment or add `imagePullSecrets:` in the deployment manifest:

```yaml
imagePullSecrets:
- name: cloudsmith-registry-secret
```

Security reminder: never commit API keys or secrets to the repository. Use GitHub Secrets or your CI provider's secret store.