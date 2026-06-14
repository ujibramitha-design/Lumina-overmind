import { test, expect } from '@playwright/test';

test.describe('Dashboard E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('should load dashboard homepage', async ({ page }) => {
    await expect(page).toHaveTitle(/LUMINA OS Enterprise/);
    await expect(page.locator('body')).toBeVisible();
  });

  test('should navigate to leads page', async ({ page }) => {
    await page.click('text=Leads');
    await expect(page).toHaveURL(/.*leads/);
    await expect(page.locator('text=Lead management')).toBeVisible();
  });

  test('should navigate to projects page', async ({ page }) => {
    await page.click('text=Projects');
    await expect(page).toHaveURL(/.*projects/);
    await expect(page.locator('text=Project directory')).toBeVisible();
  });

  test('should navigate to dashboard page', async ({ page }) => {
    await page.click('text=Dashboard');
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test('should display sidebar navigation', async ({ page }) => {
    const sidebar = page.locator('aside');
    await expect(sidebar).toBeVisible();
  });

  test('should display top header', async ({ page }) => {
    const header = page.locator('header');
    await expect(header).toBeVisible();
  });
});
