# JARVIS Hydra Protocol - Multi-Cloud Regeneration
# ===============================================
# Terraform configuration for deploying cloned fallback instances
# to multiple cloud regions (AWS Tokyo, DigitalOcean SG)

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# AWS Tokyo Region
provider "aws" {
  region = "ap-northeast-1"
  alias  = "tokyo"
}

# DigitalOcean Singapore Region
provider "digitalocean" {
  token = var.do_token
}

# Variables
variable "aws_access_key" {
  description = "AWS access key"
  type        = string
  sensitive   = true
}

variable "aws_secret_key" {
  description = "AWS secret key"
  type        = string
  sensitive   = true
}

variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}

variable "jarvis_domain" {
  description = "JARVIS domain name"
  type        = string
  default     = "jarvis.devproflow.com"
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token for DNS management"
  type        = string
  sensitive   = true
}

variable "ssh_public_key" {
  description = "SSH public key for server access"
  type        = string
}

# AWS Tokyo - JARVIS Fallback Instance
resource "aws_instance" "jarvis_tokyo" {
  provider = aws.tokyo
  
  ami           = "ami-0c3c7b1d7c3b7b7b7"  # Ubuntu 22.04 LTS
  instance_type = "t3.medium"
  
  key_name = aws_key_pair.jarvis_tokyo.key_name
  
  tags = {
    Name        = "jarvis-fallback-tokyo"
    Environment = "production"
    Role        = "jarvis-fallback"
    Region      = "tokyo"
  }
  
  user_data = <<-EOF
              #!/bin/bash
              # JARVIS Fallback Instance Setup
              
              # Update system
              apt-get update -y
              apt-get upgrade -y
              
              # Install Node.js
              curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
              apt-get install -y nodejs
              
              # Install Docker
              curl -fsSL https://get.docker.com | sh
              systemctl start docker
              systemctl enable docker
              
              # Install PM2
              npm install -g pm2
              
              # Clone JARVIS repository
              git clone https://github.com/your-repo/jarvis-system.git /opt/jarvis-system
              cd /opt/jarvis-system
              
              # Install dependencies
              npm install
              
              # Start JARVIS in fallback mode
              pm2 start ecosystem.config.js --only jarvis-app
              pm2 save
              EOF
  
  vpc_security_group_ids = [aws_security_group.jarvis_tokyo.id]
  
  depends_on = [aws_key_pair.jarvis_tokyo]
}

resource "aws_key_pair" "jarvis_tokyo" {
  provider = aws.tokyo
  
  key_name   = "jarvis-tokyo"
  public_key = var.ssh_public_key
}

resource "aws_security_group" "jarvis_tokyo" {
  provider = aws.tokyo
  
  name        = "jarvis-tokyo-sg"
  description = "Security group for JARVIS Tokyo fallback"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 3001
    to_port     = 3001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 3002
    to_port     = 3002
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# DigitalOcean Singapore - JARVIS Fallback Instance
resource "digitalocean_droplet" "jarvis_sg" {
  name   = "jarvis-fallback-sg"
  region = "sgp1"
  size   = "s-2vcpu-4gb"
  image  = "ubuntu-22-04-x64"
  
  ssh_keys = [digitalocean_ssh_key.jarvis.fingerprint]
  
  tags = ["jarvis-fallback", "production"]
  
  user_data = <<-EOF
              #!/bin/bash
              # JARVIS Fallback Instance Setup
              
              # Update system
              apt-get update -y
              apt-get upgrade -y
              
              # Install Node.js
              curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
              apt-get install -y nodejs
              
              # Install Docker
              curl -fsSL https://get.docker.com | sh
              systemctl start docker
              systemctl enable docker
              
              # Install PM2
              npm install -g pm2
              
              # Clone JARVIS repository
              git clone https://github.com/your-repo/jarvis-system.git /opt/jarvis-system
              cd /opt/jarvis-system
              
              # Install dependencies
              npm install
              
              # Start JARVIS in fallback mode
              pm2 start ecosystem.config.js --only jarvis-app
              pm2 save
              EOF
}

resource "digitalocean_ssh_key" "jarvis" {
  name       = "jarvis"
  public_key = var.ssh_public_key
}

# Cloudflare DNS Management
resource "cloudflare_record" "jarvis_primary" {
  zone_id = var.cloudflare_zone_id
  name    = var.jarvis_domain
  value   = aws_instance.jarvis_tokyo.public_ip
  type    = "A"
  ttl     = 60
  proxied = true
}

resource "cloudflare_record" "jarvis_fallback_sg" {
  zone_id = var.cloudflare_zone_id
  name    = "sg.jarvis.devproflow.com"
  value   = digitalocean_droplet.jarvis_sg.ipv4_address
  type    = "A"
  ttl     = 60
  proxied = false
}

# Outputs
output "tokyo_instance_ip" {
  description = "Public IP of Tokyo fallback instance"
  value       = aws_instance.jarvis_tokyo.public_ip
}

output "sg_instance_ip" {
  description = "Public IP of Singapore fallback instance"
  value       = digitalocean_droplet.jarvis_sg.ipv4_address
}

output "primary_dns" {
  description = "Primary DNS record"
  value       = cloudflare_record.jarvis_primary.hostname
}
