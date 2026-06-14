/**
 * PM2 Ecosystem Configuration for JARVIS System
 * ==============================================
 * 
 * Process manager configuration for auto-restart and monitoring
 * of all JARVIS components (Hub, Backend, Health Monitor, etc.)
 */

module.exports = {
  apps: [
    // JARVIS Communication Hub (WhatsApp + Telegram)
    {
      name: 'jarvis-hub',
      script: './channels/hub.js',
      cwd: __dirname,
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        JARVIS_WHATSAPP_ENABLED: 'true',
        JARVIS_TELEGRAM_ENABLED: 'true',
        JARVIS_HEALTH_CHECK_PORT: '3001',
      },
      env_development: {
        NODE_ENV: 'development',
        JARVIS_DEBUG: 'true',
        JARVIS_LOG_LEVEL: 'debug',
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
      exec_mode: 'fork',
      monitoring: true,
      pm2: true,
    },

    // JARVIS Python Backend (Health Monitor, Memory Pruning, Terminal Executor)
    {
      name: 'jarvis-backend',
      script: './main.py',
      cwd: __dirname,
      interpreter: 'python',
      interpreter_args: '-u',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '2G',
      env: {
        PYTHONUNBUFFERED: '1',
        JARVIS_SERVICE_TOKEN: process.env.JARVIS_SERVICE_TOKEN || 'default_token',
        JARVIS_MEMORY_DB_PATH: './data/jarvis_memory.db',
        JARVIS_CODE_INDEX_PATH: './data/code_index',
      },
      env_development: {
        JARVIS_DEBUG: 'true',
        JARVIS_LOG_LEVEL: 'debug',
      },
      error_file: './logs/jarvis-backend-error.log',
      out_file: './logs/jarvis-backend-out.log',
      log_file: './logs/jarvis-backend-combined.log',
      time: true,
      merge_logs: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000,
      kill_timeout: 5000,
      exec_mode: 'fork',
      monitoring: true,
    },

    // JARVIS Health Monitor (standalone process)
    {
      name: 'jarvis-health-monitor',
      script: './health_monitor.py',
      cwd: __dirname,
      interpreter: 'python',
      interpreter_args: '-u',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '512M',
      env: {
        PYTHONUNBUFFERED: '1',
        JARVIS_SERVICE_TOKEN: process.env.JARVIS_SERVICE_TOKEN || 'default_token',
      },
      error_file: './logs/jarvis-health-monitor-error.log',
      out_file: './logs/jarvis-health-monitor-out.log',
      log_file: './logs/jarvis-health-monitor-combined.log',
      time: true,
      merge_logs: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000,
      exec_mode: 'fork',
    },

    // JARVIS Scheduler (for cron jobs)
    {
      name: 'jarvis-scheduler',
      script: './scheduler.py',
      cwd: __dirname,
      interpreter: 'python',
      interpreter_args: '-u',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '256M',
      env: {
        PYTHONUNBUFFERED: '1',
        JARVIS_MEMORY_PRUNING_ENABLED: 'true',
        JARVIS_MEMORY_PRUNING_TIME: '02:00',
        JARVIS_MORNING_GREETING_ENABLED: 'true',
        JARVIS_MORNING_GREETING_TIME: '08:00',
        JARVIS_DAILY_SUMMARY_ENABLED: 'true',
        JARVIS_DAILY_SUMMARY_TIME: '18:00',
      },
      error_file: './logs/jarvis-scheduler-error.log',
      out_file: './logs/jarvis-scheduler-out.log',
      log_file: './logs/jarvis-scheduler-combined.log',
      time: true,
      merge_logs: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000,
      exec_mode: 'fork',
    },
  ],

  // Deployment configuration (optional, for remote deployment)
  deploy: {
    production: {
      user: 'jarvis',
      host: 'your-server.com',
      ref: 'origin/main',
      repo: 'git@github.com:your-repo/lumina-overmind.git',
      path: '/var/www/lumina-overmind/jarvis',
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env production',
    },
    staging: {
      user: 'jarvis',
      host: 'staging-server.com',
      ref: 'origin/develop',
      repo: 'git@github.com:your-repo/lumina-overmind.git',
      path: '/var/www/lumina-overmind/jarvis-staging',
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env staging',
    },
  },
};
