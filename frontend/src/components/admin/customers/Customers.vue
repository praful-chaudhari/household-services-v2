<script setup>
import DeleteCustomerModal from "@/components/admin/customers/modals/DeleteCustomerModal.vue";
import ViewCustomerModal from "@/components/admin/customers/modals/ViewCustomerModal.vue";
import { onMounted, provide, reactive, ref, computed } from "vue";
import axios from "@/utils/axios";
import { useToast } from "vue-toastification";

const toast = useToast();

const customers = ref([]);
const currentCustomer = reactive({});

provide("customer", currentCustomer);

const retryCount = ref(0);

const fetchCustomers = async () => {
    try {
        const response = await axios.get("/customers");
        customers.value = response.data;
        retryCount.value = 0;
    } catch (error) {
        if (retryCount < 5) {
            retryCount.value++;
            const backOffTime = Math.pow(2, retryCount.value) * 1000;
            await new Promise((resolve) => setTimeout(resolve, backOffTime));
            await fetchCustomers();
        } else {
            console.error("Error fetching customers.", error);
        }
    }
};

provide("fetchCustomers", fetchCustomers);

onMounted(() => {
    fetchCustomers();
});

const setCurrentCustomer = (customer) => {
    Object.assign(currentCustomer, customer);
};

const changeCustomerStatus = async (customerId, status) => {
    try {
        await axios.patch(`/customers/${customerId}`, {
            active: status,
        });
        fetchCustomers();
        toast.success(
            `Customer ${status ? "unbloked" : "blocked"} successfully!`
        );
    } catch (error) {
        console.error(error);
        toast.error("Error occurred");
    }
};

const searchQuery = ref('');
const filteredCustomers = computed(() => {
    return customers.value.filter(customer => 
        customer.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        customer.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});

const filterCustomers = () => {
    if (searchQuery.value) {
        customers.value = filteredCustomers.value;
    } else {
        fetchCustomers();
    }
};

</script>

<template>
    <div
        class="d-flex justify-content-between align-items-center px-4 gap-3 mt-4"
    >
        <h4>Customers</h4>
        <form class="d-flex align-items-center" role="search" @submit.prevent>
            <input
                class="form-control me-2 form-control-sm"
                type="search"
                placeholder="Search by name or email"
                aria-label="Search"
                v-model="searchQuery"
                @input="filterCustomers"
            />
            <i class="pi pi-search"></i>
        </form>
    </div>
    <div v-if="customers.length === 0" class="d-flex justify-content-center mt-4">
        <h4>No customers found</h4>
    </div>

    <table v-if="customers.length !== 0" class="table table-sm table-hover">
        <thead>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Email</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody class="table-group-divider">
            <tr v-for="(customer, index) in customers" :key="index">
                <th scope="row">
                    <button
                        class="btn btn-outline-info btn-sm"
                        @click.prevent="setCurrentCustomer(customer)"
                        data-bs-toggle="modal"
                        data-bs-target="#viewCustomerModal"
                    >
                        {{ index + 1 }}
                    </button>
                </th>
                <td>
                    {{ customer.name }}
                    <span
                        v-if="!customer.active"
                        class="badge bg-danger badge-sm"
                    >
                        Blocked
                    </span>
                </td>
                <td>{{ customer.email }}</td>
                <td>
                    <button
                        v-if="customer.active"
                        @click="changeCustomerStatus(customer.id, false)"
                        type="button"
                        class="btn btn-warning text-dark btn-sm"
                    >
                        Block
                        <span class="pi pi-ban ms-1"></span>
                    </button>
                    <button
                        v-if="!customer.active"
                        @click="changeCustomerStatus(customer.id, true)"
                        type="button"
                        class="btn btn-success btn-sm"
                    >
                        Unblock
                        <span class="pi pi-check-circle ms-1"></span>
                    </button>
                    <span v-if="!customer.active" class="mx-1"></span>
                    <button
                        v-if="!customer.active"
                        @click="setCurrentCustomer(customer)"
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
    </table>

    <DeleteCustomerModal />

    <ViewCustomerModal />
</template>
