<script setup>
import { ref, onMounted, computed } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { userStore } from "@/stores/userStore";
import { useToast } from "vue-toastification";
import axios from "@/utils/axios.js";
import { fetchServices } from "@/shared/fetchServices.js";

const router = useRouter();
const store = userStore();
const toast = useToast();

const theme = ref(localStorage.getItem("theme") || "light");
const isEditing = ref(false);

const services = ref([]);
const currentService = computed(() => {
    if (!store.isProfessional || !store.user.service_id) return null;
    return services.value.find(s => s.id === store.user.service_id);
});

const toggleTheme = () => {
    theme.value = theme.value === "light" ? "dark" : "light";
    localStorage.setItem("theme", theme.value);
    document.documentElement.setAttribute("data-bs-theme", theme.value);
};

const loadServices = async () => {
    try {
        services.value = await fetchServices();
    } catch (error) {
        console.error(error);
        toast.error("Error loading services");
    }
};

onMounted(() => {
    document.documentElement.setAttribute("data-bs-theme", theme.value);
    if (store.isProfessional) {
        loadServices();
    }
});

const handleLogout = () => {
    store.logout();
    router.push("/auth/login");
};

const profileForm = ref({
    name: store.user.name,
    oldPassword: "",
    newPassword: "",
    service: store.isProfessional ? store.user.service : "",
    description: store.isProfessional ? store.user.description : "",
});

const resetProfileForm = () => {
    profileForm.value = {
        name: store.user.name,
        oldPassword: "",
        newPassword: "",
        service: store.isProfessional ? store.user.service : "",
        description: store.isProfessional ? store.user.description : "",
    };
    isEditing.value = false;
};

const updateProfile = async () => {
    try {
        await axios.patch(`/profile/${store.user.id}`, profileForm.value);
        store.user.name = profileForm.value.name;
        if (profileForm.value.newPassword) {
            store.user.password = profileForm.value.newPassword;
        }
        if (store.isProfessional) {
            store.user.service = profileForm.value.service;
            store.user.description = profileForm.value.description;
        }
        toast.success("Profile updated successfully");
        resetProfileForm();
    } catch (error) {
        console.error(error);
        toast.error(error.response?.data?.message || "Error updating profile");
    }
};

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
                        <div v-if="!store.isAuthenticated" class="d-flex">
                            <li class="nav-item mx-3">
                                <RouterLink class="nav-link" to="/auth/login"
                                    >Login
                                    <i class="pi pi-sign-in ms-1"></i>
                                </RouterLink>
                            </li>
                            <li class="nav-item mx-3">
                                <RouterLink class="nav-link" to="/auth/register"
                                    >Register <i class="pi pi-user-plus ms-1"></i
                                ></RouterLink>
                            </li>
                        </div>
                        <div v-else-if="store.isAuthenticated && store.isAdmin" class="d-flex">
                            <li
                                class="nav-item mx-3"
                            >
                                <RouterLink
                                    class="nav-link"
                                    to="/admin-dashboard/services"
                                    >Services</RouterLink
                                >
                            </li>
                            <li
                                class="nav-item mx-3"
                            >
                                <RouterLink
                                    class="nav-link"
                                    to="/admin-dashboard/customers"
                                    >Customers</RouterLink
                                >
                            </li>
                            <li
                                class="nav-item mx-3"
                            >
                                <RouterLink
                                    class="nav-link"
                                    to="/admin-dashboard/professionals"
                                    >Professionals</RouterLink
                                >
                            </li>
                            <li
                                class="nav-item mx-3"
                            >
                                <RouterLink
                                    class="nav-link"
                                    to="/admin-dashboard/service-requests"
                                    >Service Requests</RouterLink
                                >
                            </li>
                            <li
                                class="nav-item mx-3"
                            >
                                <RouterLink
                                    class="nav-link"
                                    to="/admin-dashboard/statistics"
                                    >Statistics</RouterLink
                                >
                            </li>
                        </div>
                        <div v-else-if="store.isAuthenticated && store.isCustomer" class="d-flex">
                            <li class="nav-item mx-3">
                                <RouterLink class="nav-link" to="/customer-dashboard/available-services"
                                    >Available Services</RouterLink
                                >
                            </li>
                            <li class="nav-item mx-3">
                                <RouterLink class="nav-link" to="/customer-dashboard/service-requests"
                                    >Service Requests</RouterLink
                                >
                            </li>
                            <li class="nav-item mx-3">
                                <RouterLink class="nav-link" to="/customer-dashboard/statistics"
                                    >Statistics</RouterLink
                                >
                            </li>
                        </div>
                        <div v-else-if="store.isAuthenticated && store.isProfessional" class="d-flex">
                            <li class="nav-item mx-3">
                                <RouterLink class="nav-link" to="/professional-dashboard/service-requests"
                                    >Service Requests</RouterLink
                                >
                            </li>
                            <li class="nav-item mx-3">
                                <RouterLink class="nav-link" to="/professional-dashboard/statistics"
                                    >Statistics</RouterLink
                                >
                            </li>
                        </div>
                        <li class="nav-item mx-3">
                            <button @click="toggleTheme" class="nav-link">
                                Theme
                                <i
                                    v-if="theme === 'light'"
                                    class="pi pi-sun ms-1"
                                ></i>
                                <i
                                    v-if="theme === 'dark'"
                                    class="pi pi-moon ms-1"
                                ></i>
                            </button>
                        </li>
                    </ul>
                    <div class="d-flex" v-if="store.isAuthenticated">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            <li class="nav-item mx-2">
                                <button 
                                    class="nav-link"
                                    data-bs-toggle="modal"
                                    data-bs-target="#profileModal"
                                    @click="resetProfileForm"
                                >
                                    Welcome, {{ store.user.name }}
                                    <span class="pi pi-user ms-1"></span>
                                </button>
                            </li>

                            <!-- Profile Modal -->
                            <div class="modal fade" id="profileModal" tabindex="-1">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title">Profile Details</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" @click="resetProfileForm"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div v-if="!isEditing">
                                                <div class="mb-3">
                                                    <label class="fw-bold">Name:</label>
                                                    <div>{{ store.user.name }}</div>
                                                </div>
                                                <div class="mb-3">
                                                    <label class="fw-bold">Email:</label>
                                                    <div>{{ store.user.email }}</div>
                                                </div>
                                                <div v-if="store.isProfessional" class="mb-3">
                                                    <label class="fw-bold">Service:</label>
                                                    <div>{{ currentService?.name }} - ${{ currentService?.base_price }} ({{ currentService?.time_required }} mins)</div>
                                                </div>
                                                <div v-if="store.isProfessional" class="mb-3">
                                                    <label class="fw-bold">Description:</label>
                                                    <div>{{ currentService?.description }}</div>
                                                </div>
                                                <button @click="isEditing = true" class="btn btn-primary">Edit Profile</button>
                                            </div>

                                            <form v-else @submit.prevent>
                                                <div class="form-group mb-3">
                                                    <label class="form-label">Name</label>
                                                    <input type="text" class="form-control" v-model="profileForm.name" required>
                                                </div>
                                                <div class="form-group mb-3">
                                                    <label class="form-label">Old Password</label>
                                                    <input type="password" class="form-control" v-model="profileForm.oldPassword" required>
                                                </div>
                                                <div class="form-group mb-3">
                                                    <label class="form-label">New Password</label>
                                                    <input type="password" class="form-control" v-model="profileForm.newPassword" required>
                                                </div>
                                                <div v-if="store.isProfessional" class="form-group mb-3">
                                                    <label class="form-label">Service</label>
                                                    <select class="form-control" v-model="profileForm.service" required>
                                                        <option disabled value="">Select a service</option>
                                                        <option v-for="service in services" :key="service.id" :value="service.id">
                                                            {{ service.name }} - ${{ service.base_price }} ({{ service.time_required }} mins)
                                                        </option>
                                                    </select>
                                                </div>
                                                <div v-if="store.isProfessional" class="form-group mb-3">
                                                    <label class="form-label">Description</label>
                                                    <textarea class="form-control" v-model="profileForm.description" required></textarea>
                                                </div>
                                                <div class="d-flex gap-2">
                                                    <button type="submit" @click="updateProfile" class="btn btn-primary" data-bs-dismiss="modal">Save Changes</button>
                                                    <button type="button" @click="resetProfileForm" class="btn btn-secondary">Cancel</button>
                                                </div>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <li class="nav-item">
                                <button
                                    @click="handleLogout"
                                    class="nav-link btn btn-outline-danger"
                                >
                                    Logout
                                    <i class="pi pi-sign-out ms-1"></i>
                                </button>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>
    </div>
</template>
