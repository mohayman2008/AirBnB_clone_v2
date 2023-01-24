# Install Nginx if it not already installed
exec {'apt-get update':
  path => $path
}

package { 'nginx':
  ensure  => installed,
  require => Exec['apt-get update'],
  before  => Exec['add nginx firewall rule']
}

exec { 'add nginx firewall rule':
  provider => shell,
  command  => 'ufw allow \'Nginx HTTP\'',
  path     => $path
}
####

# Create the directories tree
file { '/data/web_static/releases/test/':
  ensure => directory
}

file { '/data/web_static/shared/':
  ensure => directory
}
####

# Deploy the current test realease
file { 'create current symlink':
  ensure => link,
  path   => '/data/web_static/current',
  target => '/data/web_static/releases/test/'
}

# Manage the ownership of '/data' directory and all its contents
file { '/data/':
  ensure  => directory,
  recurse => true,
  owner   => 'ubuntu',
  group   => 'ubuntu'
}

# Create a test index.html
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => 'AirBnB clone'
}
# exec { 'create index.html':
#   command => 'echo "AirBnB clone" > /data/web_static/releases/test/index.html',
#   path    => $path
# }

# Configure nginx to serve the contents of '/data/web_static/current/'
# + to location '/hbnb_static/' '\''
exec { 'nginx config':
  path     => $path,
  provider => shell,
  notify   => Service['nginx'],
  command  => 'bash -c \'
CONF_FILE=/etc/nginx/sites-available/default
rule_blk="\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}"
rule="\talias /data/web_static/current/;\n"
if [ "$(grep -c -E "^\\\\s*location\\\\s*/hbnb_static/\\\\s*{[ \\\\t]*$" "$CONF_FILE")" -eq 0 ]; then
	sudo sed -z -E -i "s@(\\\\n?([ \\\\t]*)location\\\\s*/\\\\s*\\\\{[^}]*\\\\})@\\\\1\\\\n\\\\n$rule_blk@" "$CONF_FILE"
else
	sudo sed -z -E -i "s@(\\\\n?([ \\\\t])*location\\\\s*/hbnb_static/\\\\s*\\\\{)[^}]*\\\\}@\\\\1\\\\n\\\\2$rule\\\\2\}@" "$CONF_FILE"
fi
  \''
}

# Make sure that default configuration is enabled
file { '/etc/nginx/sites-enabled/default':
  ensure => link,
  target => '/etc/nginx/sites-available/default'
}

# Restart Nginx service 
service { 'nginx':
  ensure  => running,
  path    => $path,
  restart => 'service nginx restart',
  require => Package['nginx']
}
