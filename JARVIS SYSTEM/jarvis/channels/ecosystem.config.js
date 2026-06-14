/**
 * PM2 Ecosystem Configuration for JARVIS Communication Hub
 * ======================================================
 * 
 * This configuration file manages the JARVIS communication channels
 * as a daemon process using PM2 process manager.
 * 
 * Usage:
 *   pm2 start ecosystem.config.js
 *   pm2 save
 *   pm2 startup
 * 
 * Commands:
 *   pm2 list                    # List all processes
 *   pm2 logs jarvis-hub         # View logs
 *   pm2 restart jarvis-hub      # Restart process
 *   pm2 stop jarvis-hub         # Stop process
 *   pm2 delete jarvis-hub       # Delete process
 *   pm2 monit                   # Monitor processes
 */

module.exports = {
  apps: [
    {
      name: 'jarvis-hub',
      script: './hub.js',
      cwd: __dirname,
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        JARVIS_WHATSAPP_ENABLED: 'true',
        JARVIS_TELEGRAM_ENABLED: 'true',
        JARVIS_HEALTH_CHECK_PORT: '3001'
      },
      env_development: {
        NODE_ENV: 'development',
        JARVIS_WHATSAPP_ENABLED: 'true',
        JARVIS_TELEGRAM_ENABLED: 'true',
        JARVIS_DEBUG: 'true',
        JARVIS_LOG_LEVEL: 'debug'
      },
      error_file: './logs/jarvis-hub-error.log',
      out_file: './logs/jarvis-hub-out.log',
      log_file: './logs/jarvis-hub-combined.log',
      time: true,
      merge_logs: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000,
      kill_timeout: 5000,
      wait_ready: true,
      listen_timeout: 10000,
      shutdown_with_message: true,
      // Graceful shutdown handling
      stop_timeout: 5000,
      // Process management
      exec_mode: 'fork',
      // Monitoring
      monitoring: true,
      // PM2 Plus integration (optional)
      pm2: true
    }
  ],

  // Deployment configuration (optional, for remote deployment)
  deploy: {
    production: {
      user: 'node',
      host: 'your-server.com',
      ref: 'origin/main',
      repo: 'git@github.com:your-repo/lumina-overmind.git',
      path: '/var/www/lumina-overmind',
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env production'
    },
    staging: {
      user: 'node',
      host: 'staging-server.com',
      ref: 'origin/develop',
      repo: 'git@github.com:your-repo/lumina-overmind.git',
      path: '/var/www/lumina-overmind-staging',
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env staging'
    }
  }
};
