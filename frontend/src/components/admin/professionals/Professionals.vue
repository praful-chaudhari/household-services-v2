<script setup>
import DeleteProfessionalModal from "@/components/admin/professionals/modals/DeleteProfessionalModal.vue";
import ViewProfessionalModal from "@/components/admin/professionals/modals/ViewProfessionalModal.vue";
import axios from "@/utils/axios.js";
import { formatDate } from "@/shared/formatDate";
import { computed, onMounted, provide, reactive, ref } from "vue";
import { useToast } from "vue-toastification";

const toast = useToast();

const professionals = ref([]);
const currentProfessional = reactive({});

provide("professional", currentProfessional);

const retryCount = ref(0);

const fetchProfessionals = async () => {
    try {
        const response = await axios.get("/professionals");
        professionals.value = response.data;
        retryCount.value = 0;
    } catch (error) {
        if (retryCount < 5) {
            retryCount.value++;
            const backOffTime = Math.pow(2, retryCount.value) * 1000;
            await new Promise((resolve) => setTimeout(resolve, backOffTime));
            await fetchProfessionals();
        } else {
            console.error("Error fetching professionals.", error);
        }
    }
};

provide("fetchProfessionals", fetchProfessionals);

onMounted(() => {
    fetchProfessionals();
});

const setCurrentProfessional = (professional) => {
    Object.assign(currentProfessional, professional);
};

const formattedProfessionals = computed(() => {
    return professionals.value.map((professional) => {
        return {
            ...professional,
            date_created: formatDate(professional.date_created),
        };
    });
});

const changeProfessionalStatus = async (professionalId, status) => {
    try {
        await axios.patch(`/professionals/${professionalId}`, {
            status: status,
        });
        fetchProfessionals();
        toast.success(`Professional ${status} successfully!`);
    } catch (error) {
        console.error(error);
        toast.error("Error approving professional");
    }
};

const blockUnblockProfessional = async (userId, status) => {
    try {
        await axios.patch(`/professionals/${userId}`, {
            active: status,
        });
        fetchProfessionals();
        toast.success(
            `Professional ${status ? "unblocked" : "blocked"} successfully!`
        );
    } catch (error) {
        console.error(error);
    }
};

const searchQuery = ref('');
const filteredProfessionals = computed(() => {
    return professionals.value.filter(professional => 
        professional.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        professional.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        professional.service.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        professional.experience.toString().includes(searchQuery.value)
    );
});

const filterProfessionals = () => {
    if (searchQuery.value) {
        professionals.value = filteredProfessionals.value;
    } else {
        fetchProfessionals();
    }
};

</script>

<template>
    <div
        class="d-flex justify-content-between align-items-center px-4 gap-3 mt-4"
    >
        <h4>Professionals</h4>
        <form class="d-flex align-items-center" role="search" @submit.prevent>
            <input
                class="form-control me-2 form-control-sm"
                type="search"
                placeholder="Search by name, email, service or experience"
                aria-label="Search"
                v-model="searchQuery"
                @input="filterProfessionals"
            />
            <i class="pi pi-search"></i>
        </form>
    </div>
    <div v-if="professionals.length === 0" class="d-flex justify-content-center mt-4">
        <h4>No professionals found</h4>
    </div>

    <table v-if="professionals.length !== 0" class="table table-sm table-hover">
        <thead>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Email</th>
                <th>Service</th>
                <th>Date Created</th>
                <th>Experience</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody class="table-group-divider">
            <tr
                v-for="(professional, index) in formattedProfessionals"
                :key="index"
            >
                <th scope="row">
                    <button
                        class="btn btn-outline-info btn-sm"
                        @click.prevent="setCurrentProfessional(professional)"
                        data-bs-toggle="modal"
                        data-bs-target="#viewProfessionalModal"
                    >
                        {{ index + 1 }}
                    </button>
                </th>
                <td>
                    {{ professional.name }}
                    <span
                        v-if="
                            professional.status === 'approved' &&
                            !professional.active
                        "
                        class="badge bg-danger badge-sm"
                    >
                        Blocked
                    </span>
                    <span
                        v-else-if="professional.status === 'pending'"
                        class="badge bg-warning text-dark badge-sm"
                    >
                        Pending
                    </span>
                    <span
                        v-else-if="professional.status === 'approved'"
                        class="badge bg-success badge-sm"
                    >
                        Approved
                    </span>
                    <span
                        v-else-if="professional.status === 'rejected'"
                        class="badge bg-secondary badge-sm"
                    >
                        Rejected
                    </span>
                </td>
                <td>{{ professional.email }}</td>
                <td>{{ professional.service.name }}</td>
                <td>{{ professional.date_created }}</td>
                <td>{{ professional.experience }} year(s)</td>
                <td>
                    <button
                        v-if="professional.status === 'pending'"
                        @click="
                            changeProfessionalStatus(
                                professional.id,
                                'approved'
                            )
                        "
                        type="button"
                        class="btn btn-success btn-sm"
                    >
                        Approve
                        <span class="pi pi-check-circle ms-1"></span>
                    </button>
                    <span
                        v-if="professional.status === 'pending'"
                        class="mx-1"
                    ></span>
                    <button
                        v-if="professional.status === 'pending'"
                        @click="
                            changeProfessionalStatus(
                                professional.id,
                                'rejected'
                            )
                        "
                        type="button"
                        class="btn btn-secondary btn-sm"
                    >
                        Reject
                        <span class="pi pi-times-circle ms-1"></span>
                    </button>
                    <button
                        v-if="
                            professional.status === 'approved' &&
                            professional.active
                        "
                        @click="
                            blockUnblockProfessional(professional.id, false)
                        "
                        type="button"
                        class="btn btn-warning text-dark btn-sm"
                    >
                        Block
                        <span class="pi pi-ban ms-1"></span>
                    </button>
                    <button
                        v-if="
                            professional.status === 'approved' &&
                            !professional.active
                        "
                        @click="blockUnblockProfessional(professional.id, true)"
                        type="button"
                        class="btn btn-success btn-sm"
                    >
                        Unblock
                        <span class="pi pi-check-circle ms-1"></span>
                    </button>
                    <span
                        v-if="
                            professional.status === 'approved' &&
                            !professional.active
                        "
                        class="mx-1"
                    ></span>
                    <button
                        v-if="
                            professional.status === 'rejected' ||
                            !professional.active
                        "
                        @click="setCurrentProfessional(professional)"
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

    <DeleteProfessionalModal />

    <ViewProfessionalModal />
</template>
