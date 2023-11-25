import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import FileUploadView from "../views/FileUploadView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: FileUploadView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
