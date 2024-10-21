#!/bin/bash

# Define variables
APP_DIR="/home/pi/climbBackEnd"
APP_PORT="5000"
REPO_URL="https://github.com/computingify/climbBackEnd.git"  # Replace with your Git repository URL
FLASK_APP="main.py"
FLASK_ENV="production"
ETH_IP=$(ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)

# Step 1: Update system and install dependencies
echo "Updating system and installing dependencies..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip nginx git

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

# Step 5: Set up the Flask application
echo "Setting up the Flask application..."
export FLASK_APP=$FLASK_APP
export FLASK_ENV=$FLASK_ENV
export APP_PORT=$APP_PORT
export ETH_IP=$ETH_IP

# Step 6: Configure Nginx
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/climb_app <<EOF
server {
    listen 80;
    server_name $ETH_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias $APP_DIR/static;
    }
}
EOF

# Enable the Nginx configuration
sudo ln -s /etc/nginx/sites-available/climb_app /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Step 7: Create a systemd service file for the Flask app
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
ExecStart=$APP_DIR/venv/bin/flask --app $FLASK_APP run --host=0.0.0.0 --port=$APP_PORT

[Install]
WantedBy=multi-user.target
EOF

# Step 8: Start and enable the systemd service
echo "Starting and enabling the Flask app service..."
sudo systemctl start climb_app
sudo systemctl enable climb_app


# Get the IP address of the Ethernet interface (eth0)
echo "Deployment completed! Your app should now be accessible at http://$ETH_IP:$APP_PORT"
