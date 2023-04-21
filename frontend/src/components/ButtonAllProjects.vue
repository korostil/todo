<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<template>
  <v-btn
    variant="plain"
    prepend-icon="mdi-format-list-bulleted"
    @click="router.push({ name: 'project_list' })"
  >
    all projects
  </v-btn>
</template>

<style scoped></style>
