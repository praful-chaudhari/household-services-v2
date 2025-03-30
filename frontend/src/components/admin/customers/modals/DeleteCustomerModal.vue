<script setup>
import axios from "@/utils/axios.js";
import { inject } from "vue";
import { useToast } from "vue-toastification";

const toast = useToast();

const customer = inject("customer");
const fetchCustomers = inject("fetchCustomers");

const deleteCustomer = async (userId) => {
    try {
        await axios.delete(`/customers/${userId}`);
        fetchCustomers();
        toast.success("Customer deleted successfully!");
    } catch (error) {
        console.error(error);
    }
};
</script>

<template>
    <div
        class="modal fade"
        id="confirmDeleteModal"
        tabindex="-1"
        aria-labelledby="confirmDeleteModalLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="confirmDeleteModalLabel">
                        Are you sure want to delete customer?
                    </h1>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    <dl class="row">
                        <dt class="col-sm-4">Name</dt>
                        <dd class="col-sm-8">{{ customer.name }}</dd>

                        <dt class="col-sm-4">Email</dt>
                        <dd class="col-sm-8">{{ customer.email }}</dd>

                        <dt class="col-sm-4">Active</dt>
                        <dd class="col-sm-8">{{ customer.active }}</dd>
                    </dl>
                </div>
                <div
                    class="modal-footer d-flex justify-content-center align-items-center"
                >
                    <button
                        type="button"
                        class="btn btn-primary"
                        data-bs-dismiss="modal"
                    >
                        Cancel
                    </button>
                    <button
                        @click="deleteCustomer(customer.id)"
                        type="button"
                        class="btn btn-danger"
                        data-bs-dismiss="modal"
                    >
                        Delete
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
