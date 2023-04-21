<script setup>
import { ref } from "vue";
import TaskItem from "@/components/TaskItem.vue";

const completed_this_week = ref(null);
const incomplete_this_week = ref(null);
const loading = ref(true);
</script>

<template>
  <div>
    <div>
      <strong>Checklist</strong>
      <div><mark>#TODO: check list to do during review</mark></div>
    </div>
    <div v-if="!loading && completed_this_week && completed_this_week.length">
      <strong>Completed this week</strong>
      <task-item
        v-for="task in completed_this_week"
        :task="task"
        :key="task.id"
      />
    </div>
    <div v-if="!loading && incomplete_this_week && incomplete_this_week.length">
      <strong>Incomplete this week</strong>
      <task-item
        v-for="task in incomplete_this_week"
        :task="task"
        :key="task.id"
      />
    </div>
    <div><mark>#TODO: list of daily reviews</mark></div>
    <div>
      <textarea
        placeholder="Some thoughts or major point of the week"
      ></textarea>
    </div>
    <button>Save</button>
  </div>
</template>

<style scoped></style>
