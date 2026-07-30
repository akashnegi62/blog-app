import requests


JENKINS_URL="http://43.204.63.127:8080/"

JOB="SeedJob"


USERNAME="admin"

TOKEN="11e3c3bcd4ac611538526106b9a0cbd12b"



url=f"{JENKINS_URL}/job/{JOB}/build"



response=requests.post(

    url,

    auth=(USERNAME,TOKEN)

)



if response.status_code==201:

    print("Seed Job Started")


else:

    print(response.text)
