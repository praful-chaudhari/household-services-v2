<script setup>
import EditServiceForm from "@/components/admin/services/forms/EditServiceForm.vue";
</script>

<template>
    <div
        class="modal fade"
        id="editServiceModal"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        tabindex="-1"
        aria-labelledby="editServiceModalLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header text-center">
                    <h1 class="modal-title fs-5" id="editServiceModalLabel">
                        Edit Service
                    </h1>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    <EditServiceForm />
                </div>
                <div
                    class="modal-footer d-flex justify-content-center align-items-center"
                >
                    <button
                        type="button"
                        class="btn btn-secondary"
                        data-bs-dismiss="modal"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
