<template>
  <div id="top" class="min-h-screen font-sans">
    <!-- Navbar -->
    <nav class="flex flex-col md:flex-row justify-between items-center py-4 px-6 md:px-12 bg-white border-b shadow-sm gap-4 md:gap-0">
      <div class="flex items-center gap-2.5">
        <img :src="logoImg" alt="Logo" class="w-12 h-12 object-contain" />
        <div class="flex flex-col">
          <span class="font-caveat font-bold text-black text-xl md:text-2xl leading-none tracking-tight">StandAlone</span>
          <span class="font-caveat text-base md:text-lg text-black leading-none mt-0.5">La Union Senior High School</span>
        </div>
      </div>
      <div class="flex flex-wrap justify-center items-center gap-4 md:gap-8 lg:gap-12 text-[0.8rem] md:text-[0.95rem]">
        <router-link to="/Staff/home" class="text-cyan-500 font-bold transition-colors">Home</router-link>
        <a href="#our-commitment" @click.prevent="scrollToSection('our-commitment')" class="text-slate-800 font-bold hover:text-cyan-500 transition-colors">Our Commitment</a>
        <a href="#staff-workflow" @click.prevent="scrollToSection('staff-workflow')" class="text-slate-800 font-bold hover:text-cyan-500 transition-colors">Workflow</a>
        <a href="#staff-faq" @click.prevent="scrollToSection('staff-faq')" class="text-slate-800 font-bold hover:text-cyan-500 transition-colors">Staff FAQ</a>
        <router-link to="/Staff/login" class="px-6 py-2 bg-[#154252] text-white font-bold rounded-lg hover:bg-[#0d2a35] transition-all shadow-md">Login Portal</router-link>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="relative min-h-[450px] md:min-h-[500px] flex flex-col justify-center bg-cover bg-center px-6 md:px-12 lg:px-24 py-16 md:py-0 text-center md:text-left"
         :style="{ backgroundImage: `url(${bgImg})` }">

      <div class="max-w-4xl relative z-10 mx-auto md:mx-0">
        <p class="text-slate-300 md:text-slate-200 font-bold mb-2 text-xs md:text-base">M.A.R.S Staff Portal - Management & Archiving System</p>
        <h1 class="text-white text-2xl sm:text-3xl md:text-4xl font-extrabold mb-4 leading-tight">
          Streamlining Document Requests for <span class="text-yellow-400">Better Service!</span>
        </h1>
        <p class="text-slate-300 md:text-slate-200 max-w-2xl mb-10 leading-relaxed text-sm md:text-base mx-auto md:mx-0">
          Dedicated portal for the registrar and staff of La Union Senior High School. Manage application requests, 
          verify records, and ensure efficient document processing for our students and alumni.
        </p>

        <!-- CTA Button -->
        <div class="relative inline-block mt-4 group w-full sm:w-auto">
          <router-link to="/Staff/login" class="inline-block px-12 py-3 md:py-4 bg-yellow-400 hover:bg-yellow-500 text-slate-900 font-black rounded-sm shadow-xl transition-all transform hover:scale-105 uppercase tracking-wide text-sm md:text-base min-w-full sm:min-w-[280px] text-center">
            Access Dashboard
          </router-link>
        </div>
      </div>

      </div>

    <!-- Stats/Quick Info Section -->
    <div class="bg-[#f8fafc] border-b">
      <div class="max-w-7xl mx-auto px-6 md:px-12 py-6 md:py-10">
        <div class="bg-white p-6 md:p-8 rounded-2xl shadow-xl -mt-10 md:-mt-20 relative z-20 border border-slate-100">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-slate-100">
            <div class="py-4 md:py-0">
              <h3 class="text-2xl md:text-3xl font-black text-[#154252] mb-1">Efficient</h3>
              <p class="text-[0.6rem] md:text-xs font-bold text-slate-500 uppercase tracking-widest">Optimized Workflow</p>
            </div>
            <div class="py-4 md:py-0 md:pl-4">
              <h3 class="text-2xl md:text-3xl font-black text-[#154252] mb-1">Secure</h3>
              <p class="text-[0.6rem] md:text-xs font-bold text-slate-500 uppercase tracking-widest">Data Management</p>
            </div>
            <div class="py-4 md:py-0 md:pl-4">
              <h3 class="text-2xl md:text-3xl font-black text-[#154252] mb-1">Reliable</h3>
              <p class="text-[0.6rem] md:text-xs font-bold text-slate-500 uppercase tracking-widest">Portal Access</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content Sections -->
    <div id="our-commitment" class="max-w-7xl mx-auto py-12 md:py-20 px-6 md:px-12 grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-20">
      <div class="flex flex-col gap-12">
        <section>
          <h2 class="text-3xl font-black text-[#154252] mb-6 border-b-4 border-slate-100 pb-2 uppercase">Our Commitment</h2>
          <p class="text-slate-700 leading-relaxed font-medium">
            At La Union Senior High School, our staff is committed to providing the highest quality of service to our students. 
            The M.A.R.S portal is designed to empower our registrar and administrative team with the tools needed for fast, 
            accurate, and seamless document processing.
          </p>
        </section>

        <section>
          <h2 class="text-3xl font-black text-[#154252] mb-6 border-b-4 border-slate-100 pb-2 uppercase">Integrity in Service</h2>
          <p class="text-slate-700 leading-relaxed font-medium">
            Every document request is handled with strict confidentiality and professionalism. We understand the importance of 
            these records for our students' future endeavors, and we strive to exceed expectations in terms of turnaround time 
            and data accuracy.
          </p>
        </section>
      </div>

      <div id="staff-workflow">
        <h2 class="text-3xl font-black text-[#154252] mb-6 border-b-4 border-slate-100 pb-2 uppercase">STAFF WORKFLOW</h2>
        <div class="space-y-6">
          <div class="flex items-start gap-4">
             <div class="w-10 h-10 rounded-full bg-[#154252] text-white flex items-center justify-center font-bold shrink-0 text-xl shadow-lg border-2 border-yellow-400">1</div>
             <div>
               <h3 class="text-lg font-bold text-slate-800">Review Applications</h3>
               <p class="text-sm text-slate-600 font-medium">Monitor and review incoming document requests from the dashboard.</p>
             </div>
          </div>
          <div class="flex items-start gap-4">
             <div class="w-10 h-10 rounded-full bg-[#154252] text-white flex items-center justify-center font-bold shrink-0 text-xl shadow-lg border-2 border-yellow-400">2</div>
             <div>
               <h3 class="text-lg font-bold text-slate-800">Verify Records</h3>
               <p class="text-sm text-slate-600 font-medium">Coordinate with the archive to verify student eligibility and record existence.</p>
             </div>
          </div>
          <div class="flex items-start gap-4">
             <div class="w-10 h-10 rounded-full bg-[#154252] text-white flex items-center justify-center font-bold shrink-0 text-xl shadow-lg border-2 border-yellow-400">3</div>
             <div>
               <h3 class="text-lg font-bold text-slate-800">Process Documents</h3>
               <p class="text-sm text-slate-600 font-medium">Update request status and upload digital copies for student download.</p>
             </div>
          </div>
          <div class="flex items-start gap-4">
             <div class="w-10 h-10 rounded-full bg-[#154252] text-white flex items-center justify-center font-bold shrink-0 text-xl shadow-lg border-2 border-yellow-400">4</div>
             <div>
               <h3 class="text-lg font-bold text-slate-800">Final Release</h3>
               <p class="text-sm text-slate-600 font-medium">Management of physical pickups and final release confirmation.</p>
             </div>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ Section for Staff -->
    <div id="staff-faq" class="bg-slate-50 border-t border-slate-200">
      <div class="max-w-7xl mx-auto py-16 md:py-20 px-6 md:px-12">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-black text-[#154252] uppercase tracking-tight">Staff Manual & FAQ</h2>
          <p class="text-slate-500 mt-2 font-medium">Essential guidelines for staff document processing.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          <!-- FAQ Item -->
          <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <h3 class="font-bold text-lg text-slate-800 mb-2 flex items-center gap-2">
              <span class="text-yellow-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </span>
              Processing Timeline?
            </h3>
            <p class="text-sm text-slate-600 leading-relaxed font-medium">Standard processing is within 3-5 working days. Urgent requests should be prioritized through the dashboard flags.</p>
          </div>
          <!-- FAQ Item -->
          <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <h3 class="font-bold text-lg text-slate-800 mb-2 flex items-center gap-2">
              <span class="text-yellow-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
              </span>
              Security Protocol?
            </h3>
            <p class="text-sm text-slate-600 leading-relaxed font-medium">Never share your staff credentials. Ensure you log out of the dashboard when leaving your workstation.</p>
          </div>
          <!-- FAQ Item -->
          <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <h3 class="font-bold text-lg text-slate-800 mb-2 flex items-center gap-2">
              <span class="text-yellow-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>
              </span>
              Status Updates?
            </h3>
            <p class="text-sm text-slate-600 leading-relaxed font-medium">Update request statuses promptly to "Approved", "Processing", or "Ready" to keep students informed via their tracking passkey.</p>
          </div>
          <!-- FAQ Item -->
          <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <h3 class="font-bold text-lg text-slate-800 mb-2 flex items-center gap-2">
              <span class="text-yellow-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
              </span>
              Archive Coordination?
            </h3>
            <p class="text-sm text-slate-600 leading-relaxed font-medium">Use the internal messaging or directory to contact archive custodians if a student record is not appearing in the digital database.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-[#0D3971] text-slate-300 py-12 md:py-16 border-t-4 border-yellow-400">
      <div class="max-w-7xl mx-auto px-6 md:px-12 grid grid-cols-1 md:grid-cols-3 gap-10 md:gap-16">
        
        <!-- Brand Info -->
        <div class="flex flex-col gap-4">
          <div class="flex items-center gap-3 bg-white/10 p-4 rounded-xl w-fit backdrop-blur-sm border border-white/10">
            <img :src="logoImg" alt="Logo" class="w-12 h-12 object-contain" />
            <div class="flex flex-col -gap-1">
              <span class="font-caveat font-bold text-white text-2xl leading-none">StandAlone</span>
              <span class="font-caveat text-yellow-400 text-lg leading-none whitespace-nowrap mt-0.5">La Union Senior High School</span>
            </div>
          </div>
          <p class="text-[0.8rem] text-slate-400 leading-relaxed max-w-sm mt-2">
            M.A.R.S Staff Portal - Empowering our staff to provide efficient and transparent document services for the La Union SHS community.
          </p>
        </div>

        <!-- Quick Links -->
        <div class="flex flex-col gap-5">
          <h4 class="text-white font-black uppercase tracking-widest text-sm mb-1">Portal Links</h4>
          <div class="flex flex-col gap-3 text-sm">
            <router-link to="/Staff/home" class="hover:text-yellow-400 transition-colors w-fit flex items-center gap-2">
              <span class="w-1 h-1 rounded-full bg-yellow-400"></span> Home
            </router-link>
            <a href="#our-commitment" @click.prevent="scrollToSection('our-commitment')" class="hover:text-yellow-400 transition-colors w-fit flex items-center gap-2">
              <span class="w-1 h-1 rounded-full bg-yellow-400"></span> Our Commitment
            </a>
            <a href="#staff-workflow" @click.prevent="scrollToSection('staff-workflow')" class="hover:text-yellow-400 transition-colors w-fit flex items-center gap-2">
              <span class="w-1 h-1 rounded-full bg-yellow-400"></span> Workflow
            </a>
            <a href="#staff-faq" @click.prevent="scrollToSection('staff-faq')" class="hover:text-yellow-400 transition-colors w-fit flex items-center gap-2">
              <span class="w-1 h-1 rounded-full bg-yellow-400"></span> Staff FAQ
            </a>
            <router-link to="/Staff/login" class="hover:text-yellow-400 transition-colors w-fit flex items-center gap-2">
              <span class="w-1 h-1 rounded-full bg-yellow-400"></span> Login
            </router-link>
          </div>
        </div>

        <!-- Contact Info -->
        <div class="flex flex-col gap-4">
          <h4 class="text-white font-black uppercase tracking-widest text-sm mb-1">Internal Support</h4>
          <div class="flex items-start gap-3 mt-1 text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            <span class="text-slate-400">Registrar's Office<br/>La Union Senior High School</span>
          </div>
          <div class="flex items-center gap-3 text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
            <span class="text-slate-400">it.support@launion.edu.ph</span>
          </div>
        </div>

      </div>
      
      <!-- Copyright -->
      <div class="max-w-7xl mx-auto px-6 md:px-12 mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between text-xs text-slate-500 gap-4">
        <p>&copy; {{ new Date().getFullYear() }} StandAlone - La Union Senior High School. Staff Portal Area.</p>
        <div class="flex gap-6">
          <a href="#" class="hover:text-white transition-colors">Internal Policy</a>
          <a href="#" class="hover:text-white transition-colors">System Help</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import bgImg from '@/assets/Launion_backend.svg';
import logoImg from '@/assets/form_logo.png';

const scrollToSection = (id) => {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap');

.font-caveat {
  font-family: 'Caveat', cursive;
}
</style>
