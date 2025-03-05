<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
    <div class="px-4 py-5 text-center">
        <div class="py-5">
            <h1 class="display-5 fw-bold">FixItFixIt</h1>
            <div class="col-lg-6 mx-auto">
                <p class="fs-5 mb-5">Your Local Handyman Service</p>
                <p class="fs-5 mb-2">
                    <span class="fw-bold"
                        >Need help with home repairs, installations, or
                        maintenance?</span
                    >
                </p>
                <p>We've got you covered.</p>
                <div class="d-grid gap-2 mt-5 d-sm-flex justify-content-center">
                    <RouterLink
                        to="/auth/login"
                        class="btn btn-outline-secondary btn-lg px-4 me-sm-3 fw-bold"
                    >
                        Login
                    </RouterLink>
                    <RouterLink
                        to="/auth/register"
                        class="btn btn-info btn-lg px-4 fw-bold"
                    >
                        Register
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>
