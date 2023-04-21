<script setup>
import { onMounted, ref, watchEffect } from "vue";
import { readTaskList } from "@/store/api/tasks";
import SnackbarWithTimeout from "@/components/SnackbarWithTimeout.vue";
import { getMonday, getSunday, toUnixDate } from "@/store/services/utils/dates";
import DialogUpdateTask from "@/components/DialogUpdateTask.vue";

const tasks = ref([]),
  loading_error = ref(null);

onMounted(() => {
  const { data, error } = readTaskList({
    decisive: true,
    due_from: toUnixDate(getMonday(new Date())),
    due_to: toUnixDate(getSunday(new Date())),
  });

  watchEffect(() => {
    tasks.value = data.value;
  });
  watchEffect(() => {
    loading_error.value = error.value;
  });
});
</script>

<template>
  <snackbar-with-timeout
    text="Failed to load week focus list. Please reload the page."
    v-if="loading_error"
  ></snackbar-with-timeout>
  <v-list>
    <v-list-subheader>WEEK FOCUS</v-list-subheader>
    <v-list-item
      v-for="task in tasks"
      :key="task.id"
      :title="task.title"
      :subtitle="task.description"
      :prepend-icon="task.is_completed ? 'mdi-check' : 'mdi-progress-helper'"
      active-color="primary"
      rounded="lg"
      @click="true"
    >
      <dialog-update-task :task="task"></dialog-update-task>
    </v-list-item>
  </v-list>
</template>

<style scoped></style>
