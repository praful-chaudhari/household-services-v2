import axios from '@/utils/axios';

export const fetchServiceRequests = async (retryCount = 0) => {
    try {
        const response = await axios.get(`/service-requests`);
        return response.data;
    } catch (error) {
        if (retryCount < 5) {
            retryCount++;
            const backOffTime = Math.pow(2, retryCount) * 1000;
            await new Promise((resolve) => setTimeout(resolve, backOffTime));
            return fetchServiceRequests(retryCount, userId);
        } else {
            console.error('Error fetching service requests:', error);
            return [];
        }
    }
};
