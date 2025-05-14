import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; // Импортируйте ваш Pinia store для аутентификации
import LoginView from '@/views/LoginView.vue';
import ClientsView from '@/views/Clients/ListView.vue';
import HomeView from '@/views/HomeView.vue';
import  RegisterView  from "@/views/RegisterView.vue";



const routes = [
  { path : '/', component: HomeView },
  { path : '/register', component: RegisterView },
  { path: '/login', component: LoginView },
  { path: '/clients', component: ClientsView, meta: { requiresAuth: true } },
  {
    path: '/clients/:id/debt',
    name: 'ClientDebt',
    component: () => import('@/views/Clients/ClientDebtPage.vue') // или твой компонент
  },
  { path: '/debts',
    name: 'Debts',
    component: () => import('@/views/debts/DebtsView.vue'),
  },
  {
    path: '/debts/:id/payments',
    name: 'DebtPayments',
    component: () => import('@/views/debts/DebtPayments.vue')
  },

  {
      path: '/payments',
      name: 'Payments',
      component: () => import('@/views/Payments/PaymentsView.vue'),
    }
  // Добавьте другие маршруты для Debts и Payments
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, _, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.accessToken) {
    next('/login');
  } else {
    next();
  }
});

export default router;