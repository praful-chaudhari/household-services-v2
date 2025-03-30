import axios from "@/utils/axios.js";

export async function fetchServices(retryCount = 0) {
    try {
        const response = await axios.get("/services");
        return response.data;
    } catch (error) {
        if (retryCount < 5) {
            retryCount++;
            const backOffTime = Math.pow(2, retryCount) * 1000;
            await new Promise((resolve) => setTimeout(resolve, backOffTime));
            return fetchServices(retryCount);
        } else {
            console.error("Error fetching services.");
            return [];
        }
    }
}
