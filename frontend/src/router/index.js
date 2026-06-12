import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardLayout from '@/views/DashboardLayout.vue'
import DashboardView from '../views/DashboardView.vue'
import PersonCreateView from '../views/PersonCreateView.vue'
import RelativeBlock from '../views/RelativeBlock.vue'
import ScanViewer from '@/views/ScanViewer.vue'
import Birth from '@/views/Birth.vue'
import AllPersons from '@/views/AllPersons.vue'
import Death from '@/views/Death.vue' 
import EditRecord from '@/views/EditRecord.vue'
import InfoPerson from '../views/InfoPerson.vue'
import Marriage from '../views/Marriage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/allpersons',
      name: 'allpersons',
      component: AllPersons,
      meta: { requiresAuth: true },
    },
    {
      path: '/birth',
      name: 'birth',
      component: Birth,
      meta: { requiresAuth: true }
    },
    {
      path: '/marriage',
      name: 'marriage',
      component: Marriage,
      meta: { requiresAuth: true }
    },
    {
      path: '/death',
      name: 'death',
      component: Death,
      meta: { requiresAuth: true }
    },
    {
      path: '/change-password',
      name: 'ChangePassword',
      component: () => import('@/views/ChangePassword.vue')
    },
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/person/view/:id/:type',
      name: 'InfoPerson',
      component: () => import('../views/InfoPerson.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/edit/:type/:id',
      name: 'EditRecord',
      component: EditRecord,
      meta: { requiresAuth: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/dash/layout',
      name: 'dashlayout',
      component: DashboardLayout,
      meta: { requiresAuth: true }
    },
    {
      path: '/relative',
      name: 'relative',
      component: RelativeBlock,
      meta: { requiresAuth: true }
    },
    {
      path: '/dash',
      name: 'dash',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/person/create',
      name: 'personcreate',
      component: PersonCreateView,
      meta: { requiresAuth: true }
    },
    {
      path: '/scan',
      name: 'scan',
      component: ScanViewer,
      meta: { requiresAuth: true }
    },
    {
      path: '/person/view/:recordId/:recordType',
      name: 'personInfo',
      component: () => import('@/views/InfoPerson.vue'),
      meta: { requiresAuth: true }
    }
  ],
})

// Исправленный navigation guard - без next()
router.beforeEach((to, from) => {
  const token = localStorage.getItem('access_token')
  
  // Если маршрут требует авторизации и нет токена
  if (to.meta.requiresAuth && !token) {
    return '/'
  }
  
  // Если пользователь авторизован и пытается перейти на страницу логина
  if (to.path === '/' && token) {
    return '/home'
  }
  
  // Разрешаем переход
  return true
})

export default router