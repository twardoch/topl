# Chapter 7: Configuration & Examples

Real-world configuration examples showcasing TOPL's power in different scenarios and use cases.

## Web Application Configuration

### Multi-Environment Setup

```toml
# app-config.toml
[environments.development]
debug = true
db_host = "localhost"
db_port = 5432
api_url = "http://localhost:3000"
log_level = "DEBUG"

[environments.staging]
debug = false
db_host = "staging-db.company.com"
db_port = 5432
api_url = "https://staging-api.company.com"
log_level = "INFO"

[environments.production]
debug = false
db_host = "prod-db.company.com"
db_port = 5432
api_url = "https://api.company.com"
log_level = "WARNING"

[app]
name = "MyWebApp"
version = "2.1.0"
environment = "${ENVIRONMENT}"

# Dynamic environment selection
debug_mode = "${environments.${ENVIRONMENT}.debug}"
log_level = "${environments.${ENVIRONMENT}.log_level}"

[database]
driver = "postgresql"
host = "${environments.${ENVIRONMENT}.db_host}"
port = "${environments.${ENVIRONMENT}.db_port}"
name = "${DB_NAME}"
user = "${DB_USER}"
password = "${DB_PASSWORD}"
url = "${database.driver}://${database.user}:${database.password}@${database.host}:${database.port}/${database.name}"

[api]
base_url = "${environments.${ENVIRONMENT}.api_url}"
timeout = 30
key = "${API_KEY}"
endpoints = {
    users = "${api.base_url}/users",
    posts = "${api.base_url}/posts",
    auth = "${api.base_url}/auth"
}

[logging]
level = "${app.log_level}"
format = "[${app.environment}] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
file = "/var/log/${app.name}-${app.environment}.log"
```

Usage:
```bash
# Development
topl app-config.toml --ENVIRONMENT development --DB_NAME myapp_dev --DB_USER dev_user --DB_PASSWORD dev_pass --API_KEY dev_key

# Production  
topl app-config.toml --ENVIRONMENT production --DB_NAME myapp --DB_USER prod_user --DB_PASSWORD $PROD_DB_PASS --API_KEY $PROD_API_KEY
```

## Microservices Configuration

### Service Discovery Template

```toml
# services.toml
[infrastructure]
domain = "${CLUSTER_DOMAIN}"
namespace = "${KUBERNETES_NAMESPACE}"
protocol = "https"

[service_defaults]
port = 8080
health_path = "/health"
metrics_path = "/metrics"
timeout = 30
replicas = 2

[services.auth]
name = "auth-service"
port = 8001
host = "${services.auth.name}.${infrastructure.namespace}.${infrastructure.domain}"
url = "${infrastructure.protocol}://${services.auth.host}:${services.auth.port}"
health_url = "${services.auth.url}${service_defaults.health_path}"

[services.users]
name = "user-service"
port = 8002
host = "${services.users.name}.${infrastructure.namespace}.${infrastructure.domain}"
url = "${infrastructure.protocol}://${services.users.host}:${services.users.port}"
auth_url = "${services.auth.url}/verify"
depends_on = ["${services.auth.name}"]

[services.notifications]
name = "notification-service"
port = 8003
host = "${services.notifications.name}.${infrastructure.namespace}.${infrastructure.domain}"
url = "${infrastructure.protocol}://${services.notifications.host}:${services.notifications.port}"
user_service_url = "${services.users.url}"
depends_on = ["${services.users.name}"]

[services.gateway]
name = "api-gateway"
port = 80
host = "${services.gateway.name}.${infrastructure.namespace}.${infrastructure.domain}"
url = "${infrastructure.protocol}://${services.gateway.host}"
upstream_services = [
    "${services.auth.url}",
    "${services.users.url}",
    "${services.notifications.url}"
]
```

## Database Configuration

### Multi-Database Setup

```toml
# database.toml
[connection_defaults]
driver = "postgresql"
pool_size = 10
timeout = 30
ssl_mode = "require"

[databases.primary]
name = "primary_db"
host = "${PRIMARY_DB_HOST}"
port = "${PRIMARY_DB_PORT}"
user = "${PRIMARY_DB_USER}"
password = "${PRIMARY_DB_PASSWORD}"
url = "${connection_defaults.driver}://${databases.primary.user}:${databases.primary.password}@${databases.primary.host}:${databases.primary.port}/${databases.primary.name}?sslmode=${connection_defaults.ssl_mode}"

[databases.replica]
name = "replica_db" 
host = "${REPLICA_DB_HOST}"
port = "${REPLICA_DB_PORT}"
user = "${REPLICA_DB_USER}"
password = "${REPLICA_DB_PASSWORD}"
url = "${connection_defaults.driver}://${databases.replica.user}:${databases.replica.password}@${databases.replica.host}:${databases.replica.port}/${databases.replica.name}?sslmode=${connection_defaults.ssl_mode}"

[databases.cache]
driver = "redis"
host = "${REDIS_HOST}"
port = "${REDIS_PORT}"
password = "${REDIS_PASSWORD}"
url = "${databases.cache.driver}://:${databases.cache.password}@${databases.cache.host}:${databases.cache.port}"

[connection_pools]
primary_pool = {
    url = "${databases.primary.url}",
    min_size = 5,
    max_size = "${connection_defaults.pool_size}",
    timeout = "${connection_defaults.timeout}"
}
replica_pool = {
    url = "${databases.replica.url}",
    min_size = 2,
    max_size = 8,  
    timeout = "${connection_defaults.timeout}"
}
```

## Kubernetes Deployment

### Dynamic Manifest Generation

```toml
# k8s-config.toml  
[cluster]
name = "${CLUSTER_NAME}"
namespace = "${NAMESPACE}"
registry = "${CONTAINER_REGISTRY}"

[app]
name = "my-application"
version = "${APP_VERSION}"
replicas = "${REPLICA_COUNT}"
image = "${cluster.registry}/${app.name}:${app.version}"

[deployment]
name = "${app.name}-deployment"
labels = {
    app = "${app.name}",
    version = "${app.version}",
    environment = "${ENVIRONMENT}"
}

[service]
name = "${app.name}-service"
port = 80
target_port = 8080
type = "ClusterIP"

[ingress]
name = "${app.name}-ingress"
host = "${app.name}.${cluster.name}.${DOMAIN_SUFFIX}"
path = "/"
service_name = "${service.name}"
service_port = "${service.port}"

[config]
database_url = "${DATABASE_URL}"
redis_url = "${REDIS_URL}"  
api_key = "${API_KEY}"
log_level = "${LOG_LEVEL}"

[secrets]
db_password = "${DB_PASSWORD}"
jwt_secret = "${JWT_SECRET}"
```

Convert to Kubernetes YAML:
```bash
topl k8s-config.toml \
  --CLUSTER_NAME my-cluster \
  --NAMESPACE production \
  --APP_VERSION v1.2.3 \
  --REPLICA_COUNT 3 \
  --ENVIRONMENT production \
  | yq eval '.' -
```

## CI/CD Pipeline Configuration

### GitHub Actions Template

```toml
# ci-config.toml
[pipeline]
name = "${REPO_NAME}-ci"
trigger_branch = "main"
node_version = "18"
python_version = "3.11"

[environments.test]
name = "test"
database_url = "postgresql://test:test@localhost:5432/test_db"
api_url = "http://localhost:3000"

[environments.staging]  
name = "staging"
database_url = "${STAGING_DATABASE_URL}"
api_url = "https://staging-api.company.com"
deploy_url = "https://staging.company.com"

[environments.production]
name = "production"  
database_url = "${PRODUCTION_DATABASE_URL}"
api_url = "https://api.company.com"
deploy_url = "https://company.com"

[jobs.build]
name = "build-and-test"
runs_on = "ubuntu-latest"
steps = [
    "checkout",
    "setup-node-${pipeline.node_version}",
    "install-dependencies", 
    "run-tests",
    "build-application"
]

[jobs.deploy_staging]
name = "deploy-staging"
runs_on = "ubuntu-latest"
environment = "${environments.staging.name}"
needs = ["${jobs.build.name}"]
condition = "github.ref == 'refs/heads/main'"

[jobs.deploy_production]
name = "deploy-production"
runs_on = "ubuntu-latest"  
environment = "${environments.production.name}"
needs = ["${jobs.deploy_staging.name}"]
condition = "github.ref == 'refs/heads/main' && github.event_name == 'release'"
```

## Monitoring & Observability

### Comprehensive Monitoring Setup

```toml
# monitoring.toml
[metrics]
enabled = true
port = 9090
path = "/metrics"
interval = "15s"

[logging]
level = "${LOG_LEVEL}"
format = "json"
output = "stdout"

[tracing]
enabled = "${TRACING_ENABLED}"
endpoint = "${JAEGER_ENDPOINT}"
service_name = "${SERVICE_NAME}"
sample_rate = 0.1

[alerts]
slack_webhook = "${SLACK_WEBHOOK_URL}"
email_recipients = ["${ALERT_EMAIL}"]

[health_checks]
liveness_probe = {
    path = "/health/live",
    port = 8080,
    initial_delay = 30,
    period = 10
}
readiness_probe = {
    path = "/health/ready", 
    port = 8080,
    initial_delay = 5,
    period = 5
}

[prometheus]
scrape_configs = [
    {
        job_name = "${SERVICE_NAME}",
        static_configs = [{
            targets = ["localhost:9090"]
        }],
        scrape_interval = "${metrics.interval}"
    }
]
```

## Development Environment

### Local Development Setup

```toml
# dev-config.toml
[local]
project_name = "${PROJECT_NAME}"
developer = "${DEVELOPER_NAME}"
workspace = "${WORKSPACE_PATH}"

[database]
host = "localhost"
port = 5432
name = "${local.project_name}_dev"
user = "${local.developer}"
password = "dev_password"
url = "postgresql://${database.user}:${database.password}@${database.host}:${database.port}/${database.name}"

[redis]
host = "localhost"
port = 6379
url = "redis://${redis.host}:${redis.port}"

[api]
host = "localhost"
port = 8000
url = "http://${api.host}:${api.port}"
debug = true

[frontend]
host = "localhost"
port = 3000
url = "http://${frontend.host}:${frontend.port}"
api_url = "${api.url}"

[tools]
editor = "${EDITOR}"
browser = "${BROWSER}"
debugger_port = 5005

[scripts]
start_db = "docker run -d --name ${local.project_name}_db -e POSTGRES_DB=${database.name} -e POSTGRES_USER=${database.user} -e POSTGRES_PASSWORD=${database.password} -p ${database.port}:5432 postgres"
start_redis = "docker run -d --name ${local.project_name}_redis -p ${redis.port}:6379 redis"
start_api = "cd ${local.workspace}/backend && python manage.py runserver ${api.host}:${api.port}"
start_frontend = "cd ${local.workspace}/frontend && npm start"
```

## Configuration Validation

### Schema Definition

```toml
# schema-config.toml
[validation]
required_external_params = [
    "ENVIRONMENT",
    "DATABASE_URL", 
    "API_KEY",
    "SECRET_KEY"
]

[defaults]
timeout = 30
debug = false
log_level = "INFO"
port = 8080

[constraints]
environment_values = ["development", "staging", "production"]
log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
port_range = [1024, 65535]

[app]
name = "validated-app"
environment = "${ENVIRONMENT}"
debug = "${DEBUG}"
log_level = "${LOG_LEVEL}"
port = "${PORT}"

# Validation logic (would be implemented in code)
[validation_rules]
environment_check = "${app.environment} in ${constraints.environment_values}"
log_level_check = "${app.log_level} in ${constraints.log_levels}"
port_check = "${constraints.port_range[0]} <= ${app.port} <= ${constraints.port_range[1]}"
```

## Template Inheritance

### Base Configuration Template

```toml
# base.toml  
[common]
organization = "MyCompany"
domain = "${organization}.com"
protocol = "https"
version = "v1"

[defaults]
timeout = 30
retries = 3
log_level = "INFO"

[base_urls]
api = "${common.protocol}://api.${common.domain}/${common.version}"
web = "${common.protocol}://www.${common.domain}"
docs = "${common.protocol}://docs.${common.domain}"
```

```toml
# service-specific.toml (extends base.toml conceptually)
[service] 
name = "user-service"
port = 8080
endpoint = "${base_urls.api}/users"

[database]
host = "${DB_HOST}"
port = 5432
name = "${service.name}_db"  
url = "postgresql://${DB_USER}:${DB_PASSWORD}@${database.host}:${database.port}/${database.name}"

[external_services]
auth_service = "${base_urls.api}/auth"
notification_service = "${base_urls.api}/notifications"
```

## Best Practices Summary

### 1. Hierarchical Organization
```toml
[environments.${ENVIRONMENT}]
# Environment-specific values

[service_defaults]  
# Shared service configuration

[services.specific_service]
# Service-specific overrides
```

### 2. Parameter Naming Conventions
```toml
# Good: Descriptive, consistent naming
database_host = "${DB_HOST}"
api_secret_key = "${API_SECRET_KEY}"

# Avoid: Ambiguous abbreviations  
db_h = "${H}"
key = "${K}"
```

### 3. Providing Defaults
```toml
[defaults]
timeout = 30  # Default value
log_level = "INFO"  # Default value

[app]  
timeout = "${TIMEOUT}"  # Override with external param if provided
log_level = "${LOG_LEVEL}"  # Override with external param if provided
```

### 4. Documentation in Configuration
```toml
# Required external parameters:
# - ENVIRONMENT: deployment environment (dev/staging/prod)
# - DATABASE_URL: full database connection string
# - API_KEY: third-party service API key
# - SECRET_KEY: application secret for JWT signing

[app]
environment = "${ENVIRONMENT}"
database_url = "${DATABASE_URL}"
api_key = "${API_KEY}"
secret_key = "${SECRET_KEY}"
```

## What's Next?

- **Having issues?** → [Chapter 8: Troubleshooting](08-troubleshooting.md)
- **Want to contribute?** → [Chapter 9: Development & Contributing](09-development-contributing.md)
- **Need CLI help?** → [Chapter 5: CLI Reference](05-cli-reference.md)