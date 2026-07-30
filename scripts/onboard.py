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
# Create Jenkins Job DSL
# -----------------------------
dsl_template = "jenkins/jobs/pipelineJob.groovy.template"

with open(dsl_template, "r") as f:
    job = f.read()

job = (
    job.replace("{{FOLDER}}", project["folder"])
       .replace("{{NAME}}", project["name"])
       .replace("{{REPO}}", github["repo"])
       .replace("{{BRANCH}}", github["branch"])
       .replace("{{CREDENTIALS}}", jenkins["credentialsId"])
)

os.makedirs("jenkins/jobs", exist_ok=True)

dsl_output = f"jenkins/jobs/{project['name']}.groovy"

with open(dsl_output, "w") as f:
    f.write(job)

print(f"✔ Jenkins Job DSL created : {dsl_output}")

# -----------------------------
# Create Jenkinsfile
# -----------------------------
jenkinsfile_template = "templates/Jenkinsfile.template"

with open(jenkinsfile_template, "r") as f:
    pipeline = f.read()

pipeline = (
    pipeline.replace("{{PROJECT_NAME}}", project["name"])
            .replace("{{APP_REPO}}", github["repo"])
            .replace("{{APP_BRANCH}}", github["branch"])
            .replace("{{GITHUB_CREDENTIALS}}", jenkins["credentialsId"])
            .replace("{{DOCKER_IMAGE}}", docker["image"])
            .replace("{{STACK_NAME}}", aws["stackName"])
            .replace("{{REGION}}", aws["region"])
            .replace("{{INSTANCE_TYPE}}", aws["instanceType"])
            .replace("{{KEY_NAME}}", aws["keyName"])
)

output_dir = f"generated/jenkinsfiles/{project['name']}"

os.makedirs(
    output_dir,
    exist_ok=True
)

jenkinsfile_output = f"{output_dir}/Jenkinsfile"

with open(jenkinsfile_output, "w") as f:
    f.write(pipeline)

print(f"✔ Jenkinsfile created : {jenkinsfile_output}")

print("\n====================================")
print(f"Project : {project['name']}")
print("Onboarding completed successfully.")
print("====================================")