<script setup>
import { computed, inject, reactive, ref, watch } from "vue";
import axios from "@/utils/axios.js";
import { useToast } from "vue-toastification";

const toast = useToast();

const service = inject("service");
const loadServices = inject("loadServices");

const isNameValid = ref(true);
const isBasePriceValid = ref(true);
const isTimeRequiredValid = ref(true);
const isDescriptionValid = ref(true);

const isNameTouched = ref(false);
const isBasePriceTouched = ref(false);
const isTimeRequiredTouched = ref(false);
const isDescriptionTouched = ref(false);

watch(
    () => service.name,
    (name) => {
        if (!isNameTouched.value && name) {
            isNameTouched.value = true;
        }
        isNameValid.value = name.trim().length > 0;
    }
);

watch(
    () => service.base_price,
    (base_price) => {
        if (!isBasePriceTouched.value && base_price) {
            isBasePriceTouched.value = true;
        }
        isBasePriceValid.value = base_price > 0 && base_price <= 500;
    }
);

watch(
    () => service.time_required,
    (time_required) => {
        if (!isTimeRequiredTouched.value && time_required) {
            isTimeRequiredTouched.value = true;
        }
        isTimeRequiredValid.value = time_required >= 10 && time_required <= 600;
    }
);

watch(
    () => service.description,
    (description) => {
        if (!isDescriptionTouched.value && description) {
            isDescriptionTouched.value = true;
        }
        isDescriptionValid.value = description.trim().length > 10;
    }
);

const isFormInvalid = computed(() => {
    return !(
        isNameValid.value &&
        isBasePriceValid.value &&
        isTimeRequiredValid.value &&
        isDescriptionValid.value &&
        service.name &&
        service.base_price &&
        service.time_required &&
        service.description
    );
});

const editService = async () => {
    if (!isFormInvalid.value) {
        try {
            const response = await axios.patch(`/services/${service.id}`, {
                name: service.name,
                basePrice: service.base_price,
                timeRequired: service.time_required,
                description: service.description,
            });
            loadServices();
            toast.success(response.data.message);
        } catch (error) {
            console.error(error);
            toast.error("Error editing service");
        }
    }
};
</script>

<template>
    <div class="d-flex justify-content-center align-items-center">
        <form @submit.prevent="editService">
            <div class="form-group mb-3">
                <label class="form-label">Name</label>
                <input
                    v-model="service.name"
                    type="text"
                    class="form-control"
                    :class="{
                        'is-invalid': !isNameValid && isNameTouched,
                    }"
                    placeholder="e.g. Plumbing"
                    required
                />
                <small v-if="!isNameValid && isNameTouched" style="color: red"
                    >Please enter valid service name</small
                >
            </div>
            <div class="form-group mb-4">
                <label class="form-label">Base Price</label>
                <input
                    v-model="service.base_price"
                    type="number"
                    class="form-control"
                    :class="{
                        'is-invalid': !isBasePriceValid && isBasePriceTouched,
                    }"
                    placeholder="100"
                    required
                />
                <small
                    v-if="!isBasePriceValid && isBasePriceTouched"
                    style="color: red"
                    >Please enter valid base price</small
                >
            </div>
            <div class="form-group mb-4">
                <label class="form-label">Time Required (In minutes)</label>
                <input
                    v-model="service.time_required"
                    type="number"
                    class="form-control"
                    :class="{
                        'is-invalid':
                            !isTimeRequiredValid && isTimeRequiredTouched,
                    }"
                    placeholder="60"
                    required
                />
                <small
                    v-if="!isTimeRequiredValid && isTimeRequiredTouched"
                    style="color: red"
                    >Please enter valid time</small
                >
            </div>
            <div class="form-group mb-4">
                <label class="form-label">Description</label>
                <textarea
                    v-model="service.description"
                    type="text"
                    class="form-control"
                    :class="{
                        'is-invalid':
                            isDescriptionTouched && !isDescriptionValid,
                    }"
                    placeholder="Repairing tap..."
                    required
                />
                <small
                    v-if="!isDescriptionValid && isDescriptionTouched"
                    style="color: red"
                    >Please enter valid description at least 10 characters
                    long</small
                >
            </div>
            <button
                class="btn btn-primary w-100"
                data-bs-dismiss="modal"
                type="submit"
                :disabled="isFormInvalid"
            >
                Save
            </button>
        </form>
    </div>
</template>
