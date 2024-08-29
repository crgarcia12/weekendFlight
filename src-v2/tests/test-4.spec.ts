import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://www.google.com/search?q=google+flights&oq=google+flights&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRhA0gEIMzE1NGowajKoAgCwAgA&sourceid=chrome&ie=UTF-8');
  await page.getByRole('button', { name: 'Accept all' }).click();
  await page.getByRole('link', { name: 'Google Flights - Find Cheap' }).click();
  await page.getByLabel('Where from?').click();
  await page.getByText('Zurich Airport').click();
  await page.getByPlaceholder('Where to?').click();
  await page.getByRole('combobox', { name: 'Where to?' }).click();
  await page.getByLabel('Enter your destination').getByText('Anywhere', { exact: true }).click();
  await page.getByRole('textbox', { name: 'Return' }).click();
  await page.getByRole('textbox', { name: 'Return' }).press('Control+a');
  await page.getByRole('textbox', { name: 'Return' }).fill('1/1/2025');
  await page.getByRole('textbox', { name: 'Return' }).press('Enter');
  await page.getByLabel('Done. Search for round trip').click();
  await page.getByLabel('Explore destinations').click();
});