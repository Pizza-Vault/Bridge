<template>
  <div class="space-y-6 max-w-4xl mx-auto p-6">
    <h1 class="text-2xl font-bold">Bridge Control</h1>

    <!-- Maschine -->
    <section class="card space-y-3">
      <h2 class="text-lg font-semibold">Maschine</h2>
      <div class="flex gap-3">
        <select v-model="mode" class="input w-48">
          <option value="active">active</option>
          <option value="maintenance">maintenance</option>
          <option value="offline">offline</option>
        </select>
        <button class="btn btn-primary" @click="onSetMode">Set mode</button>
      </div>
      <p v-if="modeMsg" class="text-sm text-gray-600">{{ modeMsg }}</p>
    </section>

    <!-- Bestellung -->
    <section class="card space-y-3">
      <h2 class="text-lg font-semibold">Bestellung</h2>
      <div class="grid md:grid-cols-3 gap-3">
        <input v-model="form.product_id" class="input" placeholder="product_id" />
        <input v-model="form.timeslot" class="input" placeholder="timeslot (ISO)" />
        <input v-model="form.pickup_code" class="input" placeholder="pickup_code" />
      </div>
      <div class="flex gap-2">
        <button class="btn btn-primary" @click="onCreate">Create</button>
        <button class="btn" :disabled="!orderId" @click="onStatus">Check</button>
        <button class="btn" :disabled="!orderId" @click="onComplete">Complete</button>
      </div>
      <div v-if="orderId" class="text-sm">order_id: {{ orderId }}</div>
      <pre v-if="status" class="bg-gray-50 p-3 rounded text-xs">{{ status }}</pre>
    </section>

    <!-- Inventar / Locker -->
    <section class="card space-y-3">
      <h2 class="text-lg font-semibold">Inventar & Locker</h2>
      <div class="flex gap-3 items-end">
        <button class="btn" @click="onInventory">Inventar abrufen</button>
        <input v-model.number="lockerId" type="number" class="input w-32" placeholder="locker_id" />
        <button class="btn" @click="onOpenLocker">Locker öffnen</button>
      </div>
      <ul v-if="inventory?.products?.length" class="list-disc pl-5 text-sm">
        <li v-for="p in inventory.products" :key="p.id">
          {{ p.name }} — Stock: {{ p.stock }}
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { setMode } from "../services/machine";
import { createOrder, getOrderStatus, completeOrder } from "../services/orders";
import { getInventory } from "../services/inventory";
import { openLocker } from "../services/locker";

const mode = ref("active");
const modeMsg = ref("");

const form = ref({ product_id: "", timeslot: "", pickup_code: "" });
const orderId = ref("");
const status = ref("");
const inventory = ref(null);
const lockerId = ref();

async function onSetMode() {
  const { data } = await setMode(mode.value);
  modeMsg.value = data?.message ?? JSON.stringify(data);
}

async function onCreate() {
  const { data } = await createOrder(form.value);
  orderId.value = data?.order_id || "";
  status.value = JSON.stringify(data, null, 2);
}

async function onStatus() {
  const { data } = await getOrderStatus(orderId.value);
  status.value = JSON.stringify(data, null, 2);
}

async function onComplete() {
  const { data } = await completeOrder(orderId.value);
  status.value = JSON.stringify(data, null, 2);
}

async function onInventory() {
  const { data } = await getInventory();
  inventory.value = data;
}

async function onOpenLocker() {
  await openLocker(lockerId.value);
}
</script>
