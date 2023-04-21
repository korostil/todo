import { ref, isRef, unref, watchEffect } from "vue";

export const todoAPIUrl = import.meta.env.VITE_TODO_API_URL,
  todoAPIHeaders = {
    "content-type": "application/json",
    Authorization: "Bearer " + import.meta.env.VITE_TODO_API_TOKEN,
  };

export function useFetch(url) {
  const data = ref(null);
  const error = ref(null);

  function doFetch() {
    data.value = null;
    error.value = null;
    fetch(unref(url), { method: "get", headers: todoAPIHeaders })
      .then((res) => res.json())
      .then((json) => (data.value = json.data))
      .catch((err) => (error.value = err));
  }

  if (isRef(url)) {
    watchEffect(doFetch);
  } else {
    doFetch();
  }

  return { data, error };
}
