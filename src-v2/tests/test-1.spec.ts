import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://www.google.com/search?q=google+flight&oq=google+flight&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRhA0gEIMjAwNWowajKoAgCwAgA&sourceid=chrome&ie=UTF-8');
  await page.getByRole('button', { name: 'Accept all' }).click();
  await page.getByRole('cell', { name: 'Flights Use Google Flights to' }).getByRole('link').click();
  await page.getByPlaceholder('Where from?').click();
  await page.getByRole('combobox', { name: 'Where else?' }).fill('zrh');
  await page.getByPlaceholder('Where to?').click();
  await page.getByRole('combobox', { name: 'Where to?' }).fill('bue');
  await page.getByRole('combobox', { name: 'Where to?' }).press('Enter');
  await page.getByRole('textbox', { name: 'Departure' }).click();
  await page.getByRole('textbox', { name: 'Departure' }).fill('1/1/25');
  await page.getByRole('textbox', { name: 'Departure' }).press('Enter');
  await page.getByRole('textbox', { name: 'Return' }).click();
  await page.getByRole('textbox', { name: 'Return' }).fill('2');
  await page.getByRole('textbox', { name: 'Return' }).click();
  await page.getByRole('textbox', { name: 'Return' }).fill('2/2/25');
  await page.getByRole('textbox', { name: 'Return' }).press('Enter');
  await page.getByLabel('Done. Search for round-trip').click();
  await page.getByLabel('Search', { exact: true }).click();
});