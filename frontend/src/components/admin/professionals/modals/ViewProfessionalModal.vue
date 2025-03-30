<script setup>
import { inject } from "vue";

const professional = inject("professional");
</script>

<template>
    <div
        class="modal fade"
        id="viewProfessionalModal"
        tabindex="-1"
        aria-labelledby="viewProfessionalModal"
        aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="viewProfessionalModal">
                        Professional Details
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
                        <dt class="col-sm-4">ID</dt>
                        <dd class="col-sm-8">{{ professional.id }}</dd>

                        <dt class="col-sm-4">Name</dt>
                        <dd class="col-sm-8">{{ professional.name }}</dd>

                        <dt class="col-sm-4">Email</dt>
                        <dd class="col-sm-8">{{ professional.email }}</dd>

                        <dt class="col-sm-4">Active</dt>
                        <dd class="col-sm-8">{{ professional.active }}</dd>

                        <dt class="col-sm-4">Service</dt>
                        <dd class="col-sm-8">
                            {{ professional.service }}
                        </dd>

                        <dt class="col-sm-4">Description</dt>
                        <dd class="col-sm-8">
                            {{ professional.description }}
                        </dd>

                        <dt class="col-sm-4">Date Created</dt>
                        <dd class="col-sm-8">
                            {{ professional.date_created }}
                        </dd>

                        <dt class="col-sm-4">Experience</dt>
                        <dd class="col-sm-8">
                            {{ professional.experience }}
                        </dd>

                        <dt class="col-sm-4">Status</dt>
                        <dd class="col-sm-8">
                            {{ professional.status }}
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
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
