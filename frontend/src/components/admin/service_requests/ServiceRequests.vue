<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from '@/utils/axios.js';
import { useToast } from 'vue-toastification';
import { formatDate } from '@/shared/formatDate.js';

const toast = useToast();
const serviceRequests = ref([]);
const searchQuery = ref('');

const fetchServiceRequests = async () => {
    try {
        const response = await axios.get('/service-requests');
        serviceRequests.value = response.data;
    } catch (error) {
        console.error(error);
        toast.error('Error fetching service requests');
    }
};

const formattedRequests = computed(() => {
    return serviceRequests.value.map((request) => {
        return {
            ...request,
            date_of_request: formatDate(request.date_of_request),
            date_of_completion: request.date_of_completion ? formatDate(request.date_of_completion) : '-'
        };
    });
});

const filteredRequests = computed(() => {
    return serviceRequests.value.filter(request => 
        request.customer.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        request.professional.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        request.service.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        request.date_of_request.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        (request.date_of_completion ? request.date_of_completion.toLowerCase().includes(searchQuery.value.toLowerCase()) : false) ||
        request.address.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        request.customer_contact_number.toString().includes(searchQuery.value) ||
        request.status.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});

const filterRequests = () => {
    if (searchQuery.value) {
        serviceRequests.value = filteredRequests.value;
    } else {
        fetchServiceRequests();
    }
};

onMounted(() => {
    fetchServiceRequests();
});

const exportCSV = async () => {
    try {
        const response = await axios.get('/api/export');
        console.log(response);

        const checkStatus = async (taskId) => {
            try {
                const csvResponse = await axios.get(`/api/csv_result/${taskId}`);
                if (csvResponse.data) {
                    window.open(`http://localhost:5000/api/csv_result/${taskId}`, '_blank');
                    return true;
                }
                return false;
            } catch (error) {
                return false;
            }
        };

        // Poll every 2 seconds for up to 5 minutes
        let attempts = 0;
        const maxAttempts = 150; // 5 minutes * 30 attempts per minute
        const interval = setInterval(async () => {
            if (attempts >= maxAttempts) {
                clearInterval(interval);
                toast.error('CSV generation timed out');
                return;
            }
            
            const success = await checkStatus(response.data.id);
            if (success) {
                clearInterval(interval);
            }
            attempts++;
        }, 2000);
    } catch (error) {
        console.error(error);
        toast.error('Error exporting CSV');
    }
};
</script>

<template>
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center px-4 gap-3 mt-4">
            <h4>Service Requests</h4>
            <form class="d-flex align-items-center" role="search" @submit.prevent>
                <input
                    class="form-control me-2 form-control-sm"
                    type="search"
                    placeholder="Search by customer, professional, service, date, address, contact or status"
                    aria-label="Search"
                    v-model="searchQuery"
                    @input="filterRequests"
                />
                <i class="pi pi-search"></i>
            </form>
            <button class="btn btn-sm btn-primary" @click="exportCSV">Export CSV</button>
        </div>

        <div v-if="serviceRequests.length === 0" class="text-center mt-4">
            <p>No service requests found</p>
        </div>

        <table v-else class="table table-sm table-hover">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Customer</th>
                    <th>Service</th>
                    <th>Professional</th>
                    <th>Status</th>
                    <th>Requested On</th>
                    <th>Completed On</th>
                    <th>Address</th>
                    <th>Customer Contact</th>
                    <th>Remarks</th>
                </tr>
            </thead>
            <tbody class="table-group-divider">
                <tr v-for="(request, index) in formattedRequests" :key="request.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ request.customer.name }}</td>
                    <td>{{ request.service.name }}</td>
                    <td>{{ request.professional ? request.professional.name : '-' }}</td>
                    <td>
                        <span :class="{
                            'badge': true,
                            'bg-warning': request.status === 'requested',
                            'bg-danger': request.status === 'rejected',
                            'bg-success': request.status === 'completed' || request.status === 'closed' || request.status === 'accepted'
                        }">
                            {{ request.status.charAt(0).toUpperCase() + request.status.slice(1) }}
                        </span>
                    </td>
                    <td>{{ request.date_of_request }}</td>
                    <td>{{ request.date_of_completion || '-' }}</td>
                    <td>{{ request.address }}</td>
                    <td>{{ request.customer_contact_number }}</td>
                    <td>{{ request.remarks || '-' }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
