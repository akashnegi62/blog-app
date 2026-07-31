import yaml
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python onboard.py projects/<project>.yml")
    sys.exit(1)

config_file = sys.argv[1]

with open(config_file, "r") as f:
    data = yaml.safe_load(f)

project = data["project"]
github = data["github"]
docker = data["docker"]
aws = data["aws"]
jenkins = data["jenkins"]

# -----------------------------
# Generate Jenkins Job DSL
# -----------------------------

dsl_template = "jenkins/jobs/pipelineJob.groovy.template"

with open(dsl_template) as f:
    job = f.read()

job = (
    job.replace("{{FOLDER}}", project["folder"])
       .replace("{{NAME}}", project["name"])
       .replace("{{APP_REPO}}", github["repo"])
       .replace("{{APP_BRANCH}}", github["branch"])
       .replace("{{GITHUB_CREDENTIALS}}", jenkins["credentialsId"])
)

os.makedirs("jenkins/jobs", exist_ok=True)

dsl_output = f"jenkins/jobs/{project['name']}.groovy"

with open(dsl_output, "w") as f:
    f.write(job)

print(f"✔ Jenkins Job DSL created : {dsl_output}")

# -----------------------------
# Generate Jenkinsfile
# -----------------------------

template = "templates/Jenkinsfile.template"

with open(template) as f:
    pipeline = f.read()

pipeline = (
    pipeline.replace("{{PROJECT_NAME}}", project["name"])
            .replace("{{DOCKER_IMAGE}}", docker["image"])
            .replace("{{STACK_NAME}}", aws["stackName"])
            .replace("{{REGION}}", aws["region"])
            .replace("{{INSTANCE_TYPE}}", aws["instanceType"])
            .replace("{{KEY_NAME}}", aws["keyName"])
)

output_file = "Jenkinsfile"

with open(output_file, "w") as f:
    f.write(pipeline)

print(f"✔ Jenkinsfile created: {output_file}")

print("\n====================================")
print(f"Project : {project['name']}")
print("Onboarding completed successfully.")
print("====================================")