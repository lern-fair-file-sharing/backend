# 📂 Lern-Fair-File-Sharing Backend

## 📝 Description
This repository holds all files necessary to start our NextCloud instance using Docker, as well as documentation for the NextCloud API features we need to use.

## 📦 Content

⚠️ Exemplary files are included. You don't need to create them for testing. Please don't use them in a production environment!

### 📄 .env file

Create a .env file with the following variables:
```
NCUSR=<nextcloud-user>
NCPW=<nextcloud-password>
```

### NextCloud secrets:
Inside the ``./secrets/`` folder, create the following files:
- ``nextcloud_admin_password.txt``: In here, put the admin password
- ``nextcloud_admin_user.txt``: In here, put the admin user name
- ``postgres_db.txt``: In here, put the database name "postgresdb"
- ``postgres_password.txt``: In here, put the postgres user password
- ``postgres_user.txt``: In here, simply put the postgres username



## 🚀 How to set up the docker Nextcloud container

⚠️ Warning: This container does not run on Windows. Windows Users should [install WSL2](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers)

1. Execute these commands on your command line:

   ```bash
   git clone git@github.com:lern-fair-file-sharing/backend.git
   cd backend
   docker compose up -d
   ```
   
   After this, the Nextcloud instance will start, and the admin user will automatically be created.
   You can visit Nextcloud at [http://localhost:8080](http://localhost:8080) (or whatever port you specified) and register as the admin.
   
2. Our application requires a specific folder structure that contains dummy files (see [./example-folder-structure/](/example-folder-structure/)). To create it, execute the script [initialization.py](./initialization.py). Make sure you have the [request](https://pypi.org/project/requests/) package installed.

   ```bash
   python ./initialization.py    
   ```

As long as you don't delete the container and volumes, you don't have to do these steps every time you want to use it. Just start Docker, and the backend will start automatically. But if you need to reset the Nextcloud instance, use the following command:
```bash
docker compose down -v
```

## ⚙️ Nextcloud API Access

### 🌐 WebDAV

#### 📝 Description
WebDAV is a network protocol that allows us to handle the data of users. You can use WebDAV API calls as is to retrieve an XML response.
Since WebDAV is an open standard, you can use services like [webdav-fd](https://www.npmjs.com/package/webdav-fs) which will most certainly not support all possible functionality supplied by Nextcloud but are easier to implement. Also check these links, if you want to implement this in the frontend: [Stack Overflow](https://stackoverflow.com/questions/58258153/is-it-possible-to-make-a-webdav-client-in-react-native-without-the-need-of-nativ), [Nextcloud Blog](https://nextcloud.com/de/blog/using-webdav-fs-to-access-files-in-nextcloud/), [Webdav Docs](https://docs.nextcloud.com/server/19/developer_manual/client_apis/WebDAV/basic.html)

#### 🛠️ API Functionality
Here you can find a collection of API endpoint descriptions ready to test using Postman: [Postman JSON File](https://github.com/lern-fair-file-sharing/backend/tree/master/documentation).
In Postman, navigate to File -> Import -> then paste .json content into "raw", additionally you have to set your username and password in the headers as basic HTTP Authentication.

### 🌐 OCS (Open Collaborative Services)
#### 📝 Description
OCS provides advanced features for Nextcloud using the corresponding CLI tool. This can be used by admins to, for example, create new suers and manage other administrative parts of their Nextcloud instance.

#### 🧑‍💻 CLI Functionality
The OCS functionality is documented [here](https://docs.nextcloud.com/server/19/developer_manual/client_apis/OCS/ocs-api-overview.html).
You can use the Docker [exec](https://docs.docker.com/reference/cli/docker/container/exec/) command to access your container running the Nextcloud instance and execute OCS commands from there
