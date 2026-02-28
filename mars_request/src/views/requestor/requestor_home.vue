<template>
  <div class="min-h-screen font-sans">
    <!-- Navbar -->
    <nav class="flex flex-col md:flex-row justify-between items-center py-4 px-6 md:px-12 bg-white border-b shadow-sm gap-4 md:gap-0">
      <div class="flex items-center gap-2.5">
        <img :src="logoImg" alt="Logo" class="w-10 h-10 object-contain" />
        <div class="flex flex-col">
          <span class="font-bold text-slate-800 text-sm leading-tight">StandAlone</span>
          <span class="text-[0.65rem] text-slate-500 font-medium whitespace-nowrap">La Union Senior High School</span>
        </div>
      </div>
      <div class="flex flex-wrap justify-center items-center gap-4 md:gap-12 text-[0.8rem] md:text-[0.95rem]">
        <router-link to="/" class="text-cyan-500 font-bold">Home</router-link>
        <a href="#" class="text-slate-800 font-bold hover:text-cyan-500 transition-colors">Navigation</a>
        <a href="#" class="text-slate-800 font-bold hover:text-cyan-500 transition-colors">Navigation</a>
        <a href="#" class="text-slate-800 font-bold hover:text-cyan-500 transition-colors">Navigation</a>
        <router-link to="/Staff/login" class="px-4 md:px-6 py-2 rounded font-bold text-white bg-[#154252] hover:bg-[#0d2a35] transition-colors whitespace-nowrap">
          Staff Login
        </router-link>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="relative min-h-[450px] md:min-h-[500px] flex flex-col justify-center bg-[#154252] bg-cover bg-center bg-blend-overlay px-6 md:px-12 lg:px-24 py-16 md:py-0 text-center md:text-left"
         :style="{ backgroundImage: `linear-gradient(rgba(21, 66, 82, 0.7), rgba(21, 66, 82, 0.7)), url(${bgImg})` }">

      <div class="max-w-4xl relative z-10 mx-auto md:mx-0">
        <p class="text-slate-300 md:text-slate-200 font-bold mb-2 text-sm md:text-base">La Union Senior High School, Cabadbaran City</p>
        <h1 class="text-white text-3xl sm:text-4xl md:text-5xl lg:text-5xl font-extrabold mb-6 leading-tight">
          Request your School Document <span class="text-yellow-400">Online!</span>
        </h1>
        <p class="text-slate-300 md:text-slate-200 max-w-2xl mb-10 leading-relaxed text-sm md:text-base mx-auto md:mx-0">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
          Ut enim ad minim veniam, quis nostrud exercitation ullamco
        </p>

        <!-- CTA Button with character -->
        <div class="relative inline-block mt-12 group">
          <div class="absolute -top-12 -right-24 flex items-center gap-2 pointer-events-none z-20">
            <!-- Character sitting -->
            <div class="relative w-12 h-12">
               <img :src="sittingPersonImg" alt="Sitting" class="absolute bottom-0 right-0 w-14 h-14 object-contain" />
            </div>
            <!-- The "HERE!" Bubble -->
            <div class="animate-bounce -mt-4">
               <div class="bg-white px-3 py-1.5 rounded-md text-[0.8rem] md:text-[0.9rem] font-black text-[#154252] shadow-xl border-2 border-[#154252] relative whitespace-nowrap">
                 HERE!
                 <!-- Left pointing tail -->
                 <div class="absolute top-1/2 -left-1.5 w-2.5 h-2.5 bg-white border-l-2 border-b-2 border-[#154252] transform -translate-y-1/2 rotate-45"></div>
               </div>
            </div>
          </div>
          
          <button @click="openModal" class="px-12 py-4 bg-yellow-400 hover:bg-yellow-500 text-slate-900 font-black rounded-sm shadow-xl transition-all transform hover:scale-105 uppercase tracking-wide text-base min-w-[280px]">
            Make a request
          </button>
        </div>
      </div>

      <!-- Decorative circles -->
      <div class="absolute right-12 lg:right-32 top-1/2 -translate-y-1/2 hidden xl:flex gap-8">
        <div class="w-40 h-40 rounded-full bg-white opacity-95"></div>
        <div class="w-40 h-40 rounded-full bg-white opacity-95"></div>
      </div>
    </div>

    <!-- Tracking Section -->
    <div class="bg-[#f8fafc] border-b">
      <div class="max-w-7xl mx-auto px-6 md:px-12 py-10">
        <div class="bg-white p-6 md:p-8 rounded-2xl shadow-xl -mt-20 relative z-20 border border-slate-100">
          <div class="flex flex-col md:flex-row items-center gap-6">
            <div class="flex-1">
              <h2 class="text-xl font-black text-[#154252] mb-1">Track Your Request</h2>
              <p class="text-xs font-bold text-slate-500 uppercase tracking-widest">Enter your details to check status & download files</p>
            </div>
            <div class="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
              <input v-model="trackId" type="text" placeholder="Passkey (e.g. 15)" class="w-full sm:w-40 border border-slate-300 rounded-lg px-4 py-3 text-sm focus:ring-2 focus:ring-[#154252] outline-none font-bold" />
              <input v-model="trackEmail" type="email" placeholder="Your Email Address" class="w-full sm:w-64 border border-slate-300 rounded-lg px-4 py-3 text-sm focus:ring-2 focus:ring-[#154252] outline-none font-bold" />
              <button @click="handleTrack" :disabled="tracking" class="w-full sm:w-auto px-8 py-3 bg-[#154252] text-white font-black rounded-lg hover:bg-[#0d2a35] transition-all disabled:opacity-50 shadow-lg shadow-[#154252]/20">
                {{ tracking ? 'Checking...' : 'Track Now' }}
              </button>
            </div>
          </div>
          <p v-if="trackError" class="text-red-500 text-[0.7rem] font-bold mt-3 text-center md:text-left">{{ trackError }}</p>
        </div>
      </div>
    </div>

    <!-- Content Sections -->
    <div class="max-w-7xl mx-auto py-12 md:py-20 px-6 md:px-12 grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-20">
      <div class="flex flex-col gap-12">
        <section>
          <h2 class="text-3xl font-black text-[#154252] mb-6 border-b-4 border-slate-100 pb-2">VISION</h2>
          <p class="text-slate-700 leading-relaxed font-medium">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
          </p>
        </section>

        <section>
          <h2 class="text-3xl font-black text-[#154252] mb-6 border-b-4 border-slate-100 pb-2">MISSION</h2>
          <p class="text-slate-700 leading-relaxed font-medium">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
          </p>
        </section>
      </div>

      <div>
        <h2 class="text-3xl font-black text-[#154252] mb-6 border-b-4 border-slate-100 pb-2">LOREM IPSUM</h2>
        <div class="space-y-8">
          <p class="text-slate-700 leading-relaxed font-medium">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            Ut enim ad minim veniam.
          </p>
          <p class="text-slate-700 leading-relaxed font-medium">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
          </p>
          <p class="text-slate-700 leading-relaxed font-medium">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
          </p>
        </div>
      </div>
    </div>

    <!-- ===================== REQUEST MODAL ===================== -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
        <div class="bg-white w-full max-w-4xl rounded-2xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[95vh]">
          
          <!-- Modal Header -->
          <div class="px-10 pt-10 pb-6 border-b border-slate-100 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-50/50 relative z-10 backdrop-blur-sm">
            <div>
              <h2 class="text-3xl font-black text-slate-900 tracking-tight">{{ currentStep === 1 ? 'Applicant Details' : 'Request Processing' }}</h2>
              <div class="mt-2 text-sm text-slate-600 font-medium">
                <span class="font-bold text-[#154252] uppercase tracking-wider text-xs">Step {{ currentStep }} of 2 &mdash;</span> Please complete the requested information.
              </div>
            </div>
            <!-- Step Indicator -->
            <div class="hidden sm:flex items-center gap-3">
              <div class="flex items-center justify-center w-10 h-10 rounded-full font-black shadow-sm transition-all duration-300"
                   :class="currentStep >= 1 ? 'bg-[#154252] text-white' : 'bg-slate-200 text-slate-400'">1</div>
              <div class="w-12 h-1 rounded-full transition-all duration-300"
                   :class="currentStep >= 2 ? 'bg-[#154252]' : 'bg-slate-200'"></div>
              <div class="flex items-center justify-center w-10 h-10 rounded-full font-black shadow-sm transition-all duration-300"
                   :class="currentStep >= 2 ? 'bg-amber-400 text-slate-900' : 'bg-slate-200 text-slate-400'">2</div>
            </div>
          </div>

          <!-- Modal Body -->
          <form id="submission-form" ref="requestForm" @submit.prevent="handleSubmit" class="p-6 lg:p-10 flex flex-col gap-10 flex-1 overflow-y-auto">
            
            <!-- STEP 1: Personal & School Information -->
            <div v-show="currentStep === 1" class="flex flex-col gap-8 animate-in fade-in slide-in-from-right-4 duration-500">

              <!-- Name Fields -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-slate-50 p-5 rounded-xl border border-slate-100">
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">First Name <span class="text-red-500">*</span></label>
                  <input v-model="form.first_name" type="text" required class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] shadow-sm font-medium" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">Last Name <span class="text-red-500">*</span></label>
                  <input v-model="form.last_name" type="text" required class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] shadow-sm font-medium" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">Middle Name</label>
                  <input v-model="form.middle_name" type="text" class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] shadow-sm font-medium" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">Suffix</label>
                  <input v-model="form.suffix" type="text" class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] shadow-sm font-medium" placeholder="Jr., Sr., III..." />
                </div>
              </div>

              <!-- School Fields -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-slate-50 p-5 rounded-xl border border-slate-100">
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">Sex <span class="text-red-500">*</span></label>
                  <select v-model="form.sex" required class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] bg-white shadow-sm font-medium">
                    <option value="" disabled>Select...</option>
                    <option>Male</option>
                    <option>Female</option>
                  </select>
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">Birthdate <span class="text-red-500">*</span></label>
                  <input v-model="form.birthdate" type="date" required class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] shadow-sm font-medium" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">Year Graduated <span class="text-red-500">*</span></label>
                  <input v-model="form.year_graduated" type="text" required class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] shadow-sm font-medium" placeholder="e.g. 2023" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">Strand <span class="text-red-500">*</span></label>
                  <select v-model="form.strand_type" required class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] bg-white shadow-sm font-medium">
                    <option value="" disabled>Select Strand</option>
                    <option v-for="s in strands" :key="s.id" :value="s.id">{{ s.name }}</option>
                  </select>
                </div>
              </div>

              <!-- Contact Fields -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-slate-50 p-5 rounded-xl border border-slate-100">
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">LRN Number <span class="text-[0.6rem] normal-case text-slate-400 font-normal">(Optional)</span></label>
                  <input v-model="form.lrn_number" type="text" class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] shadow-sm font-medium" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">Active Email <span class="text-red-500">*</span></label>
                  <input v-model="form.email" type="email" required class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] shadow-sm font-medium" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">Phone No. <span class="text-red-500">*</span></label>
                  <input v-model="form.phone_number" type="text" required class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] shadow-sm font-medium" />
                </div>
                <div class="flex flex-col gap-1 sm:col-span-2">
                  <label class="text-xs font-bold text-slate-600 uppercase tracking-wider">Permanent Address <span class="text-red-500">*</span></label>
                  <input v-model="form.permanent_address" type="text" required class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] shadow-sm font-medium" />
                </div>
              </div>
            </div>

            <!-- STEP 2: Verification, Documents, Schedule -->
            <div v-show="currentStep === 2" class="flex flex-col gap-8 animate-in fade-in slide-in-from-right-4 duration-500">
              
              <!-- Record Verification Info -->
              <div class="p-5 rounded-xl border-2 flex items-center justify-between" 
                  :class="recordStatus === 'found' ? 'bg-blue-50 border-blue-200' : 
                          recordStatus === 'duplicate' ? 'bg-amber-50 border-amber-200' :
                          recordStatus === 'not_found' ? 'bg-red-50 border-red-200' : 'bg-slate-50 border-slate-200'">
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 rounded-full flex items-center justify-center shadow-md border-2 border-white/50"
                        :class="recordStatus === 'found' ? 'bg-blue-500 text-white' : 
                                recordStatus === 'duplicate' ? 'bg-amber-500 text-white' :
                                recordStatus === 'not_found' ? 'bg-red-500 text-white' : 'bg-slate-400 text-white'">
                    <CheckIcon v-if="recordStatus === 'found'" class="w-6 h-6" />
                    <ClockIcon v-else-if="recordStatus === 'duplicate'" class="w-6 h-6" />
                    <AlertIcon v-else-if="recordStatus === 'not_found'" class="w-6 h-6" />
                    <SearchIcon v-else class="w-6 h-6" />
                  </div>
                  <div>
                    <h3 class="text-sm font-black uppercase tracking-tight"
                        :class="recordStatus === 'found' ? 'text-blue-900' : 
                                recordStatus === 'duplicate' ? 'text-amber-900' :
                                recordStatus === 'not_found' ? 'text-red-900' : 'text-slate-600'">
                      {{ recordStatus === 'found' ? 'Record Verified' : 
                          recordStatus === 'duplicate' ? 'Active Request Exists' :
                          recordStatus === 'not_found' ? 'No Digital Record' : 'Record Check' }}
                    </h3>
                    <p class="text-[0.65rem] font-medium leading-tight mt-1" 
                        :class="recordStatus === 'found' ? 'text-blue-700' : 
                                recordStatus === 'duplicate' ? 'text-amber-700' :
                                recordStatus === 'not_found' ? 'text-red-700' : 'text-slate-500'">
                      <template v-if="recordStatus === 'duplicate'">
                        {{ duplicateMessage }}
                      </template>
                      <template v-else>
                        {{ recordStatus === 'found' ? 'Master file found. You may proceed.' : recordStatus === 'not_found' ? 'Record missing. Proceed to school office for manual processing.' : 'Type Name/LRN to check system eligibility.' }}
                      </template>
                    </p>
                  </div>
                </div>
                <div v-if="checkingRecord" class="animate-spin rounded-full h-5 w-5 border-2 border-[#154252] border-t-transparent ml-2"></div>
              </div>

              <!-- File Selection -->
              <div class="flex flex-col gap-3 bg-white border border-slate-200 p-5 rounded-xl shadow-sm">
                <label class="text-xs font-bold text-[#154252] uppercase tracking-wider">Select Documents</label>
                <div class="relative">
                  <select v-model="fileSelectValue" @change="addFile" class="w-full border border-slate-300 rounded-lg px-4 py-3 text-sm text-slate-600 font-medium appearance-none bg-white focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] cursor-pointer shadow-sm">
                    <option value="" disabled>Choose a file from available records...</option>
                    <option v-for="d in filteredDocTypes" :key="d.id" :value="d.name">
                      {{ d.name }} — ₱{{ parseFloat(d.price).toLocaleString() }}
                    </option>
                  </select>
                  <div class="pointer-events-none absolute inset-y-0 right-4 flex items-center text-slate-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </div>

                <!-- Selected Files Display -->
                <div class="bg-slate-50 rounded-lg p-4 min-h-[80px] border border-slate-100 flex flex-col">
                  <div class="flex justify-between items-center mb-3">
                    <span class="text-[0.65rem] font-bold text-slate-500 uppercase tracking-widest">Requested Files:</span>
                    <button v-if="selectedFiles.length > 0" type="button" @click="removeAllFiles" class="text-[0.65rem] text-red-500 font-black hover:text-red-700 uppercase tracking-wider transition-colors">Clear All</button>
                  </div>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="(file, index) in selectedFiles"
                      :key="index"
                      class="flex items-center gap-2 bg-[#154252] text-[#99dbce] border border-[#0d2a35] shadow-sm text-xs font-bold px-3 py-1.5 rounded-full"
                    >
                      <FileTextIcon class="w-3 h-3" />
                      {{ file }}
                      <button type="button" @click="removeFile(index)" class="hover:text-yellow-400 transition-colors font-black text-sm leading-none ml-1 cursor-pointer">✕</button>
                    </span>
                    <span v-if="selectedFiles.length === 0" class="text-xs text-slate-400 italic font-medium my-auto text-center w-full">No documents selected.</span>
                  </div>
                </div>
                <div v-if="fileError" class="text-red-500 text-xs font-bold">{{ fileError }}</div>
              </div>

              <!-- Pickup Scheduling -->
              <div class="p-5 bg-amber-50 rounded-xl border border-amber-200 shadow-inner flex flex-col gap-5">
                <div class="flex flex-col gap-1">
                  <h3 class="text-sm font-black text-[#154252] uppercase tracking-tight flex items-center gap-2">
                    <CalendarIcon class="w-4 h-4 text-amber-500" />
                    Pickup Schedule
                  </h3>
                  <p class="text-[0.65rem] text-amber-800 font-medium">Select a date and timeframe to collect your processed documents from the school office.</p>
                </div>
                  
                <div class="flex flex-col gap-5">
                  <!-- Date Calendar Selection -->
                  <div class="flex flex-col gap-2">
                    <label class="text-[0.65rem] font-black text-[#154252] uppercase tracking-widest border-b border-amber-200 pb-1">Date</label>
                    <div v-if="loadingSlots" class="flex items-center gap-2 py-3">
                        <div class="animate-spin rounded-full h-4 w-4 border-2 border-amber-500 border-t-transparent"></div>
                        <span class="text-xs font-bold text-amber-700 italic">Searching available slots...</span>
                    </div>

                    <div v-else-if="slots.length > 0" class="flex overflow-x-auto gap-2 pb-2 custom-scrollbar">
                      <button 
                        v-for="slot in slots" 
                        :key="slot.id" 
                        type="button"
                        @click="handleDateSelect(slot)"
                        :disabled="slot.booked_morning >= slot.morning_slots && slot.booked_afternoon >= slot.afternoon_slots"
                        :class="[
                          'flex-shrink-0 w-20 p-2 rounded-xl border-2 transition-all flex flex-col items-center justify-center gap-1 group relative',
                          form.pickup_date === slot.date 
                            ? 'bg-[#154252] border-[#154252] text-white shadow-md' 
                            : (slot.booked_morning >= slot.morning_slots && slot.booked_afternoon >= slot.afternoon_slots)
                              ? 'bg-slate-100 border-slate-200 text-slate-400 cursor-not-allowed opacity-60'
                              : 'bg-white border-white text-slate-700 hover:border-amber-400 hover:shadow-sm'
                        ]"
                      >
                        <span class="text-[0.55rem] font-black uppercase tracking-widest opacity-80">
                          {{ new Date(slot.date).toLocaleDateString('en-PH', { month: 'short' }) }}
                        </span>
                        <span class="text-xl font-black leading-none my-0.5">
                          {{ new Date(slot.date).getDate() }}
                        </span>
                        <span class="text-[0.5rem] font-bold uppercase tracking-tighter">
                          {{ new Date(slot.date).toLocaleDateString('en-PH', { weekday: 'short' }) }}
                        </span>
                        <!-- Status Badge -->
                        <div class="absolute -top-2 -right-1.5" v-if="slot.booked_morning >= slot.morning_slots && slot.booked_afternoon >= slot.afternoon_slots">
                          <span class="bg-red-500 text-white border-2 border-amber-50 text-[0.45rem] font-black px-1.5 py-0.5 rounded shadow-sm">FULL</span>
                        </div>
                        <div class="absolute -top-2 -right-1.5" v-else-if="form.pickup_date === slot.date">
                          <span class="bg-yellow-400 text-slate-900 border-2 border-[#154252] text-[0.45rem] font-black px-1.5 py-0.5 rounded shadow-sm">✓</span>
                        </div>
                      </button>
                    </div>
                    <p v-else class="text-[0.7rem] text-red-500 font-bold bg-white p-3 rounded-lg border border-red-100">No available pickup dates scheduled at the moment.</p>
                  </div>

                  <!-- Time Slot Selection -->
                  <div class="flex flex-col gap-2">
                    <label class="text-[0.65rem] font-black text-[#154252] uppercase tracking-widest border-b border-amber-200 pb-1">Time</label>
                    <div class="flex gap-2">
                      <button 
                        v-for="time in availableTimes" 
                        :key="time"
                        type="button"
                        @click="form.pickup_time = time"
                        :disabled="isTimeDisabled(time)"
                        :class="[
                          'flex-1 py-3 rounded-xl border-2 transition-all flex flex-col items-center justify-center text-center',
                          isTimeDisabled(time)
                            ? 'bg-slate-100 border-slate-200 text-slate-400 cursor-not-allowed opacity-60'
                            : form.pickup_time === time 
                              ? 'bg-[#154252] border-[#154252] text-yellow-400 shadow-md' 
                              : 'bg-white border-white text-slate-600 hover:border-amber-400'
                        ]"
                      >
                        <span class="text-xs font-black uppercase tracking-wide">{{ time }}</span>
                        <span class="text-[0.6rem] font-bold opacity-80 mt-0.5">
                          {{ time === 'Morning' ? '8:00 AM - 12:00 PM' : '1:00 PM - 5:00 PM' }}
                        </span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- General Submit Error -->
              <div v-if="submitError" class="text-red-600 text-[0.7rem] font-bold uppercase tracking-wider text-center bg-red-50 border border-red-200 rounded-lg p-3 shadow-sm">{{ submitError }}</div>
            </div>
          </form>

          <!-- Modal Footer -->
          <div class="px-10 py-6 border-t border-slate-100 flex flex-col sm:flex-row justify-between items-center gap-4 bg-slate-50/50 sticky bottom-0 z-10 backdrop-blur-sm">
            <!-- Branding -->
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-full bg-[#99dbce] flex items-center justify-center shadow-inner">
                <img :src="logoImg" alt="logo" class="w-6 h-6 object-contain" />
              </div>
              <div class="flex flex-col leading-tight">
                <span class="text-sm font-bold text-slate-800 italic">StandAlone</span>
                <span class="text-[0.6rem] font-bold text-slate-500 uppercase tracking-wider">La Union SHS</span>
              </div>
            </div>
            
            <!-- Controls -->
            <div class="flex gap-4 w-full sm:w-auto">
              <!-- Actions for Step 1 -->
              <template v-if="currentStep === 1">
                <button type="button" @click="closeModal" class="flex-1 sm:flex-none px-8 py-2.5 border-2 border-slate-200 text-slate-600 font-bold rounded-lg hover:border-slate-800 hover:text-slate-800 transition-colors">Cancel</button>
                <button type="button" @click="goToNextStep" class="flex-1 sm:flex-none px-8 py-2.5 bg-[#154252] text-white hover:bg-[#0d2a35] font-black rounded-lg shadow-md transition-all hover:shadow-lg active:scale-95 flex items-center justify-center gap-2">
                  Next Step
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </button>
              </template>
              
              <!-- Actions for Step 2 -->
              <template v-else>
                <button type="button" @click="currentStep = 1" class="flex-1 sm:flex-none px-8 py-2.5 border-2 border-slate-200 text-slate-600 font-bold rounded-lg hover:border-slate-800 hover:text-slate-800 transition-colors flex items-center justify-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  Back
                </button>
                <button type="submit" form="submission-form" :disabled="submitting || recordStatus !== 'found'" class="flex-1 sm:flex-none px-8 py-2.5 bg-yellow-400 hover:bg-yellow-500 font-black text-slate-900 rounded-lg shadow-md transition-all hover:shadow-lg active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed">
                  <span v-if="submitting">Submitting...</span>
                  <span v-else-if="recordStatus === 'not_found'">Unavailable</span>
                  <span v-else>Submit Request</span>
                </button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ===================== TRACKING RESULT MODAL ===================== -->
    <Teleport to="body">
      <div v-if="showTrackModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="showTrackModal = false">
        <div class="bg-white w-full max-w-2xl rounded-2xl shadow-2xl border-4 border-[#154252] flex flex-col max-h-[90vh] overflow-hidden">
          <div class="px-8 py-6 bg-[#154252] text-white flex justify-between items-center shrink-0">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-yellow-400 rounded-lg flex items-center justify-center text-[#154252]">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>
              </div>
              <h2 class="text-xl font-black uppercase tracking-tight">Passkey: {{ trackedRequest?.passkey }}</h2>
            </div>
            <button @click="showTrackModal = false" class="p-2 hover:bg-white/10 rounded-full transition-colors"><XIcon class="w-6 h-6" /></button>
          </div>

          <div class="p-8 overflow-y-auto" v-if="trackedRequest">
            <div class="flex flex-col md:flex-row gap-8 mb-8">
               <div class="flex-1 p-5 bg-slate-50 rounded-xl border border-slate-200">
                 <h3 class="text-[0.65rem] font-black text-slate-400 uppercase tracking-widest mb-4">Request Info</h3>
                 <div class="space-y-3">
                   <div class="flex justify-between"><span class="text-xs font-bold text-slate-500">Name:</span> <span class="text-xs font-black text-[#154252]">{{ trackedRequest.first_name }} {{ trackedRequest.last_name }}</span></div>
                   <div class="flex justify-between"><span class="text-xs font-bold text-slate-500">Applied:</span> <span class="text-xs font-black text-[#154252]">{{ new Date(trackedRequest.submitted_at).toLocaleDateString() }}</span></div>
                   <div class="flex justify-between"><span class="text-xs font-bold text-slate-500">Pickup:</span> <span class="text-xs font-black text-[#154252]">{{ trackedRequest.pickup_date }} @ {{ trackedRequest.pickup_time }}</span></div>
                 </div>
               </div>
               <div class="flex-1 p-5 border-2 border-[#154252] rounded-xl flex flex-col items-center justify-center text-center">
                 <h3 class="text-[0.65rem] font-black text-slate-400 uppercase tracking-widest mb-2">Current Status</h3>
                 <div class="text-2xl font-black text-[#154252] uppercase mb-1">{{ trackedRequest.status }}</div>
                 <p class="text-[0.6rem] font-bold text-slate-500 uppercase tracking-tighter">Last Update: {{ new Date(trackedRequest.submitted_at).toLocaleString() }}</p>
               </div>
            </div>

            <div class="mb-6">
              <h3 class="text-sm font-black text-[#154252] uppercase mb-4 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                Requested Documents
              </h3>
              <div class="grid grid-cols-1 gap-3">
                <div v-for="file in trackedRequest.requested_files" :key="file" class="bg-slate-50 border border-slate-200 p-4 rounded-xl flex items-center justify-between group">
                  <div class="flex flex-col">
                    <span class="text-xs font-black text-[#154252]">{{ file }}</span>
                    <span v-if="trackedRequest.processed_documents?.find(d => d.document_type === file)" class="text-[0.6rem] font-bold text-green-500 uppercase">✓ Document Ready</span>
                    <span v-else class="text-[0.6rem] font-bold text-amber-500 uppercase">On Process</span>
                  </div>
                  
                  <div v-if="trackedRequest.processed_documents?.find(d => d.document_type === file)">
                    <a :href="'http://127.0.0.1:8000' + trackedRequest.processed_documents.find(d => d.document_type === file).file" 
                       target="_blank"
                       class="px-5 py-2 bg-[#154252] text-white text-[0.65rem] font-black uppercase rounded shadow-lg shadow-[#154252]/20 hover:bg-yellow-400 hover:text-[#154252] transition-all flex items-center gap-2">
                       <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
                       Download
                    </a>
                  </div>
                </div>
              </div>
            </div>

            <div class="p-4 bg-amber-50 rounded-xl border border-amber-200">
               <p class="text-[0.7rem] font-bold text-amber-800 leading-relaxed italic">
                 Note: If your document status is "Ready", you can download the digital copy above. Please bring a valid ID when picking up your physical documents at the school on your scheduled date.
               </p>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ===================== SUCCESS MODAL ===================== -->
    <Teleport to="body">
      <div v-if="showSuccess" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
        <div class="bg-white w-full max-w-sm rounded-2xl shadow-2xl border border-slate-200 px-10 py-10 text-center">
          <!-- Green Check Icon -->
          <div class="flex justify-center mb-4">
            <div class="w-16 h-16 rounded-full bg-green-500 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-9 h-9 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
          <h2 class="text-2xl font-black text-green-600 mb-1">Request Submitted!</h2>
          <div v-if="submittedRequestId" class="my-4 p-4 bg-slate-50 border-2 border-dashed border-[#154252] rounded-xl flex flex-col items-center">
            <span class="text-[0.6rem] font-black text-slate-400 uppercase tracking-widest">Your Passkey</span>
            <span class="text-2xl font-black text-[#154252]">{{ submittedRequestId }}</span>
            <span class="text-[0.6rem] font-bold text-slate-400 mt-1 uppercase tracking-tighter">Save this for tracking</span>
          </div>
          <p class="text-sm text-slate-400 mb-6">Your record request has been recorded in our system.</p>
          <div class="text-left mb-6">
            <p class="text-[#e07b2a] font-bold mb-1">What's Next?</p>
            <p class="text-slate-800 text-sm leading-relaxed text-center">
              Please monitor your email for updates regarding your request status. 
              Our registrar staff will review your documents and verify your clearance shortly.
            </p>
          </div>
          <button @click="closeSuccess" class="w-full py-3 bg-[#154252] hover:bg-[#0d2a35] text-white font-bold rounded-lg transition-colors">Close</button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue';
import bgImg from '@/assets/launion.png';
import logoImg from '@/assets/logo-launion.png';
import sittingPersonImg from '@/assets/sitting_person.png';
import { requestService, publicService } from '@/services/api';

// Lucide Icons
import { X as XIcon, CheckCircle as CheckIcon, AlertCircle as AlertIcon, Search as SearchIcon, Calendar as CalendarIcon, Clock as ClockIcon, FileText as FileTextIcon } from 'lucide-vue-next';

// Modal State
const showModal = ref(false);
const showSuccess = ref(false);
const showTrackModal = ref(false);
const submittedRequestId = ref(null);

const currentStep = ref(1);
const requestForm = ref(null);

const submitting = ref(false);
const submitError = ref('');
const fileError = ref('');
const fileSelectValue = ref('');
const selectedFiles = ref([]);
const docTypes = ref([]);
const strands = ref([]);

// Tracking State
const trackId = ref('');
const trackEmail = ref('');
const tracking = ref(false);
const trackError = ref('');
const trackedRequest = ref(null);

// Record status checking
const checkingRecord = ref(false);
const recordStatus = ref('idle'); // idle, checking, found, duplicate, not_found
const availableDocs = ref([]);
const duplicateMessage = ref('');

// Form Data
const form = reactive({
  first_name: '',
  middle_name: '',
  last_name: '',
  suffix: '',
  sex: '',
  year_graduated: '',
  strand_type: '',
  birthdate: '',
  lrn_number: '',
  email: '',
  phone_number: '',
  permanent_address: '',
  pickup_date: '',
  pickup_time: '',
});

const filteredDocTypes = computed(() => {
  if (recordStatus.value !== 'found') return [];
  // Only show document types that exist for this student in the master database
  return docTypes.value.filter(dt => availableDocs.value.includes(dt.name));
});

const slots = ref([]);
const loadingSlots = ref(false);
const availableTimes = ['Morning', 'Afternoon'];

function handleDateSelect(slot) {
  form.pickup_date = slot.date;
  form.pickup_time = ''; // Reset chosen time when date changes
}

function isTimeDisabled(time) {
  if (!form.pickup_date) return true; // Disabled if no date selected
  const slot = slots.value.find(s => s.date === form.pickup_date);
  if (!slot) return true;
  if (time === 'Morning') return slot.booked_morning >= slot.morning_slots;
  if (time === 'Afternoon') return slot.booked_afternoon >= slot.afternoon_slots;
  return false;
}

function openModal() {
  loadSlots();
  currentStep.value = 1;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  setTimeout(resetForm, 300); // Wait for transition
}

function goToNextStep() {
  if (requestForm.value && requestForm.value.reportValidity()) {
    currentStep.value = 2;
  }
}

function closeSuccess() {
  showSuccess.value = false;
}

function addFile() {
  const val = fileSelectValue.value;
  if (!val) return;
  if (!selectedFiles.value.includes(val)) {
    selectedFiles.value.push(val);
  }
  // Reset the dropdown so it can be selected again for another file
  fileSelectValue.value = '';
}

function removeFile(index) {
  selectedFiles.value.splice(index, 1);
}

function removeAllFiles() {
  selectedFiles.value = [];
}

function resetForm() {
  Object.keys(form).forEach(k => { form[k] = ''; });
  selectedFiles.value = [];
  fileSelectValue.value = '';
  submitError.value = '';
  fileError.value = '';
  currentStep.value = 1;
}

async function handleSubmit() {
  fileError.value = '';
  submitError.value = '';

  if (selectedFiles.value.length === 0) {
    fileError.value = 'Please select at least one file to request.';
    return;
  }

  if (!form.pickup_date || !form.pickup_time) {
    submitError.value = 'Please select a preferred pickup date and time.';
    return;
  }

  submitting.value = true;
  try {
    const res = await requestService.submitRequest({
      ...form,
      requested_files: selectedFiles.value,
    });
    submittedRequestId.value = res.data.passkey;
    showModal.value = false;
    showSuccess.value = true;
    resetForm();
  } catch (err) {
    const data = err.response?.data;
    if (data) {
      const firstKey = Object.keys(data)[0];
      submitError.value = Array.isArray(data[firstKey]) ? data[firstKey][0] : data[firstKey];
    } else {
      submitError.value = 'Something went wrong. Please try again.';
    }
  } finally {
    submitting.value = false;
  }
}

async function loadDocTypes() {
  try {
    const res = await requestService.getPublicDocTypes();
    docTypes.value = res.data;
  } catch (err) {
    console.error('Failed to load doc types');
  }
}

async function loadSlots() {
  loadingSlots.value = true;
  try {
    const res = await requestService.getPublicSlots();
    slots.value = res.data;
  } catch (err) {
    console.error('Failed to load slots');
  } finally {
    loadingSlots.value = false;
  }
}

async function loadStrands() {
  try {
    const res = await requestService.getPublicStrands();
    strands.value = res.data;
  } catch (err) {
    console.error('Failed to load strands');
  }
}

async function handleTrack() {
  if (!trackId.value || !trackEmail.value) {
    trackError.value = 'Please provide both Passkey and Email.';
    return;
  }
  
  trackError.value = '';
  tracking.value = true;
  trackedRequest.value = null;

  try {
    const res = await publicService.getMyRequest(trackEmail.value, trackId.value);
    trackedRequest.value = res.data;
    showTrackModal.value = true;
  } catch (err) {
    trackError.value = err.response?.data?.error || 'No matching request found. Please check your Passkey and Email.';
  } finally {
    tracking.value = false;
  }
}

const initials = (f, l) => {
  if (!f) return '?';
  return `${f[0]}${l?.[0] || ''}`.toUpperCase();
};

let checkTimeout = null;
async function handleRecordCheck() {
  if ((!form.first_name || !form.last_name) && !form.lrn_number) {
    recordStatus.value = 'idle';
    availableDocs.value = [];
    return;
  }

  checkingRecord.value = true;
  try {
    const params = {};
    if (form.lrn_number) params.lrn = form.lrn_number;
    if (form.first_name) params.first_name = form.first_name;
    if (form.last_name) params.last_name = form.last_name;

    const res = await publicService.checkRecord(params);
    if (res.data.exists) {
      if (res.data.has_active_request) {
        recordStatus.value = 'duplicate';
        duplicateMessage.value = res.data.message;
        availableDocs.value = [];
      } else {
        recordStatus.value = 'found';
        availableDocs.value = res.data.documents;
        duplicateMessage.value = '';
      }
    } else {
      recordStatus.value = 'not_found';
      availableDocs.value = [];
      duplicateMessage.value = '';
    }
  } catch (err) {
    console.error('Check failed:', err);
    recordStatus.value = 'not_found';
  } finally {
    checkingRecord.value = false;
  }
}

// Watchers for real-time checking
watch(() => [form.first_name, form.last_name, form.lrn_number], () => {
  clearTimeout(checkTimeout);
  checkTimeout = setTimeout(handleRecordCheck, 800);
});

onMounted(() => {
  loadDocTypes();
  loadSlots();
  loadStrands();
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
