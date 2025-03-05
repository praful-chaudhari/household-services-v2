<script setup>
import { ref, onMounted } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { userStore } from "@/stores/userStore";

const router = useRouter();
const store = userStore();

const theme = ref(localStorage.getItem("theme") || "light");

const handleLogout = () => {
    store.logout();
    router.push("/auth/login");
};

const toggleTheme = () => {
    theme.value = theme.value === "light" ? "dark" : "light";
    localStorage.setItem("theme", theme.value);
    document.documentElement.setAttribute("data-bs-theme", theme.value);
};

onMounted(() => {
    document.documentElement.setAttribute("data-bs-theme", theme.value);
});
</script>

<template>
    <div class="container">
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <RouterLink class="navbar-brand" to="/">FixItFixIt</RouterLink>
                <button
                    class="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div
                    class="collapse navbar-collapse"
                    id="navbarSupportedContent"
                >
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li v-if="!store.isAuthenticated" class="nav-item mx-3">
                            <RouterLink class="nav-link" to="/auth/login"
                                >Login
                                <i
                                    class="pi pi-sign-in ms-1"
                                    style="font-size: 1rem"
                                ></i>
                            </RouterLink>
                        </li>
                        <li v-if="!store.isAuthenticated" class="nav-item mx-3">
                            <RouterLink class="nav-link" to="/auth/register"
                                >Register
                                <i
                                    class="pi pi-user-plus ms-1"
                                    style="font-size: 1rem"
                                ></i
                            ></RouterLink>
                        </li>
                        <li v-if="store.isAuthenticated" class="nav-item mx-3">
                            <button @click="handleLogout" class="nav-link">
                                Logout
                                <i
                                    class="pi pi-sign-out ms-1"
                                    style="font-size: 1rem"
                                ></i>
                            </button>
                        </li>
                        <li class="nav-item mx-3">
                            <button @click="toggleTheme" class="nav-link">
                                Theme
                                <i
                                    v-if="theme === 'light'"
                                    class="pi pi-sun ms-1"
                                    style="font-size: 1rem"
                                ></i>
                                <i
                                    v-if="theme === 'dark'"
                                    class="pi pi-moon ms-1"
                                    style="font-size: 1rem"
                                ></i>
                            </button>
                        </li>
                    </ul>
                    <form class="d-flex" role="search">
                        <input
                            class="form-control me-2"
                            type="search"
                            placeholder="Search"
                            aria-label="Search"
                        />
                        <button class="btn btn-outline-success" type="submit">
                            Search
                        </button>
                    </form>
                </div>
            </div>
        </nav>
    </div>
</template>
