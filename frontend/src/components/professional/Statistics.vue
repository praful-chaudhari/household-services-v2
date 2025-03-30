<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from '@/utils/axios.js';
import { useToast } from 'vue-toastification';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Pie, Bar } from 'vue-chartjs';
import { userStore } from '@/stores/userStore.js';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const toast = useToast();
const store = userStore();

const serviceRequests = ref([]);
const reviews = ref([]);

const fetchData = async () => {
    try {
        const [requestsRes, reviewsRes] = await Promise.all([
            axios.get('/service-requests'),
            axios.get(`/reviews/${store.user.id}`)
        ]);

        serviceRequests.value = requestsRes.data
        reviews.value = reviewsRes.data
    } catch (error) {
        console.error(error);
        toast.error('Error fetching statistics data');
    }
};

// Service request status distribution data
const requestStatusData = computed(() => ({
    labels: ['Requested', 'Accepted', 'Completed', 'Rejected', 'Closed'],
    datasets: [{
        data: [
            serviceRequests.value.filter(r => r.status === 'requested').length,
            serviceRequests.value.filter(r => r.status === 'accepted').length,
            serviceRequests.value.filter(r => r.status === 'completed').length,
            serviceRequests.value.filter(r => r.status === 'rejected').length,
            serviceRequests.value.filter(r => r.status === 'closed').length
        ],
        backgroundColor: ['#ffd700', '#90EE90', '#32CD32', '#ff6b6b', '#4169E1']
    }]
}));

// Rating distribution data
const ratingDistributionData = computed(() => ({
    labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
    datasets: [{
        label: 'Number of Reviews',
        data: [
            reviews.value.filter(r => parseInt(r.rating) === 1).length,
            reviews.value.filter(r => parseInt(r.rating) === 2).length,
            reviews.value.filter(r => parseInt(r.rating) === 3).length,
            reviews.value.filter(r => parseInt(r.rating) === 4).length,
            reviews.value.filter(r => parseInt(r.rating) === 5).length
        ],
        backgroundColor: '#FF8C00'
    }]
}));

const barChartOptions = {
    responsive: true,
    scales: {
        y: {
            beginAtZero: true
        }
    }
};

onMounted(() => {
    fetchData();
});
</script>

<template>
    <div class="container mt-4 mb-5">
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Quick Stats</h5>
                        <div class="row mt-3">
                            <div class="col-6 mb-3">
                                <div class="p-3 bg-primary bg-opacity-10 rounded">
                                    <h6>Total Requests</h6>
                                    <h3>{{ serviceRequests.length }}</h3>
                                </div>
                            </div>
                            <div class="col-6 mb-3">
                                <div class="p-3 bg-success bg-opacity-10 rounded">
                                    <h6>Completed Requests</h6>
                                    <h3>{{ serviceRequests.filter(r => r.status === 'completed' || r.status === 'closed').length }}</h3>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="p-3 bg-warning bg-opacity-10 rounded">
                                    <h6>Reviews Received</h6>
                                    <h3>{{ reviews.length }}</h3>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="p-3 bg-info bg-opacity-10 rounded">
                                    <h6>Avg Rating</h6>
                                    <h3>{{ reviews.length ? (reviews.reduce((acc, curr) => acc + parseInt(curr.rating), 0) / reviews.length).toFixed(1) : 0 }}</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Request Status Distribution</h5>
                        <Pie 
                            v-if="serviceRequests.length"
                            :data="requestStatusData"
                            :options="{ responsive: true }"
                        />
                        <div v-else class="text-center mt-3">
                            <p>No service requests yet</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-12 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Your Rating Distribution</h5>
                        <Bar
                            v-if="reviews.length"
                            :data="ratingDistributionData"
                            :options="barChartOptions"
                        />
                        <div v-else class="text-center mt-3">
                            <p>No reviews received yet</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
