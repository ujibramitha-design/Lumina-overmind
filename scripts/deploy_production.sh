#!/bin/bash

# LUMINA OS - Production Deployment Script
# Domain: lumina.devproflow.com
# Infrastructure: Cloudflare + Docker Compose

set -e  # Exit on any error

echo "🚀 Starting LUMINA OS Production Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="lumina.devproflow.com"
COMPOSE_FILE="docker-compose.production.yml"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Check if docker-compose.production.yml exists
if [ ! -f "$COMPOSE_FILE" ]; then
    print_error "$COMPOSE_FILE not found."
    exit 1
fi

# Load environment variables
source .env

print_status "Environment variables loaded successfully."

# Check required environment variables
required_vars=("DATABASE_PASSWORD" "REDIS_PASSWORD" "ENCRYPTION_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        print_error "Required environment variable $var is not set."
        exit 1
    fi
done

print_status "Required environment variables verified."

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs/nginx logs/app uploads backups data/postgres data/redis public/maintenance

# Set proper permissions
chmod 755 logs uploads backups data
chmod 600 .env

# Stop existing services
print_status "Stopping existing services..."
docker-compose -f $COMPOSE_FILE down

# Pull latest images
print_status "Pulling latest Docker images..."
docker-compose -f $COMPOSE_FILE pull

# Build services
print_status "Building Docker images..."
docker-compose -f $COMPOSE_FILE build --no-cache

# Start database services first
print_status "Starting database services..."
docker-compose -f $COMPOSE_FILE up -d postgres redis

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 30

# Run database migrations
print_status "Running database migrations..."
docker-compose -f $COMPOSE_FILE run --rm backend python -m alembic upgrade head

# Start all services
print_status "Starting all services..."
docker-compose -f $COMPOSE_FILE up -d

# Wait for services to be healthy
print_status "Waiting for services to be healthy..."
sleep 60

# Check service health
print_status "Checking service health..."

services=("backend" "frontend" "nginx")
for service in "${services[@]}"; do
    health=$(docker-compose -f $COMPOSE_FILE ps -q $service | xargs docker inspect --format='{{.State.Health.Status}}' 2>/dev/null || echo "unknown")
    if [ "$health" == "healthy" ]; then
        print_status "$service is healthy"
    else
        print_warning "$service health status: $health"
    fi
done

# Show running services
print_status "Running services:"
docker-compose -f $COMPOSE_FILE ps

# Show logs for any errors
print_status "Recent logs:"
docker-compose -f $COMPOSE_FILE logs --tail=50

# Test connectivity
print_status "Testing connectivity to $DOMAIN..."

# Test HTTP
if curl -f -s -o /dev/null -w "%{http_code}" "http://$DOMAIN/health" | grep -q "200"; then
    print_status "HTTP connectivity test passed"
else
    print_warning "HTTP connectivity test failed"
fi

# Test HTTPS
if curl -f -s -o /dev/null -w "%{http_code}" "https://$DOMAIN/health" | grep -q "200"; then
    print_status "HTTPS connectivity test passed"
else
    print_warning "HTTPS connectivity test failed"
fi

# Test API
if curl -f -s -o /dev/null -w "%{http_code}" "https://$DOMAIN/api/health" | grep -q "200"; then
    print_status "API connectivity test passed"
else
    print_warning "API connectivity test failed"
fi

print_status "Deployment completed successfully!"
print_status "Your LUMINA OS is now running at: https://$DOMAIN"
print_status "Flower monitoring is available at: http://localhost:5555 (if enabled)"

# Show useful commands
echo ""
print_status "Useful commands:"
echo "  View logs: docker-compose -f $COMPOSE_FILE logs -f [service]"
echo "  Stop services: docker-compose -f $COMPOSE_FILE down"
echo "  Restart services: docker-compose -f $COMPOSE_FILE restart [service]"
echo "  Update services: docker-compose -f $COMPOSE_FILE pull && docker-compose -f $COMPOSE_FILE up -d"

# Security reminders
echo ""
print_warning "Security reminders:"
echo "  1. Ensure your SSL certificates are properly configured in Cloudflare"
echo "  2. Set up Cloudflare Firewall rules for additional protection"
echo "  3. Monitor logs for any suspicious activity"
echo "  4. Keep your Docker images and dependencies updated"
echo "  5. Regularly backup your database and configuration"

print_status "Deployment script completed successfully! 🎉"
