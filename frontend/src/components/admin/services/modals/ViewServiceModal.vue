<script setup>
import { inject } from "vue";

const service = inject("service");
</script>

<template>
    <div
        class="modal fade"
        id="viewServiceModal"
        tabindex="-1"
        aria-labelledby="viewServiceModalLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="viewServiceModalLabel">
                        Service Details
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
                        <dd class="col-sm-8">{{ service.id }}</dd>

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
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
