// src/services/orders.js – API-Funktionen für Orders (Platzhalter – integriere Bridge-API)
export async function createOrder(form) {
  try {
    // Beispiel-Call zu Bridge-API: POST /api/order/create
    const response = await fetch('/api/order/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Füge Auth-Headers hinzu (Bearer, HMAC etc. aus Übergabe)
      },
      body: JSON.stringify(form),
    });
    if (!response.ok) throw new Error('Create failed');
    return response.json();
  } catch (e) {
    throw new Error('Create order error: ' + e.message);
  }
}

export async function getOrderStatus(orderId) {
  try {
    // Beispiel-Call: GET /api/order/status?order_id=ord_xxx
    const response = await fetch(`/api/order/status?order_id=${orderId}`, {
      headers: {
        // Auth-Headers
      },
    });
    if (!response.ok) throw new Error('Status failed');
    return response.json();
  } catch (e) {
    throw new Error('Get status error: ' + e.message);
  }
}

export async function completeOrder(orderId) {
  try {
    // Beispiel-Call: POST /api/locker/pickup/confirm oder ähnlich
    const response = await fetch('/api/order/complete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Auth-Headers
      },
      body: JSON.stringify({ order_id: orderId }),
    });
    if (!response.ok) throw new Error('Complete failed');
    return response.json();
  } catch (e) {
    throw new Error('Complete order error: ' + e.message);
  }
}