#!/bin/bash

# Define variables
APP_DIR="/home/pi/climbBackEnd"
REPO_URL="https://github.com/computingify/climbBackEnd.git"  # Replace with your Git repository URL
FLASK_APP="main.py"
FLASK_ENV="production"

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

# Step 6: Configure Nginx
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/climb_app <<EOF
server {
    listen 80;
    server_name 192.168.0.78;

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
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 main:app

[Install]
WantedBy=multi-user.target
EOF

# Step 8: Start and enable the systemd service
echo "Starting and enabling the Flask app service..."
sudo systemctl start climb_app
sudo systemctl enable climb_app

echo "Deployment completed! Your app should now be accessible at http://192.168.0.78:5000"
