import { todoAPIHeaders, todoAPIUrl, useFetch } from "@/store/api/base";

// TODO create new URL every time?
const entity_url = new URL(todoAPIUrl + "/api/private/v1/tasks/");

export function createTask(body) {
  return fetch(entity_url, {
    method: "post",
    body: JSON.stringify(body),
    headers: todoAPIHeaders,
  }).then((response) => {
    if (response.status !== 201) {
      const error = new Error(response.statusText);
      error.json = response.json();
      throw error;
    }
    return response.json();
  });
}

export function readTaskList({
  completed = null,
  decisive = null,
  due_from = null,
  due_to = null,
  inbox = null,
  project_id = null,
  search = null,
  space = null,
}) {
  let url = new URL(todoAPIUrl + "/api/private/v1/tasks/");
  // TODO find a right way to check null value
  if (completed !== null && completed !== "null") {
    url.searchParams.set("completed", completed);
  }
  if (project_id !== null && project_id !== "null") {
    url.searchParams.set("project_id", project_id);
  }
  if (search !== null && search !== "null") {
    url.searchParams.set("search", search);
  }
  if (space !== null && space !== "null") {
    url.searchParams.set("space", space);
  }
  if (decisive !== null && decisive !== "null") {
    url.searchParams.set("decisive", decisive);
  }
  if (due_from !== null && due_from !== "null") {
    url.searchParams.set("due_from", due_from);
  }
  if (due_to !== null && due_to !== "null") {
    url.searchParams.set("due_to", due_to);
  }
  if (inbox !== null && inbox !== "null") {
    url.searchParams.set("inbox", "true");
  }

  return useFetch(url);
}

export function readTask(id) {
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

export function updateTask(id, body) {
  return fetch(entity_url + id + "/", {
    method: "put",
    body: JSON.stringify(body),
    headers: todoAPIHeaders,
  }).then((response) => {
    if (response.status !== 200) {
      const error = new Error(response.statusText);
      error.json = response.json();
      throw error;
    }
    return response.json();
  });
}

export function deleteTask(id) {
  return fetch(entity_url + id + "/", {
    method: "delete",
    headers: todoAPIHeaders,
  }).then((response) => {
    if (response.status !== 204) {
      const error = new Error(response.statusText);
      error.json = response.json();
      throw error;
    }
  });
}

export function completeTask(id) {
  return fetch(entity_url + id + "/complete/", {
    method: "post",
    headers: todoAPIHeaders,
  }).then((response) => {
    if (!response.ok) {
      const error = new Error(response.statusText);
      error.json = response.json();
      throw error;
    }
  });
}

export function restoreTask(id) {
  return fetch(entity_url + id + "/reopen/", {
    method: "post",
    headers: todoAPIHeaders,
  }).then((response) => {
    if (!response.ok) {
      const error = new Error(response.statusText);
      error.json = response.json();
      throw error;
    }
  });
}
