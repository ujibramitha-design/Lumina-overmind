/**
 * JARVIS Mobile - Android Build Script
 * ====================================
 * 
 * Build script for compiling APK using Expo EAS Build
 * Run with: node build-android.js
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🤖 JARVIS Mobile - Android Build Script');
console.log('======================================\n');

// Configuration
const CONFIG = {
  profile: 'preview', // 'preview' for testing, 'production' for release
  platform: 'android',
};

// Check if EAS CLI is installed
function checkEASCLI() {
  try {
    execSync('eas --version', { stdio: 'pipe' });
    console.log('✅ EAS CLI is installed\n');
    return true;
  } catch (error) {
    console.log('❌ EAS CLI is not installed');
    console.log('Installing EAS CLI...\n');
    try {
      execSync('npm install -g eas-cli', { stdio: 'inherit' });
      console.log('✅ EAS CLI installed\n');
      return true;
    } catch (installError) {
      console.error('❌ Failed to install EAS CLI');
      console.error('Please run: npm install -g eas-cli');
      process.exit(1);
    }
  }
}

// Check if node_modules exists
function checkDependencies() {
  const nodeModulesPath = path.join(__dirname, 'node_modules');
  if (!fs.existsSync(nodeModulesPath)) {
    console.log('⚠️  node_modules not found');
    console.log('Installing dependencies...\n');
    try {
      execSync('npm install', { stdio: 'inherit', cwd: __dirname });
      console.log('✅ Dependencies installed\n');
    } catch (error) {
      console.error('❌ Failed to install dependencies');
      process.exit(1);
    }
  } else {
    console.log('✅ Dependencies are installed\n');
  }
}

// Check if .env exists
function checkEnv() {
  const envPath = path.join(__dirname, '.env');
  if (!fs.existsSync(envPath)) {
    console.log('⚠️  .env file not found');
    console.log('Creating .env from .env.example...\n');
    
    const envExamplePath = path.join(__dirname, '.env.example');
    if (fs.existsSync(envExamplePath)) {
      fs.copyFileSync(envExamplePath, envPath);
      console.log('✅ .env file created');
      console.log('⚠️  Please update .env with your configuration before building\n');
    } else {
      console.log('⚠️  .env.example not found, creating basic .env\n');
      fs.writeFileSync(envPath, `
# JARVIS Mobile Configuration
API_BASE_URL=http://localhost:8000
JARVIS_SERVICE_TOKEN=your_service_token_here
`);
    }
  } else {
    console.log('✅ .env file exists\n');
  }
}

// Run EAS build
function runBuild() {
  console.log(`🚀 Starting EAS build for ${CONFIG.platform} (${CONFIG.profile})...\n`);
  
  try {
    const command = `eas build --platform ${CONFIG.platform} --profile ${CONFIG.profile}`;
    console.log(`Running: ${command}\n`);
    
    execSync(command, {
      stdio: 'inherit',
      cwd: __dirname,
    });
    
    console.log('\n✅ Build completed successfully!');
    console.log('📱 Check your Expo dashboard for the APK download link\n');
  } catch (error) {
    console.error('\n❌ Build failed');
    console.error('Please check the error messages above\n');
    process.exit(1);
  }
}

// Main build process
async function main() {
  try {
    // Step 1: Check EAS CLI
    checkEASCLI();
    
    // Step 2: Check dependencies
    checkDependencies();
    
    // Step 3: Check .env
    checkEnv();
    
    // Step 4: Run build
    runBuild();
    
  } catch (error) {
    console.error('❌ Build process failed:', error.message);
    process.exit(1);
  }
}

// Run the build
main();
