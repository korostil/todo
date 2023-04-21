import { todoAPIHeaders, todoAPIUrl, useFetch } from "@/store/api/base";
import { computed, ref, watchEffect } from "vue";
import { findEntityIndexById } from "@/store/services/utils/entities";

const entity_url = new URL(todoAPIUrl + "/api/private/v1/projects/");

export const projects = ref([]);
export const isProjectsLoadingError = ref(false);
export const activeProjects = computed(() =>
  projects.value.filter((project) => !project.is_archived)
);

export function createProject(body) {
  return fetch(entity_url, {
    method: "post",
    body: JSON.stringify(body),
    headers: todoAPIHeaders,
  })
    .then((response) => {
      if (response.status !== 201) {
        const error = new Error(response.statusText);
        error.json = response.json();
        throw error;
      }
      return response.json();
    })
    .then((json) => {
      projects.value.push(json.data);
      return json;
    });
}

export function readProjectList({ force = false }) {
  let url = new URL(todoAPIUrl + "/api/private/v1/projects/");

  if (projects.value && projects.value.length !== 0 && !force)
    return { data: projects, error: ref(null) };

  const { data, error } = useFetch(url);

  watchEffect(() => {
    projects.value = data.value;
  });
  watchEffect(() => {
    isProjectsLoadingError.value = error.value;
  });
}

export function readProject(id) {
  return fetch(entity_url + id + "/", {
    method: "get",
    headers: todoAPIHeaders,
  }).then((response) => {
    if (!response.ok) {
      const error = new Error(response.statusText);
      error.json = response.json();
      throw error;
    }
    return response.json();
  });
}

export function updateProject(id, body) {
  return fetch(entity_url + id + "/", {
    method: "put",
    body: JSON.stringify(body),
    headers: todoAPIHeaders,
  })
    .then((response) => {
      if (!response.ok) {
        const error = new Error(response.statusText);
        error.json = response.json();
        throw error;
      }
      return response.json();
    })
    .then((json) => {
      projects.value.splice(findEntityIndexById(projects, id), 1, json.data);
      return json;
    });
}

export function archiveProject(id) {
  return fetch(entity_url + id + "/archive/", {
    method: "post",
    headers: todoAPIHeaders,
  })
    .then((response) => {
      if (!response.ok) {
        const error = new Error(response.statusText);
        error.json = response.json();
        throw error;
      }
      return response.json();
    })
    .then((json) => {
      projects.value.splice(findEntityIndexById(projects, id), 1, json.data);
      return json;
    });
}

export function restoreProject(id) {
  return fetch(entity_url + id + "/restore/", {
    method: "post",
    headers: todoAPIHeaders,
  })
    .then((response) => {
      if (!response.ok) {
        const error = new Error(response.statusText);
        error.json = response.json();
        throw error;
      }
      return response.json();
    })
    .then((json) => {
      projects.value.splice(findEntityIndexById(projects, id), 1, json.data);
      return json;
    });
}

export function deleteProject(id) {
  return fetch(entity_url + id + "/", {
    method: "delete",
    headers: todoAPIHeaders,
  })
    .then((response) => {
      if (response.status !== 204) {
        const error = new Error(response.statusText);
        error.json = response.json();
        throw error;
      }
    })
    .then((json) => {
      projects.value.splice(findEntityIndexById(projects, id), 1);
      return json;
    });
}
