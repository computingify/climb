#!/bin/bash

# Define variables
APP_DIR="/home/pi/climbBackEnd"
APP_PORT="5000"
REPO_URL="https://github.com/computingify/climbBackEnd.git"  # Replace with your Git repository URL
FLASK_APP="main.py"
FLASK_ENV="production"
ETH_IP=$(ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1) # The IP address of the device where we are
JQUERY_VERSION="3.7.1"
JQUERY_FILE="jquery-$JQUERY_VERSION.slim.js"
STATIC_DIR="$APP_DIR/web_pages/js/thirdParty"

# Step 1: Update system and install dependencies
echo "Updating system and installing dependencies..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip nginx git curl

# Step 2: Clone the repository if it doesn't exist
if [ ! -d "$APP_DIR" ]; then
    echo "Cloning the repository..."
    git clone "$REPO_URL" "$APP_DIR"
fi

# Step 3: Set up a Python virtual environment
echo "Setting up a Python virtual environment..."
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate

# Step 4: Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Download jQuery if it doesn't exist
echo "Downloading jQuery..."
mkdir -p "$STATIC_DIR"
if [ ! -f "$STATIC_DIR/$JQUERY_FILE" ]; then
    curl -o "$STATIC_DIR/$JQUERY_FILE" "https://code.jquery.com/$JQUERY_FILE"
fi

# Step 6: Set up the Flask application
echo "Setting up the Flask application..."
export FLASK_APP=$FLASK_APP
export FLASK_ENV=$FLASK_ENV
export APP_PORT=$APP_PORT
export ETH_IP=$ETH_IP

# Step 7: Configure Nginx
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/climb_app <<EOF
server {
    listen 443 ssl;
    server_name $ETH_IP;

    ssl_certificate /etc/letsencrypt/live/$ETH_IP/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$ETH_IP/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias $APP_DIR/static;
    }

    server {
        listen 80;
        server_name $ETH_IP;
        return 301 https://$host$request_uri;
    }
}
EOF

# Enable the Nginx configuration
sudo ln -s /etc/nginx/sites-available/climb_app /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Step 8: Create a systemd service file for the Flask app
echo "Creating a systemd service for the Flask app..."
sudo tee /etc/systemd/system/climb_app.service <<EOF
[Unit]
Description=Gunicorn instance to serve climbBackEnd
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 main:app

[Install]
WantedBy=multi-user.target
EOF

# Step 9: Start and enable the systemd service
echo "Starting and enabling the Flask app service..."
sudo systemctl start climb_app
sudo systemctl enable climb_app

# Get the IP address of the Ethernet interface (eth0)
echo "Deployment completed! Your app should now be accessible at http://$ETH_IP:$APP_PORT"