// src/services/orders.js – Service-Funktionen für Orders
export async function createOrder(form) {
  // Platzhalter – ersetze mit Bridge-API-Call
  console.log('Create order:', form);
  return { data: { order_id: 'ord_123', pickup_code: 'pc_456', status: 'pending' } };
}

export async function getOrderStatus(orderId) {
  // Platzhalter
  console.log('Get status for:', orderId);
  return { data: { order_id, status: 'completed', payment: 'paid' } };
}

export async function completeOrder(orderId) {
  // Platzhalter
  console.log('Complete order:', orderId);
  return { data: { order_id, status: 'completed' } };
}