import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import LoginRegisterView from "@/views/LoginRegisterView.vue";
import { userStore } from "@/stores/userStore";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            component: HomeView,
            beforeEnter: (to, from, next) => {
                const store = userStore();
                if (store.isAuthenticated) {
                    next("/dashboard");
                } else {
                    next();
                }
            },
        },
        {
            path: "/auth",
            component: LoginRegisterView,
            children: [
                {
                    path: "login",
                    name: "login",
                    component: () => import("@/components/LoginForm.vue"),
                },
                {
                    path: "register",
                    name: "register",
                    component: () => import("@/components/RegisterForm.vue"),
                },
            ],
            beforeEnter: (to, from, next) => {
                const store = userStore();
                if (store.isAuthenticated) {
                    next("/dashboard");
                } else {
                    next();
                }
            },
        },
        {
            path: "/dashboard",
            name: "dashboard",
            component: () => import("@/views/DashboardView.vue"),
            beforeEnter: (to, from, next) => {
                const store = userStore();
                if (store.isAuthenticated) {
                    next();
                } else {
                    next("/auth/login");
                }
            },
        },
        // {
        //   path: '/about',
        //   name: 'about',
        //   // route level code-splitting
        //   // this generates a separate chunk (About.[hash].js) for this route
        //   // which is lazy-loaded when the route is visited.
        //   component: () => import('../views/AboutView.vue'),
        // },
    ],
});

export default router;
