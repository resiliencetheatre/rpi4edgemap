# kamailio

These are work in progress configurations for kamailio sip server. 

Note that these configurations are not used from this directory.
Check /usr/lib/kamailio/ and /etc/kamailio instead.

Note that you need modified /sbin/kamctl 

On line 73: 

 MYLIBDIR="/usr/lib/kamailio/kamctl/kamctl"

You need to change that path. Maybe there is more elegant way to
install these files during build process, but this is my take now.

Buildroot overlay contains that modified /sbin/kamctl - remember to
alter it if you update kamailio from version I've used.

## sqlite3

I like using sqlite3 because the I can have DB as one file, makes 
life easier.

Database (dbtest) and configs location:

 /etc/kamailion

Run directory for kamdbctl

 /usr/lib/kamailio/kamctl/kamctl

Create initial DB

 cd /usr/lib/kamailio/kamctl/kamctl
 kamdbctl create

Optional reinit

 kamdbctl reinit 

Create users

 export SIP_DOMAIN=192.168.1.242
 kamctl add test secret
 kamctl add test1 secret
