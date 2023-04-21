<script setup>
import { ref } from "vue";
import TaskItem from "@/components/TaskItem.vue";

const completed_today = ref(null);
const incomplete_today = ref(null);
const created_today = ref(null);
const loading = ref(true);
</script>

<template>
  <div>
    <div>
      <strong>Checklist</strong>
      <div><mark>#TODO: checklist to do during review</mark></div>
    </div>
    <div v-if="!loading && completed_today && completed_today.length">
      <strong>Completed today</strong>
      <task-item v-for="task in completed_today" :task="task" :key="task.id" />
    </div>
    <div v-if="!loading && incomplete_today && incomplete_today.length">
      <strong>Incomplete today</strong>
      <task-item v-for="task in incomplete_today" :task="task" :key="task.id" />
    </div>
    <div>
      <textarea
        placeholder="Some thoughts or major point of the day"
      ></textarea>
    </div>
    <div v-if="!loading && created_today && created_today.length">
      <strong>Created today</strong>
      <task-item v-for="task in created_today" :task="task" :key="task.id" />
    </div>
    <button>Save</button>
  </div>
</template>

<style scoped></style>
