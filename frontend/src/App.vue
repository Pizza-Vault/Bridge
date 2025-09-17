<template>
  <div>
    <!-- Topbar -->
    <header class="topbar">
      <div class="container-app flex items-center justify-between py-3">
        <div class="flex items-center gap-3">
          <span class="brand-dot"></span>
          <div class="font-semibold tracking-wide">Bridge Console</div>
          <span class="badge badge-info">beta</span>
        </div>
        <div class="text-sm text-slate-400">
          <a class="hover:text-slate-200" href="#">Docs</a>
        </div>
      </div>
    </header>

    <!-- Content -->
    <main class="container-app py-6">
      <Dashboard />
    </main>
  </div>
</template>

<script setup>
import Dashboard from "./views/Dashboard.vue";
</script>
