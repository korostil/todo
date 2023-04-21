<script setup>
import { onMounted, ref, watchEffect } from "vue";
import { readGoalList } from "@/store/api/goals";

const goals = ref([]),
  loading_error = ref(null);

onMounted(() => {
  const today = new Date();
  const { data, error } = readGoalList({
    month: today.getMonth() + 1,
    year: today.getFullYear(),
  });

  watchEffect(() => {
    goals.value = data.value;
  });
  watchEffect(() => {
    loading_error.value = error.value;
  });
});
</script>

<template>
  <v-list>
    <v-list-subheader>MONTH FOCUS</v-list-subheader>
    <v-list-item
      v-for="item in goals"
      :key="item.id"
      :title="item.title"
      :subtitle="item.description"
      :prepend-icon="item.is_completed ? 'mdi-check' : 'mdi-circle-outline'"
      active-color="primary"
      rounded="lg"
      @click="true"
    >
    </v-list-item>
  </v-list>
</template>

<style scoped></style>
