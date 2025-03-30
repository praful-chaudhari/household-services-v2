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
            meta: {
                guest: true,
            },
            component: HomeView,
        },
        {
            path: "/auth",
            component: LoginRegisterView,
            meta: {
                guest: true,
            },
            redirect: { name: "login" },
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
        },
        {
            path: "/admin-dashboard",
            name: "AdminDashboard",
            component: () => import("@/views/AdminDashboardView.vue"),
            meta: {
                requiresAuth: true,
                requiresUserRole: "admin",
            },
            redirect: { name: "AdminServices" },
            children: [
                {
                    path: "services",
                    name: "AdminServices",
                    component: () =>
                        import("@/components/admin/services/Services.vue"),
                },
                {
                    path: "professionals",
                    name: "AdminProfessionals",
                    component: () =>
                        import(
                            "@/components/admin/professionals/Professionals.vue"
                        ),
                },
                {
                    path: "customers",
                    name: "AdminCustomers",
                    component: () =>
                        import("@/components/admin/customers/Customers.vue"),
                },
                {
                    path: "service-requests",
                    name: "AdminServiceRequests",
                    component: () =>
                        import("@/components/admin/service_requests/ServiceRequests.vue"),
                },
                {
                    path: "statistics",
                    name: "AdminStatistics",
                    component: () =>
                        import("@/components/admin/Statistics.vue"),
                },
            ],
        },
        {
            path: "/customer-dashboard",
            name: "CustomerDashboard",
            meta: {
                requiresAuth: true,
                requiresUserRole: "customer",
            },
            component: () => import("@/views/CustomerDashboardView.vue"),
            redirect: { name: "AvailableServices" },
            children: [
                {
                    path: "available-services",
                    name: "AvailableServices",
                    component: () =>
                        import("@/components/customer/AvailableServices.vue"),
                },
                {
                    path: "service-details/:id",
                    name: "ServiceDetails",
                    component: () =>
                        import("@/components/customer/ServiceDetails.vue"),
                },
                {
                    path: "service-requests",
                    name: "CustomerServiceRequests",
                    component: () =>
                        import("@/components/customer/ServiceRequests.vue"),
                },
                {
                    path: "statistics",
                    name: "CustomerStatistics",
                    component: () =>
                        import("@/components/customer/Statistics.vue"),
                },
            ],
        },
        {
            path: "/professional-dashboard",
            name: "ProfessionalDashboard",
            meta: {
                requiresAuth: true,
                requiresUserRole: "professional",
            },
            component: () => import("@/views/ProfessionalDashboardView.vue"),
            redirect: { name: "ProfessionalServiceRequests" },
            children: [
                {
                    path: "service-requests",
                    name: "ProfessionalServiceRequests",
                    component: () =>
                        import("@/components/professional/ServiceRequests.vue"),
                },
                {
                    path: "statistics",
                    name: "ProfessionalStatistics",
                    component: () =>
                        import("@/components/professional/Statistics.vue"),
                },
            ],
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

router.beforeEach((to, from, next) => {
    const store = userStore();
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (store.isAuthenticated) {
            // Check if user has the required role
            const requiredRole = to.meta.requiresUserRole;
            if (store.getRoles.includes(requiredRole)) {
                next();
            } else {
                // If user doesn't have required role, redirect to their appropriate dashboard
                next({
                    name: store.getRoles.includes("admin")
                        ? "AdminDashboard"
                        : store.getRoles.includes("customer")
                        ? "CustomerDashboard"
                        : "ProfessionalDashboard",
                });
            }
        } else {
            next({ name: "login" });
        }
    } else if (to.matched.some((record) => record.meta.guest)) {
        if (store.isAuthenticated) {
            // If authenticated user tries to access guest routes, redirect to their dashboard
            next({
                name: store.getRoles.includes("admin")
                    ? "AdminDashboard"
                    : store.getRoles.includes("customer")
                    ? "CustomerDashboard"
                    : "ProfessionalDashboard",
            });
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;
