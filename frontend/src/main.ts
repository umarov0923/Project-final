import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

// Инициализация приложения
const app = createApp(App);
const pinia = createPinia();

// Подключение плагинов
app.use(pinia);
app.use(router);
app.use(Toast, {
    transition: 'Vue-Toastification__bounce',
    maxToasts: 5,
    newestOnTop: true
  })

// Монтирование приложения
app.mount('#app');