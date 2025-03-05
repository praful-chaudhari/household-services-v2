import { createApp } from "vue";
import { createPinia } from "pinia";
import Toast from "vue-toastification";

import "vue-toastification/dist/index.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "primeicons/primeicons.css";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(Toast);

app.mount("#app");
