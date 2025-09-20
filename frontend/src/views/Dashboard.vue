<template>
  <div class="space-y-6">
    <!-- Stat Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-slate-400 text-xs uppercase">System</div>
            <div class="text-xl font-semibold flex items-center gap-2">
              {{ modeLabel }}
              <span :class="['badge', modeBadgeClass]">{{ mode }}</span>
            </div>
          </div>
          <IconBolt />
        </div>
      </div>
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-slate-400 text-xs uppercase">Orders</div>
            <div class="text-xl font-semibold">{{ orderId ? 1 : 0 }}</div>
          </div>
          <IconPackage />
        </div>
      </div>
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-slate-400 text-xs uppercase">Inventory</div>
            <div class="text-xl font-semibold">{{ invCount }}</div>
          </div>
          <IconBoxes />
        </div>
      </div>
    </div>

    <!-- Grid: Maschine + Bestellung -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Maschine -->
      <section class="card space-y-4">
        <div>
          <h2 class="section-title">Maschine</h2>
          <p class="section-sub">Modus setzen und Statusmeldung sehen.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="label">Modus</label>
            <select v-model="mode" class="input">
              <option value="active">active</option>
              <option value="maintenance">maintenance</option>
              <option value="offline">offline</option>
            </select>
            <p class="help mt-1">Wähle den Betriebszustand der Maschine.</p>
          </div>
          <div class="flex items-end">
            <button class="btn btn-primary w-full" @click="onSetMode" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              <span v-else>Set mode</span>
            </button>
          </div>
        </div>

        <p v-if="modeMsg" class="text-sm text-slate-300/90">{{ modeMsg }}</p>
      </section>

      <!-- Bestellung -->
      <section class="card space-y-4">
        <div>
          <h2 class="section-title">Bestellung</h2>
          <p class="section-sub">Neuen Auftrag anlegen, prüfen und abschließen.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div>
            <label class="label">Product ID</label>
            <input v-model="form.product_id" class="input" placeholder="z. B. 123" />
          </div>
          <div>
            <label class="label">Timeslot</label>
            <input v-model="form.timeslot" type="datetime-local" class="input" />
            <p class="help mt-1">ISO-Zeit; lokale Zeitzone.</p>
          </div>
          <div>
            <label class="label">Pickup Code</label>
            <input v-model="form.pickup_code" class="input" placeholder="ABCD1234" />
          </div>
        </div>

        <div class="flex flex-wrap gap-2">
          <button class="btn btn-primary" @click="onCreate" :disabled="loading">Create</button>
          <button class="btn btn-ghost" :disabled="!orderId || loading" @click="onStatus">Check</button>
          <button class="btn btn-ok" :disabled="!orderId || loading" @click="onComplete">Complete</button>
          <button class="btn btn-outline" v-if="orderId" @click="clearOrder">Reset</button>
        </div>

        <div v-if="orderId" class="text-sm text-slate-300/90">
          <span class="badge badge-info">order_id: {{ orderId }}</span>
        </div>

        <pre v-if="status"
             class="bg-white/5 border border-white/10 rounded-lg p-3 text-xs whitespace-pre-wrap text-slate-200/90">
{{ status }}
        </pre>
      </section>
    </div>

    <!-- Inventar / Locker -->
    <section class="card space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="section-title">Inventar & Locker</h2>
          <p class="section-sub">Bestände ansehen und Locker öffnen.</p>
        </div>
        <div class="flex items-center gap-2">
          <button class="btn btn-ghost" @click="onInventory" :disabled="loading">
            Inventar abrufen
          </button>
          <div class="flex items-end gap-2">
            <div>
              <label class="label">Locker ID</label>
              <input v-model.number="lockerId" type="number" class="input w-36" placeholder="z. B. 5" />
            </div>
            <button class="btn btn-outline" @click="onOpenLocker" :disabled="loading">Öffnen</button>
          </div>
        </div>
      </div>

      <div v-if="inventory?.products?.length">
        <table class="table">
          <thead>
            <tr>
              <th>Name</th>
              <th class="w-24">ID</th>
              <th class="w-24 text-right">Stock</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in inventory.products" :key="p.id">
              <td class="py-2">{{ p.name }}</td>
              <td class="py-2 text-slate-400">{{ p.id }}</td>
              <td class="py-2 text-right">
                <span :class="['badge', p.stock > 5 ? 'badge-ok' : 'badge-warn']">{{ p.stock }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="text-sm text-slate-400">Kein Inventar geladen.</div>
    </section>

    <!-- Feedback -->
    <div v-if="loading" class="flex items-center gap-2 text-slate-300">
      <span class="spinner"></span> Verarbeite …
    </div>
    <div v-if="error" class="text-red-400">❌ {{ error }}</div>

    <!-- Toast -->
    <Toast v-if="toast.show" :type="toast.type" :message="toast.message" @close="toast.show=false" />
  </div>
</template>

<script setup lang="jsx">
import { ref, computed } from "vue";
import { setMode } from "../services/machine";
import { createOrder, getOrderStatus, completeOrder } from "../services/orders";
import { getInventory } from "../services/inventory";
import { openLocker } from "../services/locker";
import Toast from "../ui/Toast.vue";

/* Icons (inline, leichtgewichtig) */
const IconBolt = () => ({
  render(){ return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" class="text-amber-400">
      <path d="M13 2L3 14h7l-1 8 11-14h-7l0-6z" stroke="currentColor" stroke-width="1.5" fill="currentColor" />
    </svg>
  )}
})
const IconPackage = () => ({
  render(){ return (
    <svg width="28" height="28" viewBox="0 0 24 24" class="text-indigo-300" fill="none">
      <path d="M3 7l9-4 9 4-9 4-9-4zM3 7v10l9 4 9-4V7" stroke="currentColor" stroke-width="1.5" fill="none"/>
    </svg>
  )}
})
const IconBoxes = () => ({
  render(){ return (
    <svg width="28" height="28" viewBox="0 0 24 24" class="text-emerald-300" fill="none">
      <path d="M3 9l9-5 9 5-9 5-9-5zM3 15l9 5 9-5" stroke="currentColor" stroke-width="1.5"/>
    </svg>
  )}
})

/* State */
const mode = ref("active");
const modeMsg = ref("");
const form = ref({ product_id: "", timeslot: "", pickup_code: "" });
const orderId = ref("");
const status = ref("");
const inventory = ref(null);
const lockerId = ref();
const loading = ref(false);
const error = ref("");
const toast = ref({ show:false, message:"", type:"success" });

const invCount = computed(()=> inventory.value?.products?.length ?? 0);
const modeLabel = computed(()=> mode.value === "active" ? "Online" :
                               mode.value === "maintenance" ? "Wartung" : "Offline");
const modeBadgeClass = computed(()=> mode.value === "active" ? "badge-ok" :
                                   mode.value === "maintenance" ? "badge-info" : "badge-warn");

/* Utils */
async function wrap(fn, okMsg){
  loading.value = true; error.value = "";
  try{
    await fn();
    if(okMsg) showToast(okMsg, "success");
  }catch(e){
    error.value = e?.response?.data?.message || e?.message || "Unknown error";
    showToast(error.value, "error");
  }finally{ loading.value = false; }
}
function showToast(message, type="success"){
  toast.value = { show:true, message, type };
  setTimeout(()=> toast.value.show=false, 2500);
}

/* Actions */
async function onSetMode(){
  await wrap(async ()=>{
    const { data } = await setMode(mode.value);
    modeMsg.value = data?.message ?? JSON.stringify(data);
  }, "Mode aktualisiert");
}
async function onCreate(){
  await wrap(async ()=>{
    const { data } = await createOrder(form.value);
    orderId.value = data?.order_id || "";
    status.value = JSON.stringify(data, null, 2);
  }, "Bestellung erstellt");
}
async function onStatus(){
  await wrap(async ()=>{
    const { data } = await getOrderStatus(orderId.value);
    status.value = JSON.stringify(data, null, 2);
  }, "Status aktualisiert");
}
async function onComplete(){
  await wrap(async ()=>{
    const { data } = await completeOrder(orderId.value);
    status.value = JSON.stringify(data, null, 2);
  }, "Bestellung abgeschlossen");
}
async function onInventory(){
  await wrap(async ()=>{
    const { data } = await getInventory();
    inventory.value = data;
  }, "Inventar geladen");
}
async function onOpenLocker(){
  await wrap(async ()=>{
    await openLocker(lockerId.value);
  }, `Locker ${lockerId.value ?? ''} geöffnet`);
}
function clearOrder(){
  form.value = { product_id:"", timeslot:"", pickup_code:"" };
  orderId.value = ""; status.value = "";
}
</script>