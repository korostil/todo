export const routes = [
  {
    path: "/tasks/",
    name: "task_list",
    component: () => import("../views/tasks/TaskListView.vue"),
  },
  {
    path: "/tasks/:task_id/",
    name: "task",
    component: () => import("../views/tasks/TaskView.vue"),
  },
  {
    path: "/tasks/completed/",
    name: "completed_tasks",
    component: () => import("../views/tasks/CompletedTaskView.vue"),
  },
];
