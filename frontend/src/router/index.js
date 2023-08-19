import { createRouter, createWebHistory } from 'vue-router'

// import LoginPage from '../views/LoginPage.vue'
import Dashboard from '../components/Dashboard.vue'
import Excel from '../components/Excel.vue'
import ErrorPage404 from '../components/ErrorPage404.vue'

const routes = [
  // {
  //   path: '/login',
  //   name: 'Login',
  //   component: LoginPage,
  //   meta: { requiredAuthorization: false }
  // },
  {
    path: '/',
    name: 'Dashboard1',
    component: Dashboard,
    meta: { requiredAuthorization: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiredAuthorization: false }
  },
  {
    path: '/excel',
    name: 'Excel',
    component: Excel,
    meta: { requiredAuthorization: false }
  },
  {
    path: '/:catchAll(.*)',
    name: 'ErrorPage404',
    component: ErrorPage404,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => { 
  next()
})


export default router