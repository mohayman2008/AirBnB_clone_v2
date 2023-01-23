#!/usr/bin/env bash
# Bash script that sets up the web servers for the deployment of web_static
# shellcheck disable=SC1004

# Install Nginx if it not already installed
sudo apt-get update && sudo apt-get -y install nginx
# nginx -v || (sudo apt-get update && sudo apt-get -y install nginx)

# Create the directories tree
sudo mkdir -p '/data/web_static/releases/test/'
sudo mkdir -p '/data/web_static/shared/'

# Deploy the current test realease
sudo ln -sf '/data/web_static/releases/test/' '/data/web_static/current'

# Manage the ownership of '/data' directory and all its contents
sudo chown -hR 'ubuntu':'ubuntu' '/data'

# Create a test index.html
echo 'AirBnB clone' > /data/web_static/releases/test/index.html

# Configure nginx to serve the contents of '/data/web_static/current/'
# + to location '/hbnb_static/'
CONF_FILE='/etc/nginx/sites-available/default'
rule_blk=\
'	location /hbnb_static/ {\
		alias /data/web_static/current/;\
	}'
rule='	alias /data/web_static/current/;\n'
if [ "$(grep -c -E '^\s*location\s*/hbnb_static/\s*{[ \t]*$' "$CONF_FILE")" -eq 0 ]; then
	sudo sed -z -E -i 's@(\n?([ \t]*)location\s*/\s*\{[^}]*\})@\1\n\n'"$rule_blk@" "$CONF_FILE"
else
	sudo sed -z -E -i 's@(\n?([ \t])*location\s*/hbnb_static/\s*\{)[^}]*\}@\1\n\2'"$rule"'\2\}@' "$CONF_FILE"
fi

# Make sure that default configuration is enabled 
sudo ln -sf "$CONF_FILE" /etc/nginx/sites-enabled/default

# Restart Nginx service 
sudo service nginx restart
