import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://www.google.com/search?q=google+flight&oq=google+flight&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRhA0gEIMTY0MmowajKoAgCwAgA&sourceid=chrome&ie=UTF-8');
  await page.getByRole('button', { name: 'Accept all' }).click();
  await page.getByRole('link', { name: 'Google Flights - Find Cheap' }).click();
  await page.getByLabel('Where from?').click();
  await page.getByRole('combobox', { name: 'Where else?' }).fill('zrh');
  await page.getByRole('combobox', { name: 'Where else?' }).press('Tab');
  await page.getByLabel('Origin, Select multiple').press('Tab');
  await page.getByPlaceholder('Where to?').fill('c');
  await page.getByRole('combobox', { name: 'Where else?' }).fill('cph');
  await page.getByRole('combobox', { name: 'Where else?' }).press('Tab');
  await page.getByLabel('Destination, Select multiple').press('Tab');
  await page.getByRole('button', { name: 'Monday, September 2,' }).click();
  await page.getByRole('textbox', { name: 'Departure' }).click();
  await page.getByRole('button', { name: 'Wednesday, September 11, 2024' }).click();
  await page.getByLabel('Done. Search for round trip').click();
  await page.getByLabel('Search', { exact: true }).click();
});