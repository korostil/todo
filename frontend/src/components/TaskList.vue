<script setup>
import TaskItem from "@/components/TaskItem.vue";
import { ref, watchEffect } from "vue";
import { readTaskList } from "@/store/api/tasks";
import { toUnixDate } from "@/store/services/utils/dates";
import SnackbarWithTimeout from "@/components/SnackbarWithTimeout.vue";
import { INBOX_PROJECT_ID } from "@/store/services/constants";

const props = defineProps({
  completed: { type: Boolean, required: false, default: null },
  decisive: { type: Boolean, required: false, default: null },
  dueFrom: { type: Date, required: false, default: null },
  dueTo: { type: Date, required: false, default: null },
  projectId: { type: Number, required: false, default: null },
  search: { type: String, required: false, default: null },
  space: { type: Number, required: false, default: null },
  today: { type: Boolean, required: false, default: false },
});
const completed = ref(props.completed),
  decisive = ref(props.decisive),
  due_from = ref(props.dueFrom),
  due_to = ref(props.dueTo),
  project_id = ref(props.projectId),
  search = ref(props.search),
  space = ref(props.space),
  today = ref(props.today),
  tasks = ref(null),
  loading_error = ref(null),
  taskCompleted = ref(false);

function fetchTasks() {
  let filter;
  if (project_id.value === INBOX_PROJECT_ID) {
    filter = {
      completed: completed.value,
      decisive: decisive.value,
      due_from: due_from.value,
      due_to: due_to.value,
      inbox: true,
      search: search.value,
      space: space.value,
    };
  } else if (today.value === true) {
    filter = {
      completed: false,
      space: space.value,
      due_to: toUnixDate(new Date()),
    };
  } else {
    filter = {
      completed: completed.value,
      decisive: decisive.value,
      due_from: due_from.value,
      due_to: due_to.value,
      project_id: project_id.value,
      search: search.value,
      space: space.value,
    };
  }

  const { data, error } = readTaskList(filter);

  watchEffect(() => {
    tasks.value = data.value;
  });
  watchEffect(() => {
    loading_error.value = error.value;
  });
}

watchEffect(() => {
  completed.value = props.completed;
  decisive.value = props.decisive;
  due_from.value = props.dueFrom;
  due_to.value = props.dueTo;
  project_id.value = props.projectId;
  search.value = props.search;
  space.value = props.space;
  today.value = props.today;
  fetchTasks();
});

function doComplete(task_id) {
  taskCompleted.value = true;
  function removeValue(value, index, arr) {
    if (value.id === task_id) {
      arr.splice(index, 1);
      return true;
    }
    return false;
  }

  if (today.value === true || completed.value === false) {
    // TODO optimization: there is a way to make it neat and tidy?
    tasks.value.filter(removeValue);
  } else {
    const findTaskIndex = (element) => element.id === task_id;
    tasks.value[tasks.value.findIndex(findTaskIndex)].completed = true;
  }
}
</script>

<template>
  <snackbar-with-timeout
    text="Task is completed"
    v-if="taskCompleted"
  ></snackbar-with-timeout>
  <snackbar-with-timeout
    text="Failed to load task list. Please reload the page."
    v-if="loading_error"
  ></snackbar-with-timeout>
  <v-list v-else>
    <v-list-item
      v-for="task in tasks"
      :key="task.id"
      active-color="primary"
      rounded="lg"
      @click="true"
    >
      <task-item :task="task" @task-completed="doComplete"></task-item>
    </v-list-item>
  </v-list>
</template>

<style scoped></style>
