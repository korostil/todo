export const routes = [
  {
    path: "/projects/",
    name: "project_list",
    component: () => import("../views/projects/ProjectListView.vue"),
  },
];
