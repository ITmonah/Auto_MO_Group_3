# lab2

## Run

```bash
docker compose up-d
```

Jenkins: [http://localhost:8080](http://localhost:8080)

```bash
docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

## Jenkins

Create a `Pipeline` job and paste the contents of `Jenkinsfile`.

Or

Use from SCM