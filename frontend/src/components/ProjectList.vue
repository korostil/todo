<script setup>
import { computed, ref, watchEffect } from "vue";
import { readProjectList, projects } from "@/store/api/projects";
import ButtonUpdateProject from "@/components/ButtonUpdateProject.vue";
import ButtonRemoveProject from "@/components/ButtonRemoveProject.vue";
import ButtonArchiveProject from "@/components/ButtonArchiveProject.vue";
import ButtonRestoreProject from "@/components/ButtonRestoreProject.vue";
import SnackbarWithTimeout from "@/components/SnackbarWithTimeout.vue";
import { INBOX_PROJECT_ID } from "@/store/services/constants";

const props = defineProps({
  archived: { type: Boolean, required: false, default: null },
  search: { type: String, required: false, default: null },
  space: { type: Number, required: false, default: null },
  showDescription: { type: Boolean, required: false, default: false },
});
const emit = defineEmits(["projectSelected"]);

const archived = ref(props.archived),
  search = ref(props.search),
  space = ref(props.space),
  loading_error = ref(null);

const filteredProjects = computed(() => {
  if (!projects.value) return [];

  return projects.value.filter((project) => {
    const is_archived =
        archived.value === null || project.is_archived === archived.value,
      is_searched =
        search.value === null ||
        project.title.includes(search.value) ||
        project.description.includes(search.value),
      is_in_space = space.value === null || project.space === space.value;

    return is_archived && is_searched && is_in_space;
  });
});

watchEffect(() => {
  archived.value = props.archived;
  search.value = props.search;
  space.value = props.space;
  readProjectList({});
});
</script>

<template>
  <snackbar-with-timeout
    text="Failed to load project list. Please reload the page."
    v-if="loading_error"
  ></snackbar-with-timeout>
  <v-list v-else>
    <v-list-item
      title="Inbox"
      :value="INBOX_PROJECT_ID"
      active-color="secondary"
      rounded="lg"
      prepend-icon="mdi-inbox"
      @click="emit('projectSelected', INBOX_PROJECT_ID)"
    ></v-list-item>
    <v-list-subheader>PROJECTS</v-list-subheader>
    <v-list-item
      v-for="project in filteredProjects"
      :key="project.id"
      :title="project.title"
      :subtitle="showDescription ? project.description : ''"
      :value="project.id"
      @click="emit('projectSelected', project.id)"
      active-color="secondary"
      rounded="lg"
    >
      <template v-slot:prepend>
        <v-icon
          :icon="project.is_archived ? 'mdi-archive-outline' : 'mdi-circle'"
          :color="project.color"
        ></v-icon>
      </template>

      <template v-slot:append>
        <!-- TODO make menu disappear after successful project update -->
        <v-menu close-on-content-click>
          <template v-slot:activator="{ props }">
            <v-btn
              color="grey-darken-1"
              icon="mdi-menu"
              variant="text"
              v-bind="props"
            ></v-btn>
          </template>
          <v-list>
            <v-list-item>
              <button-update-project :project="project"></button-update-project>
            </v-list-item>

            <v-list-item>
              <button-restore-project
                v-if="project.is_archived"
                :project="project"
              ></button-restore-project>
              <button-archive-project
                v-else
                :project="project"
              ></button-archive-project>
            </v-list-item>

            <v-list-item>
              <button-remove-project :project="project"></button-remove-project>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-list-item>
  </v-list>
</template>

<style scoped></style>
