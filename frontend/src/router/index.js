import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardLayout from '@/views/DashboardLayout.vue'
import DashboardView from '../views/DashboardView.vue'
import PersonCreateView from '../views/PersonCreateView.vue'
import RelativeBlock from '../views/RelativeBlock.vue'
import ScanViewer from '@/views/ScanViewer.vue'
//import BirthInfoView from '@/views/BirthInfoView.vue'
//import DeathInfoView from '@/views/DeathInfoView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: HomeView
    },
    { path: '/', 
      name: 'login', 
      component: LoginView 
    },
    { path: '/register', 
      name: 'register', 
      component: RegisterView
    },
    {
      path: '/dash/layout',
      name: '/dashlayout',
      component: DashboardLayout
    },
    {
      path: '/relative',
      name: '/relative',
      component: RelativeBlock
    },
    {
      path: '/dash',
      name: 'dash',
      component: DashboardView,
    },
    {
      path: '/person/create',
      name: 'personcreate',
      component: PersonCreateView,
    },
    {
      path: '/scan',
      name: 'scan',
      component: ScanViewer,
    },
/*     {
      path: '/birth',
      component: BirthInfoView,
    },
    {
      path: '/death',
      component: DeathInfoView,
    },*/
    ]
})

export default router
