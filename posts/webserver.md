[category]: <> (devops)
[date]: <> (2022/05/30)
[title]: <> (Build your own web server)
[color]: <> (purple)

In this article we are going to build a Web-Server based on **Debian** (Linux) OS, using **Apache2**. We will also configure and secure the **SSH access**, so that we can securely access our server from a remote desktop.

I’m not gonna explain why you’d like to build an on-premise web server _(Privacy! 🔔)_. You can of course always [google it](https://letmegooglethat.com/?q=why+on+premise+web+server)!

### Let’s get right into the how-to build it 🏗️!

&nbsp;

**Requirements:**

- Have a dedicated machine _(old laptop, raspberry pi, cloud instance, etc)_
- A Pendrive _(to boot and install the new OS)_

**Steps:**

1.  Set up the operating system _(Linux)_
2.  Install and configure the webserver _(Apache)_
3.  Configure secure ssh access to your server
    &nbsp;

## Set up the operating system

### **Overview**

- Get iso image from the desired OS
- Burn image into Pendrive
- Boot system from the Pendrive
- Install new OS

You can use any Linux distro of preference for the OS, In this case I’ll use **Debian**. It’s well suited for web servers and it’s relatively easy to get started with.

Similar options can be Ubuntu, Linux Mint, or for more experienced people Gentoo.
&nbsp;

**Start:**

- Download the **Debian ISO image** from the Debian official site: [Debian .iso](https://www.debian.org/CD/http-ftp/).

- Let’s **burn the ISO image into the Pendrive**. You can use [pendrivelinux.com](https://www.pendrivelinux.com/) to do this.

  ![Pendrive ISO burner](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/webserver/boot-from-usb.webp)\

  I’m using Ubuntu, thus I’ll also add the steps on how to do it from Ubuntu itself: [bootable-usb-from-ubuntu](https://ubuntu.com/tutorials/create-a-usb-stick-on-ubuntu#1-overview).

- **Boot from our Pendrive**; First we need to enter BIOS setup.

  – Restart your computer

  – While the startup screen is loading, to enter BIOS; Press ESC, F8, F9, or Option (depending on the manufacturer)

  – Navigate to “Boot” menu using the arrow keys and select your USB Disk as the Boot Option #1

  – Press F10 to save and quit

  ![BIOS](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/webserver/bios.jpg)\
  &nbsp;

- Once your computer boots from USB, you’ll go through the **Debian installation process**

**Recommendations for installing Debian:**

– Select Debian as Web-Server option and disable Desktop functionality _(we only need web-server capabilities)_

– Select "All files in one partition" _(this is recommended for new users)_

&nbsp;

** Debian homescreen**

![Debian OS](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/webserver/debian11.jpg)\
&nbsp;

> **Congrats!** You have now Debian OS up and running 🏃🏃‍♀️!
> &nbsp;

## Install and configure the webserver

### **Overview**

- Update system repositories
- Install Apache2
- Configure webserver
- Test web server
  &nbsp;

**On your terminal,**

#### Let’s start by updating the packages.

    sudo apt update

--– _If your account doesn’t have sudo rights, switch to the root user by running `su -`_

#### Install Apache2 by running

    sudo apt install apache2

#### Verify installation by running

    apache2 -version

#### Configure the Firewall settings (if it’s running in your system)

    sudo ufw allow 80/tcp # (default network port used to send and receive unencrypted web pages)

    sudo ufw allow 443/tcp # (network port used to make secured and encrypted data - HTTPS)

#### Verify port settings

    sudo ufw status

#### Verify Apache2 is active by running:

    sudo systemctl status apache2

_The response should similar to:_
![Check Apache Status](https://www.tecmint.com/wp-content/uploads/2019/08/Check-Apache-Status.png)\
_Credits to_ [_tecmint.com_](http://tecmint.com/) _for the image_

--- _If the server is not running, you can start it by running:_

    sudo systemctl start apache2 **or** sudo systemctl restart apache2

#### Get your server IP address _(hostname)_ by running:

    hostname -I

#### **Access your web server!**

Open the browser and navigate to [http://your-server-IP-address](http://your-server-ip-address/) (e.g. [http://192.173.43.21](http://192.173.43.21/))

**Apache2's Home page**
![Web Server Homepage](https://assets.digitalocean.com/how-to-install-lamp-debian-9/small_apache_default_debian9.png)\

&nbsp;

> **Congrats!** You now have your own web server ✨!
> &nbsp;

## #3 - Secure SSH access to manage your server

### **Overview**

- Configure login access
- Create public keys to ssh into our server
  &nbsp;

I would like to ideally manage my server from a remote computer, thus let’s configure it to have secure SSH access.

**SSH Key access**

It’s recommended to enter your server by using SSH Keys instead of passwords since it’s a more secure way to do so.

&nbsp;

**How to:**

#### Switch to your local user profile that will be accessing the server

    su username

— _It’s best practice neither to use root nor admin users_

#### Generate a new key pair

    ssh-keygen -t rsa

— _It’s recommended to add a catchphrase when generating the key since it adds an extra layer of security_

#### Check that the public key was created successfully

    ls ~/.ssh/id_*

#### Copy the key to your remote server

    ssh-copy-id -i ~/.ssh/id_rsa.pub remote_username@your_server_ip_address

#### Validate that the key was added successfully

    ssh remote_username@your_server_ip_address

&nbsp;

**SSH access configuration:**

Navigate to `/etc/ssh/sshd_config` and within the file:
&nbsp;

#### Change 22 Port

Change port 22 to any non-default port: e.g. `Port 20155`
&nbsp;

#### Disable Root logins

Set `#PermitRootLogin` as `noPermitRootLogin no`
&nbsp;

#### Disable empty passwords

Set `#PermitEmptyPasswords` as `PermitEmptyPasswords no`
&nbsp;

#### Enable Protocol 2

Add the line `Protocol 2` to the file.
&nbsp;

#### Limit for password attends

Set `#MaxAuthTries` to `MaxAuthTries 3`

_or Disable password authentication altogether_
_(Important -– Please make sure you already have SSH Key access before disabling it)_
— Set `#PasswordAuthentication` as `PasswordAuthentication no`

&nbsp;

Now, restart SSH service to apply our changes

#### Restart ssh by running:

    systemctl restart ssh

&nbsp;

**Let's finally test our changes!**

#### SSH into your server using your keys

    ssh remote_username@your_server_ip_address -p your_server_port_number

![Log in into server](https://raw.githubusercontent.com/Danielratmiroff/myblog/master/images/webserver/login.jpg)\

&nbsp;

> **Woohoo!** You can now SSH into your server 🔥 !
