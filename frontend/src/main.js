import { createApp } from 'vue'
import './index.css'
import App from './App.vue'
import store from './store'
import router from './router';
import { Toaster, toast } from 'vue-sonner';
import 'vue-sonner/style.css'
import { TOAST_MESSAGES } from './config/ToastMessages'; 

const app = createApp(App)
app.component('Toaster', Toaster);
app.config.globalProperties.$toast = toast;
app.config.globalProperties.$toastMsg = TOAST_MESSAGES;
app.use(store).use(router).mount('#app');
