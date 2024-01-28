import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://consent.google.com/m?continue=https://www.google.com/travel/flights&gl=CH&m=0&pc=trv&cm=2&hl=en-US&src=1');
  await page.getByRole('button', { name: 'Accept all' }).click();
  await page.getByLabel('Economy').click();
  await page.getByRole('option', { name: 'Premium economy' }).click();
  await page.getByLabel('Premium economy').click();
  await page.getByRole('option', { name: 'Business' }).click();
  await page.getByLabel('1 passenger').click();
  await page.getByPlaceholder('Where to?').click();
  await page.getByLabel('1 passenger').click();
  await page.getByLabel('Add adult').click();
  await page.getByLabel('Flight', { exact: true }).getByLabel('Explore destinations').click();
});