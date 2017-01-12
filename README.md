#Jasper-HomeAutomation
Home automation module for [Jasper](http://jasperproject.github.io/).
Allows the ability to command devices and scenes through my home automation JSON API.

###Steps to install Jasper-HomeAutomation:
- Make sure the home automation server is running by going to the `server_url`,
e.g. `https://server_ip` or `http://server_ip:port`.
- Add the server url, username and password to `profile.yml`:
```
ha:
  server: <server_url>
  username: <username>
  password: <password>
```
- Clone this repo and copy HomeAutomation.py into jasper/client/modules/HomeAutomation.py

###Usage:
Assuming a bedtime scene has been defined
```
YOU: Run scene bedtime
JASPER: Running scene bedtime
```
