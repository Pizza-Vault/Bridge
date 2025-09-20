// src/services/orders.js – API-Calls zu Bridge (mit HMAC-Auth)
const BASE_URL = 'http://127.0.0.1:8000';
const TOKEN = 'my-super-token';
const SECRET = 'my-super-secret';

async function generateHMAC(method, path, body) {
  const crypto = await import('crypto');
  const bodyStr = body ? JSON.stringify(body) : '';
  const bodyHash = crypto.createHash('sha256').update(bodyStr).digest('hex');
  const timestamp = Math.floor(Date.now() / 1000);
  const nonce = crypto.randomUUID().replace(/-/g, '');
  const baseString = `${method}\n${path}\n${bodyHash}\n${timestamp}\n${nonce}`;
  const signature = crypto.createHmac('sha256', SECRET).update(baseString).digest('hex');
  return { timestamp, nonce, signature };
}

export async function createOrder(form) {
  const path = '/api/order/create';
  const { timestamp, nonce, signature } = await generateHMAC('POST', path, form);
  const response = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'X-Timestamp': timestamp,
      'X-Nonce': nonce,
      'X-Signature': signature,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(form),
  });
  if (!response.ok) throw new Error('Create failed');
  return response.json();
}

export async function getOrderStatus(orderId) {
  const path = `/api/order/status?order_id=${orderId}`;
  const { timestamp, nonce, signature } = await generateHMAC('GET', path);
  const response = await fetch(`${BASE_URL}${path}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'X-Timestamp': timestamp,
      'X-Nonce': nonce,
      'X-Signature': signature,
    },
  });
  if (!response.ok) throw new Error('Status failed');
  return response.json();
}

export async function completeOrder(orderId) {
  const path = '/api/locker/pickup/confirm';
  const body = { pickup_code: orderId };  // Annahme: orderId als pickup_code
  const { timestamp, nonce, signature } = await generateHMAC('POST', path, body);
  const response = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'X-Timestamp': timestamp,
      'X-Nonce': nonce,
      'X-Signature': signature,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error('Complete failed');
  return response.json();
}