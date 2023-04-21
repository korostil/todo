<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { completeTask, deleteTask, readTask } from "@/store/api/tasks";
import { readProject } from "@/store/api/projects";

const route = useRoute();
const router = useRouter();

const task_id = route.params.task_id;

const task = ref(null);
const project = ref(null);
const loading = ref(true);
const loading_project = ref(true);

function fetchTask() {
  return readTask(task_id)
    .then((json) => {
      task.value = json.data;
      if (json.data.project_id !== null) {
        fetchProject(json.data.project_id);
      } else {
        loading_project.value = false;
        project.value = { title: "With no project" };
      }
    })
    .catch(() => {
      console.log("error");
    })
    .then(() => {
      loading.value = false;
    });
}

function doDelete() {
  deleteTask(task_id)
    .then(() => {
      router.push({ name: "main" });
    })
    .catch(() => {
      console.log("error");
    });
}

function doComplete() {
  completeTask(task_id)
    .then(() => {
      router.push({ name: "main" });
    })
    .catch(() => {
      console.log("error");
    });
}

function fetchProject(id) {
  return readProject(id)
    .then((json) => {
      project.value = json.data;
    })
    .catch(() => {
      console.log("error");
    })
    .then(() => {
      loading_project.value = false;
    });
}

onMounted(() => {
  fetchTask();
});
</script>

<template>
  <div>
    <div>
      <button class="btn purple" @click="router.push({ name: 'main' })">
        Back to mainpage
      </button>
    </div>
    <div v-if="!loading && task">
      <h1>{{ task.title }}</h1>
      <div>
        <strong>{{ task.description }}</strong>
      </div>
      <div>
        <strong>Decisive: {{ task.decisive }}</strong>
      </div>
      <div>
        <strong>Space: {{ task.space }}</strong>
      </div>
      <div>
        <strong>Due date: {{ task.due_date }}</strong>
      </div>
      <div>
        <strong>Due time: {{ task.due_time }}</strong>
      </div>
      <div v-if="!loading_project && project">
        <strong>Project: {{ project.title }}</strong>
      </div>

      <div v-else>
        <button class="btn green" @click="doComplete">Complete</button>
      </div>
      <div>
        <button
          class="btn orange"
          @click="
            router.push({
              name: 'update_task',
              params: { task_id: task.id },
            })
          "
        >
          Update
        </button>
      </div>
      <div>
        <button class="btn red" @click="doDelete">Delete</button>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
