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
      path: '/Staff/login',
      name: 'login',
      component: () => import('../views/auth/login.vue'),
    },

    {
      path: '/Staff/dashboard/:tab?',
      name: 'staff-dashboard',
      component: () => import('../views/staff/StaffDashboard.vue'),
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

router.beforeEach((to) => {
  const token = localStorage.getItem('token');
  const isAuthenticated = !!token;
  const isSuperuser = localStorage.getItem('is_superuser') === 'true';
  const isAdminOrStaff = localStorage.getItem('is_admin') === 'true';

  // Redirect unauthenticated users away from protected pages
  if (to.meta.requiresAuth && !isAuthenticated) {
    return to.meta.requiresAdmin ? '/admin/login' : '/Staff/login';
  }

  // Redirect non-superusers away from the specific Admin Dashboard
  if (to.meta.requiresAdmin && !isSuperuser) {
    return '/admin/login'; // or access-denied
  }

  // Redirect already-authenticated users AWAY from login pages
  if (to.name === 'admin-login' && isAuthenticated) {
    return isSuperuser ? '/admin/dashboard' : '/Staff/dashboard';
  }

  if (to.name === 'login' && isAuthenticated) {
    return isSuperuser ? '/admin/dashboard' : '/Staff/dashboard';
  }

  return true;
});

export default router
