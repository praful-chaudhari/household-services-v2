<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from '@/utils/axios.js';
import { useToast } from 'vue-toastification';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Pie, Bar } from 'vue-chartjs';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const toast = useToast();

const services = ref([]);
const customers = ref([]);
const professionals = ref([]);
const serviceRequests = ref([]);
const reviews = ref([]);

const fetchData = async () => {
    try {
        const [servicesRes, customersRes, professionalsRes, requestsRes, reviewsRes] = await Promise.all([
            axios.get('/services'),
            axios.get('/customers'),
            axios.get('/professionals'),
            axios.get('/service-requests'),
            axios.get('/reviews')
        ]);

        services.value = servicesRes.data;
        customers.value = customersRes.data;
        professionals.value = professionalsRes.data;
        serviceRequests.value = requestsRes.data;
        reviews.value = reviewsRes.data;
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

// Services and their professional counts
const serviceDistributionData = computed(() => ({
    labels: services.value.map(s => s.name),
    datasets: [{
        label: 'Number of Professionals',
        data: services.value.map(service => 
            professionals.value.filter(p => p.service.id === service.id).length
        ),
        backgroundColor: '#4CAF50'
    }]
}));

// Average ratings per service
const serviceRatingsData = computed(() => ({
    labels: services.value.map(s => s.name),
    datasets: [{
        label: 'Average Rating',
        data: services.value.map(service => {
            // Get all professionals for this service
            const serviceProfessionals = professionals.value.filter(p => p.service.id === service.id);
            
            // Get all reviews for professionals of this service
            let allServiceReviews = [];
            serviceProfessionals.forEach(professional => {
                const profReviews = reviews.value.filter(r => r.professional_id === professional.id);
                allServiceReviews = [...allServiceReviews, ...profReviews];
            });

            if (allServiceReviews.length === 0) return 0;
            
            const avgRating = allServiceReviews.reduce((acc, curr) => acc + parseInt(curr.rating), 0) / allServiceReviews.length;
            return parseFloat(avgRating.toFixed(1));
        }),
        backgroundColor: '#FF8C00'
    }]
}));

const barChartOptions = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top'
        },
        title: {
            display: true,
            text: 'Professionals per Service'
        }
    }
};

const ratingChartOptions = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top'
        },
        title: {
            display: true,
            text: 'Average Service Ratings'
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            max: 5
        }
    }
};

onMounted(() => {
    fetchData();
});
</script>

<template>
    <div class="container mt-4 mb-5 container-fluid">
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Quick Stats</h5>
                        <div class="row mt-3">
                            <div class="col-6 mb-3">
                                <div class="p-3 bg-primary bg-opacity-10 rounded">
                                    <h6>Total Services</h6>
                                    <h3>{{ services.length }}</h3>
                                </div>
                            </div>
                            <div class="col-6 mb-3">
                                <div class="p-3 bg-success bg-opacity-10 rounded">
                                    <h6>Total Customers</h6>
                                    <h3>{{ customers.length }}</h3>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="p-3 bg-warning bg-opacity-10 rounded">
                                    <h6>Total Professionals</h6>
                                    <h3>{{ professionals.length }}</h3>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="p-3 bg-info bg-opacity-10 rounded">
                                    <h6>Total Requests</h6>
                                    <h3>{{ serviceRequests.length }}</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Service Request Status Distribution</h5>
                        <Pie 
                            v-if="serviceRequests.length"
                            :data="requestStatusData"
                            :options="{ responsive: true }"
                        />
                        <div v-else class="text-center mt-3">
                            <p>No service requests available yet</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Professionals per Service</h5>
                        <Bar
                            v-if="services.length"
                            :data="serviceDistributionData"
                            :options="barChartOptions"
                        />
                        <div v-else class="text-center mt-3">
                            <p>No services available yet</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Service Ratings</h5>
                        <Bar
                            v-if="services.length && reviews.length"
                            :data="serviceRatingsData"
                            :options="ratingChartOptions"
                        />
                        <div v-else class="text-center mt-3">
                            <p>No ratings available yet</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
