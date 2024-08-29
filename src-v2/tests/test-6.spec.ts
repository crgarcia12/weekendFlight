import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://www.google.com/search?q=google+flights&oq=google+flights&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRhA0gEIMTQ2MWowajKoAgCwAgA&sourceid=chrome&ie=UTF-8');
  await page.getByRole('button', { name: 'Accept all' }).click();
  await page.getByRole('link', { name: 'Google Flights - Find Cheap' }).click();
  await page.getByLabel('Where from?').click();
  await page.getByLabel('Economy').locator('div').click();
  await page.getByRole('option', { name: 'Business' }).click();
});