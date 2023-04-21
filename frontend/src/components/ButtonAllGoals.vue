<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<template>
  <v-btn
    variant="plain"
    prepend-icon="mdi-format-list-bulleted"
    @click="router.push({ name: 'goal_list' })"
  >
    all goals
  </v-btn>
</template>

<style scoped></style>
