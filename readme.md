# 📂 Lern-Fair-File-Sharing Backend

## 📝 Description
This repository holds the docker-compose file for our nextcloud backend as well as a documentation for the nextcloud features, we need to access.

## 📦 Content

### 📄 .env file
An example debugging configuration for the variables in your dockerfile. WARNING: Don't use this in a production environment

### 📡 API Calls
All relevant API calls are collected in our postman json that you can find [here](https://github.com/lern-fair-file-sharing/backend/tree/master/documentation)
To load it into postman, navigate to Under File -> Import -> then past .json content into "raw", additionally you have to set your username and password

### 💻 Commandline Instructions
Coming soon...

## 🚀 How to setup the docker nextcloud container
- Execute these commands on your commandline
```bash
git clone git@github.com:lern-fair-file-sharing/backend.git #or the http version if you're not a maintainer
cd backend
docker compose up -d
```
*for now we have to manually add a new admin account, this should be fixed in the future*
- after this, open [http://localhost:8080](http://localhost:8080) and register the admin account with a username and password
- now your nextcloud instance is good to go, as long as you don't delete the container in you docker environment, you don't have to do these steps everytime you want to use this. Just start docker and the backend will start automatically.

## ⚙️ Nextcloud functionality access

### 🌐 Webdav

#### 📝 Description
Webdav is a network protcol that allows us to handle the data of users. You can use Webdav API calls as is to retrieve an XML as a response 

#### 🖥️ Webdav Clients
Since webdav is an open standard you can use services like [webdav-fd](https://www.npmjs.com/package/webdav-fs) which will most certainly not support all possible functionality supplied by nextcloud but are easier to implement. Also check these links, if you want to implement this in the frontend: [StackOverflow](https://stackoverflow.com/questions/58258153/is-it-possible-to-make-a-webdav-client-in-react-native-without-the-need-of-nativ),[NextCloudBlog](https://nextcloud.com/de/blog/using-webdav-fs-to-access-files-in-nextcloud/)

#### 🛠️ API Functionality
The Webdav functionality is documented [here](https://docs.nextcloud.com/server/19/developer_manual/client_apis/WebDAV/basic.html).
For tested functions check out the [postmanfile](https://github.com/lern-fair-file-sharing/backend/tree/master/documentation).

### 🌐 OCS (Open Collaborative Services)

#### 📝 Description
Has it's roots as a Rest API originally from Social Desktop. Here with Nextcloud: Advanced features that would usually require an admin console like adding a new user

#### 🛠️ API Functionality
The OCS functionality is documented [here](https://docs.nextcloud.com/server/19/developer_manual/client_apis/OCS/ocs-api-overview.html).
For tested functions check out the [postmanfile](https://github.com/lern-fair-file-sharing/backend/tree/master/documentation).
