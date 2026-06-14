/**
 * JARVIS Mobile - Authentication Service
 * =====================================
 * 
 * Service Token authentication for secure communication
 * with JARVIS backend API
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const STORAGE_KEY = '@jarvis_auth_token';
const API_BASE_URL = process.env.API_BASE_URL || 'https://jarvis.yourdomain.com'; // Cloudflare domain

class AuthService {
  constructor() {
    this.token = null;
    this.isAuthenticated = false;
  }

  /**
   * Initialize auth service by loading token from storage
   */
  async initialize() {
    try {
      const storedToken = await AsyncStorage.getItem(STORAGE_KEY);
      if (storedToken) {
        this.token = storedToken;
        this.isAuthenticated = true;
        console.log('Auth token loaded from storage');
      }
    } catch (error) {
      console.error('Error loading auth token:', error);
    }
  }

  /**
   * Set service token (typically from app configuration)
   */
  async setToken(token) {
    try {
      this.token = token;
      this.isAuthenticated = true;
      await AsyncStorage.setItem(STORAGE_KEY, token);
      console.log('Auth token saved');
    } catch (error) {
      console.error('Error saving auth token:', error);
      throw error;
    }
  }

  /**
   * Get current auth token
   */
  getToken() {
    return this.token;
  }

  /**
   * Check if authenticated
   */
  checkAuth() {
    return this.isAuthenticated;
  }

  /**
   * Clear auth token (logout)
   */
  async logout() {
    try {
      this.token = null;
      this.isAuthenticated = false;
      await AsyncStorage.removeItem(STORAGE_KEY);
      console.log('Auth token cleared');
    } catch (error) {
      console.error('Error clearing auth token:', error);
      throw error;
    }
  }

  /**
   * Make authenticated API request
   */
  async request(endpoint, options = {}) {
    if (!this.isAuthenticated || !this.token) {
      throw new Error('Not authenticated');
    }

    const config = {
      url: `${API_BASE_URL}${endpoint}`,
      headers: {
        'Content-Type': 'application/json',
        'X-Jarvis-Service-Token': this.token,
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await axios(config);
      return response.data;
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  /**
   * GET request
   */
  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  /**
   * POST request
   */
  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      data,
    });
  }

  /**
   * PUT request
   */
  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      data,
    });
  }

  /**
   * DELETE request
   */
  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }

  /**
   * Health check to verify connection
   */
  async healthCheck() {
    try {
      const response = await this.get('/api/jarvis-mobile/health');
      return response;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  /**
   * Get system metrics
   */
  async getMetrics() {
    return this.get('/api/jarvis-mobile/metrics');
  }

  /**
   * Get connection status
   */
  async getConnectionStatus() {
    return this.get('/api/jarvis-mobile/connections');
  }

  /**
   * Get JARVIS thought process
   */
  async getThoughtProcess() {
    return this.get('/api/jarvis-mobile/thought-process');
  }

  /**
   * Search codebase
   */
  async searchCode(query, filters = []) {
    return this.post('/api/jarvis-mobile/code/search', {
      query,
      filters,
    });
  }

  /**
   * Get code explanation
   */
  async explainCode(filePath) {
    return this.get(`/api/jarvis-mobile/code/explain/${encodeURIComponent(filePath)}`);
  }
}

// Export singleton instance
const authService = new AuthService();

export default authService;
