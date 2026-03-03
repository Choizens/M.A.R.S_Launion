// Initializing Vue Router - Triggering fresh Vercel deployment
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'requestor-home',
      component: () => import('../views/requestor/requestor_home.vue'),
    },
    // ── Staff routes ──────────────────────────────────────
    {
      path: '/Staff/home',
      name: 'staff-home',
      component: () => import('../views/Staff/Staff_Home.vue'),
    },
    {
      path: '/Staff/login',
      name: 'login',
      component: () => import('../views/auth/login.vue'),
    },
    {
      path: '/Staff/register',
      name: 'register',
      component: () => import('../views/auth/register.vue'),
    },
    {
      path: '/Staff/dashboard/:tab?',
      name: 'staff-dashboard',
      component: () => import('../views/Staff/StaffDashboard.vue'),
      meta: { requiresAuth: true },
    },
    // ── Admin routes (using lowercase 'admin' for Linux compatibility) ────
    {
      path: '/admin/login',
      name: 'admin-login',
      component: () => import('../views/admin/AdminLogin.vue'),
    },
    {
      path: '/admin/dashboard/:tab?',
      name: 'admin-dashboard',
      component: () => import('../views/admin/AdminDashboard.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    // Catch-all
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
    {
      path: '/requestor/request-details/:code',
      name: 'request-details',
      component: () => import('../views/requestor/request_details.vue'),
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const isAuthenticated = !!token;
  const isAdmin = localStorage.getItem('is_admin') === 'true';

  // Redirect unauthenticated users away from protected pages
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next(to.meta.requiresAdmin ? '/admin/login' : '/Staff/login');
  }

  // Redirect non-admins away from admin dashboard
  if (to.meta.requiresAdmin && !isAdmin) {
    return next('/admin/login');
  }

  // Redirect already-authenticated admin away from admin login
  if (to.name === 'admin-login' && isAuthenticated && isAdmin) {
    return next('/admin/dashboard');
  }

  // Redirect already-authenticated staff away from staff login/register
  if ((to.name === 'login' || to.name === 'register') && isAuthenticated && !isAdmin) {
    return next('/Staff/dashboard');
  }

  next();
});

export default router
