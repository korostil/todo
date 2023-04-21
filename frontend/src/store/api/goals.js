import { todoAPIHeaders, todoAPIUrl, useFetch } from "@/store/api/base";

const entity_url = new URL(todoAPIUrl + "/api/private/v1/goals/");

export function createGoal(body) {
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

export function readGoalList({
  archived = null,
  search = null,
  month = null,
  year = null,
}) {
  let url = new URL(todoAPIUrl + "/api/private/v1/goals/");

  if (archived !== null && archived !== "null") {
    url.searchParams.set("archived", archived);
  }
  if (search !== null && search !== "null") {
    url.searchParams.set("search", search);
  }
  if (month !== null && month !== "null") {
    url.searchParams.set("month", month);
  }
  if (year !== null && year !== "null") {
    url.searchParams.set("year", year);
  }

  return useFetch(url);
}

export function readGoal(id) {
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

export function updateGoal(id, body) {
  return fetch(entity_url + id + "/", {
    method: "put",
    body: JSON.stringify(body),
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

export function deleteGoal(id) {
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
