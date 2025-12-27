import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import LoginForbiddenView from '../views/LoginForbiddenView.vue'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import ForgotPasswordView from '../views/ForgotPasswordView.vue'
import OnerilenlerView from '../views/OnerilenlerView.vue'
import FavorilerView from '../views/FavorilerView.vue'
import MoviesView from '../views/MoviesView.vue'
import SeriesView from '../views/SeriesView.vue'
import WatchlistView from '../views/WatchlistView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/login-forbidden',
    name: 'LoginForbidden',
    component: LoginForbiddenView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPasswordView
  },
  {
    path: '/onerilenler',
    name: 'Onerilenler',
    component: OnerilenlerView,
    meta: { requiresAuth: true }
  },
  {
    path: '/favoriler',
    name: 'Favoriler',
    component: FavorilerView,
    meta: { requiresAuth: true }
  },
  {
    path: '/filmler',
    name: 'Movies',
    component: MoviesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/diziler',
    name: 'Series',
    component: SeriesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/izlenecekler',
    name: 'Watchlist',
    component: WatchlistView,
    meta: { requiresAuth: true }
  },
  {
  path: '/listelerim/:id',
  name: 'CustomListDetail',
  component: () => import('../views/CustomListDetailView.vue'),
  props: true
},
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('authToken') || localStorage.getItem('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router

