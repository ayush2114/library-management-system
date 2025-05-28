import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('../views/SignupView.vue')
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboard.vue'),
    meta: {
      requiresLogin: true,
      role: 'admin'
    },
  },
  {
    path: '/admin/ebooks',
    name: 'AdminEbooks',
    component: () => import('../views/AdminEbooks.vue'),
    meta: {
      requiresLogin: true,
      role: 'admin'
    },
  },
  {
    path: '/admin/add-section',
    name: 'AddSection',
    component: () => import('@/views/AddSection.vue'),
    meta: {
      requiresLogin: true,
      role: 'admin'
    },
  },
  {
    path: '/admin/update-section/:section_id',
    name: 'UpdateSection',
    component: () => import('@/views/UpdateSection.vue'),
    meta: {
      requiresLogin: true,
      role: 'admin'
    },
  },
  {
    path: '/admin/add-ebook/:section_id',
    name: 'AddEbook',
    component: () => import('@/views/AddEbook.vue'),
    meta: {
      requiresLogin: true,
      role: 'admin'
    },
  },
  {
    path: '/admin/update-ebook/:ebook_id',
    name: 'UpdateEbook',
    component: () => import('@/views/UpdateEbook.vue'),
    meta: {
      requiresLogin: true,
      role: 'admin'
    },
  },
  {
    path: '/admin/stats',
    name: 'AdminStats',
    component: () => import('../views/AdminStats.vue'),
    meta: {
      requiresLogin: true,
      role: 'admin'
    },
  },
  {
    path: '/admin/users',
    name: 'AllUsers',
    component: () => import('../views/AllUsers.vue'),
    meta: {
      requiresLogin: true,
      role: 'admin'
    },
  },
  {
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: () => import('../views/UserDashboard.vue'),
    meta: {
      requiresLogin: true
    },
  },
  {
    path: '/user/ebooks',
    name: 'UserEbooks',
    component: () => import('../views/UserEbooks.vue'),
    meta: {
      requiresLogin: true
    },
  },
  {
    path: '/user/buy-ebook/:ebook_id',
    name: 'BuyEbook',
    component: () => import('../views/BuyEbook.vue'),
    meta: {
      requiresLogin: true
    },
  },
  {
    path: '/read-ebook/:ebook_id',
    name: 'ReadEbook',
    component: () => import('@/views/ReadEbook.vue'),
    meta: {
      requiresLogin: true
    }
  },
  {
    path: '/user/stats',
    name: 'UserStats',
    component: () => import('../views/UserStats.vue'),
    meta: {
      requiresLogin: true
    },
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresLogin)) {
    if (!store.getters.loggedIn) {
      next({ name: 'Login' })
    } else if ( to.meta.role && !store.getters.isAdmin ) {
      next({ name: 'Login' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
