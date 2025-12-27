import Vue from "vue";
import VueRouter from "vue-router";


Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("../views/Home.vue"),  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("../components/Dashboard.vue"),
  },
  {
    path: "/estudantes",
    name: "estudantes",
    component: () => import("../components/CardEstudantes.vue"),
  },
  {
    path: "/sobre",
    name: "sobre",
    component: () => import("../views/Sobre.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/Login.vue"),
  },
  {
    path: "/tutorial",
    name: "tutorial",
    component: () => import("../views/Tutorial.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
