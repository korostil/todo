<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<template>
  <v-btn
    variant="plain"
    prepend-icon="mdi-format-list-bulleted"
    @click="router.push({ name: 'task_list' })"
  >
    all tasks
  </v-btn>
</template>

<style scoped></style>
