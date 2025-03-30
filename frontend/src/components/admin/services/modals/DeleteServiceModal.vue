<script setup>
import axios from "@/utils/axios.js";
import { inject } from "vue";
import { useToast } from "vue-toastification";

const toast = useToast();

const service = inject("service");
const loadServices = inject("loadServices");

const deleteService = async (serviceId) => {
    try {
        await axios.delete(`/services/${serviceId}`);
        loadServices();
        toast.success("Service deleted successfully!");
    } catch (error) {
        console.error(error);
        toast.error("An error occurred while deleting service!");
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
                        Are you sure want to delete service?
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
                        <dd class="col-sm-8">{{ service.name }}</dd>

                        <dt class="col-sm-4">Base Price</dt>
                        <dd class="col-sm-8">$ {{ service.base_price }}</dd>

                        <dt class="col-sm-4">Time Required</dt>
                        <dd class="col-sm-8">
                            {{ service.time_required }} minues
                        </dd>

                        <dt class="col-sm-4">Description</dt>
                        <dd class="col-sm-8">
                            {{ service.description }}
                        </dd>
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
                        @click="deleteService(service.id)"
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
