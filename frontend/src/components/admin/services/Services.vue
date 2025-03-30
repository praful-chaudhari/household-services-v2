<script setup>
import AddNewServiceModal from "@/components/admin/services/modals/AddNewServiceModal.vue";
import EditServiceModal from "@/components/admin/services/modals/EditServiceModal.vue";
import DeleteServiceModal from "@/components/admin/services/modals/DeleteServiceModal.vue";
import ViewServiceModal from "@/components/admin/services/modals/ViewServiceModal.vue";
import { fetchServices } from "@/shared/fetchServices";
import { onMounted, ref, provide, reactive, computed } from "vue";
import { useToast } from "vue-toastification";

const toast = useToast();

const services = ref([]);
const currentService = reactive({});

provide("service", currentService);

const loadServices = async () => {
    try {
        services.value = await fetchServices();
    } catch (error) {
        console.error(error);
    }
};

provide("loadServices", loadServices);

const setCurrentService = (service) => {
    Object.assign(currentService, service);
};

onMounted(() => {
    loadServices();
});

const searchQuery = ref('');
const filteredServices = computed(() => {
    return services.value.filter(service => 
        service.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        service.base_price.toString().includes(searchQuery.value) ||
        service.time_required.toString().includes(searchQuery.value)
    );
});

const filterServices = () => {
    if (searchQuery.value) {
        services.value = filteredServices.value;
    } else {
        loadServices();
    }
};

</script>

<template>
    <div
        v-if="services.length !== 0"
        class="d-flex justify-content-between align-items-center px-4 gap-3 mt-4"
    >
        <h4>Services</h4>
        <form class="d-flex align-items-center" role="search" @submit.prevent>
            <input
                class="form-control me-2 form-control-sm"
                type="search"
                placeholder="Search by name, price or time"
                aria-label="Search"
                v-model="searchQuery"
                @input="filterServices"
            />
            <i class="pi pi-search"></i>
        </form>
    </div>
    <div v-else class="d-flex justify-content-center mt-4">
        <h4>No Services found</h4>
    </div>
    <table v-if="services.length !== 0" class="table table-sm table-hover">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Service Name</th>
                <th scope="col">Base Price</th>
                <th scope="col">Time Required</th>
                <th scope="col">Action</th>
            </tr>
        </thead>
        <tbody class="table-group-divider">
            <tr v-for="(service, index) in services" :key="index">
                <th scope="row">
                    <button
                        class="btn btn-outline-info btn-sm"
                        @click.prevent="setCurrentService(service)"
                        data-bs-toggle="modal"
                        data-bs-target="#viewServiceModal"
                    >
                        {{ index + 1 }}
                    </button>
                </th>
                <td>{{ service.name }}</td>
                <td>$ {{ service.base_price }}</td>
                <td>{{ service.time_required }} minutes</td>
                <td>
                    <button
                        @click="setCurrentService(service)"
                        type="button"
                        class="btn btn-primary btn-sm"
                        data-bs-toggle="modal"
                        data-bs-target="#editServiceModal"
                    >
                        Edit
                        <span class="pi pi-pen-to-square ms-1"></span>
                    </button>
                    <span class="mx-2"></span>
                    <button
                        @click="setCurrentService(service)"
                        type="button"
                        class="btn btn-danger btn-sm"
                        data-bs-toggle="modal"
                        data-bs-target="#confirmDeleteModal"
                    >
                        Delete
                        <span class="pi pi-trash ms-1"></span>
                    </button>
                </td>
            </tr>
        </tbody>
        <tfoot>
            <tr>
                <td scope="row" colspan="12"></td>
            </tr>
        </tfoot>
    </table>

    <div class="d-flex justify-content-center">
        <!-- Button trigger modal -->
        <button
            type="button"
            class="btn btn-primary btn-sm mt-2"
            data-bs-toggle="modal"
            data-bs-target="#addNewServiceModal"
        >
            Add New Service
        </button>
    </div>

    <AddNewServiceModal />

    <EditServiceModal />

    <DeleteServiceModal />

    <ViewServiceModal />
</template>
