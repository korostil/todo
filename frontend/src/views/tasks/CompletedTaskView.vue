<script setup>
import TaskItem from "@/components/TaskItem.vue";
import { ref, onMounted } from "vue";
import { readTaskList } from "@/store/api/tasks";

const tasks = ref(null);
const loading = ref(true);

function fetchTasks() {
  return readTaskList({ completed: true })
    .then((json) => {
      tasks.value = json.data;
    })
    .catch(() => {
      console.log("error");
    })
    .then(() => {
      loading.value = false;
    });
}

onMounted(() => {
  fetchTasks();
});
</script>

<template>
  <div v-if="!loading && tasks && tasks.length">
    <task-item v-for="task in tasks" :task="task" :key="task.id" />
  </div>
</template>

<style scoped></style>
