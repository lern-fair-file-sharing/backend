# 📂 Lern-Fair-File-Sharing Backend

## 📝 Description
This repository holds all files necessary to start our NextCloud instance using Docker and as well as a documentation for the NextCloud API features, we need to use.

## 📦 Content

### 📄 .env file
Create a .env file with the following variables:
```
NCUSR=<nextcloud-user>
NCPW=<nextcloud-password>
```
An examplary .env file is included, but pleae don't use this in a production environment.

### NextCloud secrets:
Inside the ``./secrets/`` folder create the following files:
- ``nextcloud_admin_password.txt``: In here put the admin password
- ``nextcloud_admin_user.txt``: In here put the admin user name
- ``postgres_db.txt``: In here put the database name "postgresdb"
- ``postgres_password.txt``: In here put the postgres user password
- ``postgres_user.txt``: In here simply the postgres user name
Examplary secrets are included, but pleae don't use them in a production environment.

## 🚀 How to setup the docker nextcloud container
1. Execute these commands on your command line:
   ```bash
   git clone git@github.com:lern-fair-file-sharing/backend.git
   cd backend
   docker compose up -d
   ```
   
   After this the NextCloud instance will be starting and the admin user automatically created.
   You can visit NextCloud at [http://localhost:8080](http://localhost:8080) (or whatever port you specified) and register as the admin.
   
2. Our application requires a specific folder structure which contains dummy files (see [./example-folder-structure/](/example-folder-structure/)). To create it execute the script [initialization.py](./initialization.py). Make sure you have the [requests](https://pypi.org/project/requests/) package installed.

As long as you don't delete the container and volumes, you don't have to do these steps everytime you want to use this. Just start docker and the backend will start automatically. But if you need to reset the NextCloud instance use the following command:
```bash
docker compose down -v
```

## ⚙️ Nextcloud API Access

### 🌐 Webdav

#### 📝 Description
Webdav is a network protcol that allows us to handle the data of users. You can use Webdav API calls as is to retrieve an XML as a response.
Since webdav is an open standard you can use services like [webdav-fd](https://www.npmjs.com/package/webdav-fs) which will most certainly not support all possible functionality supplied by nextcloud but are easier to implement. Also check these links, if you want to implement this in the frontend: [StackOverflow](https://stackoverflow.com/questions/58258153/is-it-possible-to-make-a-webdav-client-in-react-native-without-the-need-of-nativ), [NextCloud Blog](https://nextcloud.com/de/blog/using-webdav-fs-to-access-files-in-nextcloud/), [Webdav Docs](https://docs.nextcloud.com/server/19/developer_manual/client_apis/WebDAV/basic.html)

#### 🛠️ API Functionality
Here you can find a collection of API endpoint descriptions ready to test using Postman: [Postman JSON File](https://github.com/lern-fair-file-sharing/backend/tree/master/documentation).
In Postman navigate to File -> Import -> then paste .json content into "raw", additionally you have to set your username and password in the headers as basic HTTP Authentication.

### 🌐 OCS (Open Collaborative Services)
#### 📝 Description
OCS provides advanced features for NextCloud using the corresponding CLI tool. This can be used by admins to, for example, create new suers and manage other administrative parts of their NextCloud instance.

#### 🧑‍💻 CLI Functionality
The OCS functionality is documented [here](https://docs.nextcloud.com/server/19/developer_manual/client_apis/OCS/ocs-api-overview.html).
You can use the Dcker [exec](https://docs.docker.com/reference/cli/docker/container/exec/) command to opt-into you container running the NextCloud instance and execute OCS commands from there.