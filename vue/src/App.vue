<script setup>
import AppLayout from '@/layouts/AppLayout.vue'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
</script>

<template>
  <ErrorBoundary>
    <AppLayout />
  </ErrorBoundary>
</template>