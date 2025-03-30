export function formatDate(datetimeStr) {
    // Parse the datetime string into a JavaScript Date object
    const date = new Date(datetimeStr);

    // Extract day, month, and year
    const day = date.getUTCDate(); // Day of the month
    const month = date.toLocaleString("default", { month: "long" }); // Full month name
    const year = date.getUTCFullYear(); // Year

    // Return the formatted date string
    return `${day} ${month}, ${year}`;
}
