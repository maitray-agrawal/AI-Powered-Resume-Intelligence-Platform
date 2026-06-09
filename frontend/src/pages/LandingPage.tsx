import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Button from '../components/ui/Button';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  const handleStartTrial = () => {
    navigate('/dashboard');
  };

  return (
    <div className="bg-surface text-on-surface selection:bg-primary-container selection:text-on-primary-container min-h-screen">
      {/* TopNavBar */}
      <header className="bg-surface/70 dark:bg-surface-dim/70 backdrop-blur-md border-b border-outline-variant dark:border-outline shadow-sm dark:shadow-none docked full-width top-0 sticky flex justify-between items-center w-full px-gutter h-16 z-40">
        <div className="flex items-center gap-xs">
          <span className="material-symbols-outlined text-primary text-3xl mr-1" style={{ fontVariationSettings: "'FILL' 1" }}>
            rocket_launch
          </span>
          <span className="font-headline-md text-headline-md font-bold text-primary dark:text-inverse-primary">
            AeroTalent AI
          </span>
        </div>
        <nav className="hidden md:flex items-center gap-lg">
          <Link className="text-primary dark:text-inverse-primary font-bold border-b-2 border-primary font-label-md text-label-md transition-colors h-16 flex items-center" to="/">
            Home
          </Link>
          <a className="text-on-surface-variant dark:text-on-surface-variant hover:bg-surface-container-high dark:hover:bg-on-secondary-fixed-variant transition-colors px-3 py-2 rounded-lg font-label-md text-label-md" href="#features">
            Features
          </a>
          <a className="text-on-surface-variant dark:text-on-surface-variant hover:bg-surface-container-high dark:hover:bg-on-secondary-fixed-variant transition-colors px-3 py-2 rounded-lg font-label-md text-label-md" href="#pricing">
            Pricing
          </a>
          <Link className="text-on-surface-variant dark:text-on-surface-variant hover:bg-surface-container-high dark:hover:bg-on-secondary-fixed-variant transition-colors px-3 py-2 rounded-lg font-label-md text-label-md" to="/dashboard">
            Recruiter App
          </Link>
        </nav>
        <div className="flex items-center gap-sm">
          <Button variant="ghost" size="sm" icon="notifications" className="p-2" />
          <Button variant="ghost" size="sm" icon="settings" className="p-2" />
          <Button variant="primary" size="md" onClick={handleStartTrial}>
            Enter Platform
          </Button>
        </div>
      </header>

      <main>
        {/* Hero Section */}
        <section className="relative overflow-hidden pt-24 pb-16 md:pt-32 md:pb-32 px-gutter bg-surface-bright">
          <div className="max-w-container-max mx-auto relative z-10 grid md:grid-cols-2 gap-xl items-center">
            <div className="space-y-md text-left">
              <div className="inline-flex items-center gap-xs px-3 py-1 bg-on-tertiary-container/10 text-on-tertiary-container rounded-full border border-on-tertiary-container/20 w-fit">
                <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                  auto_awesome
                </span>
                <span className="font-label-sm text-label-sm uppercase tracking-wider">
                  Next-Gen Recruitment AI
                </span>
              </div>
              <h1 className="font-display-lg text-display-lg text-primary max-w-xl">
                Hire at the <span className="text-on-tertiary-container italic">speed of thought</span>
              </h1>
              <p className="font-body-lg text-body-lg text-on-surface-variant max-w-lg">
                The executive search engine that thinks like a recruiter. Automate screening, matching, and reporting with enterprise-grade precision and AI-human synergy.
              </p>
              <div className="flex flex-col sm:flex-row gap-md pt-4">
                <Button variant="primary" size="lg" icon="arrow_forward" shimmer onClick={handleStartTrial}>
                  Start Free Trial
                </Button>
                <Button variant="outline" size="lg" icon="play_circle">
                  Watch Video
                </Button>
              </div>
            </div>

            <div className="relative">
              {/* Glassmorphism Product Preview */}
              <div className="relative rounded-2xl border border-outline-variant bg-white/40 backdrop-blur-xl p-6 shadow-2xl overflow-hidden aspect-square md:aspect-video flex items-center justify-center">
                <div className="relative z-20 w-full max-w-sm space-y-sm bg-white rounded-xl p-6 shadow-sm border border-outline-variant text-left">
                  <div className="flex items-center justify-between border-b border-outline-variant pb-2">
                    <span className="font-label-md text-label-md text-primary font-bold">Candidate Analysis</span>
                    <span className="material-symbols-outlined text-on-tertiary-container" style={{ fontVariationSettings: "'FILL' 1" }}>
                      verified
                    </span>
                  </div>
                  <div className="flex items-center gap-md py-2">
                    <div className="w-16 h-16 rounded-full bg-surface-container-high flex-shrink-0">
                      <img
                        alt="Elena Rodriguez profile headshot"
                        className="w-full h-full object-cover rounded-full"
                        src="https://lh3.googleusercontent.com/aida-public/AB6AXuBkv9gfEweiEXkYV9zHlDx0xRTIUYXaPta-EnbzqoHKewk1eHu0zZSAtW_pQk1OY0erOH76b_xWbCPIfVDnQwIifB-CG9jng81h4e0hIAl-CrX0bzMxoil6DzgFv2ZvxDENtFHEoM921cYyVeHr0XOis0MI6ttv6B3n-4yAGy5tQUPsEfp5ssqZuL8hAPLWwzqFBerLnFWHUGUBKOIHKRPnitbcRFaUb_48tDodGzVZH9k5mUUVaHt3ZV97m5bqXDXKVTqL8zwwTBY"
                      />
                    </div>
                    <div className="space-y-xs">
                      <h4 className="font-headline-md text-headline-md text-on-surface font-semibold">Elena Rodriguez</h4>
                      <p className="font-label-sm text-label-sm text-on-surface-variant">Lead ML Architect • 12 Yrs Exp</p>
                    </div>
                  </div>
                  <div className="space-y-xs">
                    <div className="flex justify-between font-label-sm text-label-sm">
                      <span className="text-on-surface-variant">Cultural Alignment</span>
                      <span className="text-on-tertiary-container font-bold">98% Match</span>
                    </div>
                    <div className="h-2 w-full bg-surface-container rounded-full overflow-hidden">
                      <div className="h-full bg-on-tertiary-container w-[98%] rounded-full"></div>
                    </div>
                  </div>
                  <div className="pt-2">
                    <div className="bg-on-tertiary-container/5 p-3 rounded-lg border border-on-tertiary-container/10">
                      <p className="font-body-sm text-body-sm italic text-on-surface">
                        "AI Insight: Elena possesses deep expertise in transformer architectures and has scaled teams of 40+ engineers."
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              {/* Decorative Elements */}
              <div className="absolute -top-12 -right-12 w-64 h-64 bg-primary/5 rounded-full blur-3xl -z-10"></div>
              <div className="absolute -bottom-12 -left-12 w-64 h-64 bg-on-tertiary-container/10 rounded-full blur-3xl -z-10"></div>
            </div>
          </div>
        </section>

        {/* Trust Badges */}
        <section className="py-16 border-y border-outline-variant bg-surface-bright">
          <div className="max-w-container-max mx-auto px-gutter text-center">
            <p className="font-label-md text-label-md text-on-surface-variant mb-10 uppercase tracking-[0.2em]">
              Trusted by the world's most innovative teams
            </p>
            <div className="flex flex-wrap justify-center items-center gap-xl opacity-40 grayscale hover:grayscale-0 transition-all duration-700">
              <img alt="Amazon Logo" className="h-8" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAoDSiIRpzCeemmhnwVYR7vWiR1wz7xt8p8jxn5Ii_xq6ggFunsO6QhhZTC3qx8IROn3PbVqQcz7ShHF7XF26z_jupBwVXTiQFQyrI3fToj4glx4CmvuKrfbhoFt2jdFV-7Bo4lu9umUjhaAlfa7ogE1V0L8v6GwbbRUNa-mtOdeGezhJfX-4v4D4qtlXH4uOjScXE8ukNgQXIJlxqHMPDsVPkFCtfVSukRV-s4zFf2gVZqau-SpjT_i415li5TJAcijQm9WiZPNt0" />
              <img alt="Google Logo" className="h-8" src="https://lh3.googleusercontent.com/aida-public/AB6AXuD-mRgcGZ6-mxiErvj4cUya3V4JdgJKGzRe18gowKYWuXITSEKZa729sxFzjaYU-TjuHUkhzWx2tyB2fr0s8K8QrlIwFOZkHMWkKBAv6470ZugyzRm2H1b2WMC9zp0BVQ4l61AfhqpEakVeemlXFWik2zqXJhQBYxfCxcR86XzmFZYyHoPkETvOGK8zbJsts7CH0Kb06BNC1uo8N2FGVM0N1Ufm6Fjbzj18Z7SRh4VLbNLPBI0_ylCdMjuJtu-UUeRyF6ru1sLoLsY" />
              <img alt="IBM Logo" className="h-8" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDdl5r1hTsIPwOwkeQqzryrv3WpdoTNBDeaPzvMAkx3VDV6H4woER93fHRy-TenYdAq973WQfomZRBqmQQsE_TL4sw1VspEnfST09yXvJSB13d-Sv9x8PxdhBvNWFKpYYbNUaPDT-Z8IQxHR2DRSnHwlHPVnsT692-5cQWPLepn42_uIiZMYtmGsegvKQHsSuNWylfCUGO5fzM1mZl_MsBMaF3Gc8a8ilgLaIAeLjwSqg4rvqIMlumq9HCop0kSupMU4ql_JMEhAbM" />
              <img alt="Netflix Logo" className="h-10" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBo8MNlnk253kzLmwKKwdpJiBRVi-7KKX5NTuoI9P2UgEQtkX-NVN0FGD0k6rE-C0kgdhf1TKRa8wZ1PS5xZay9YM6uvLJnWA2KSUQ73FrmaeE-myzHVrroNJ334Qx51yapPi-vVhVT-VdU5HEFjluWKjlzkDgJoTXWtCj8q93MHj-06QEe3HAPOb_WbUm5YisM4tCVQ-kkTAPVpHO6GzrERGXK5YNgHC24nTNz27agwYfsF3Gw83wnLipixqhzAdevOCFdIHy_kx0" />
              <img alt="Microsoft Logo" className="h-8" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCp4O06eEgNE_Hyd0Py8kUsiVoHxHZgyyC9arKIN1HC80DkEE6yTS7DREAHNtvX38HM6kE-VPmI1xC2_Nz8EaueIJwkE2KrW-iquM4DI8cEHwM3DXt9H3tvLbvhvhIYeMColvnfhWFdh2NEruc2cqzYObOl6Lfk8pZ8vUwl1yr2kWda-n4QylY9TN8qSZHH_BKddzrIFkmX613jaVhEC-t8i55KnxNMfjYxUs5iRpU3QB8zuOCPPJC1wmBpisbyg4cxK6J7ALfO_xE" />
            </div>
          </div>
        </section>

        {/* Feature Bento Grid */}
        <section id="features" className="py-xl bg-surface-container-low px-gutter">
          <div className="max-w-container-max mx-auto">
            <div className="text-center mb-xl space-y-sm">
              <h2 className="font-display-lg text-display-lg text-primary">Everything you need to hire elite talent</h2>
              <p className="font-body-lg text-body-lg text-on-surface-variant max-w-2xl mx-auto">
                From instant resume parsing to behavioral analysis, AeroTalent AI handles the heavy lifting so you can focus on the human connection.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-12 gap-gutter text-left">
              {/* AI Screening */}
              <div className="md:col-span-8 bg-white rounded-2xl border border-outline-variant p-lg flex flex-col md:flex-row gap-lg items-center hover:shadow-lg transition-shadow duration-300">
                <div className="flex-1 space-y-md">
                  <div className="w-12 h-12 rounded-xl bg-primary-container flex items-center justify-center text-on-primary-container">
                    <span className="material-symbols-outlined">psychology</span>
                  </div>
                  <h3 className="font-headline-lg text-headline-lg text-primary font-bold">AI-Human Screening</h3>
                  <p className="font-body-md text-body-md text-on-surface-variant">
                    Our models don't just search for keywords. They understand context, career trajectory, and implicit skills like a seasoned recruiter.
                  </p>
                  <ul className="space-y-xs font-label-md text-label-md text-on-surface">
                    <li className="flex items-center gap-xs">
                      <span className="material-symbols-outlined text-on-tertiary-container text-[18px]">check_circle</span>
                      Contextual skill verification
                    </li>
                    <li className="flex items-center gap-xs">
                      <span className="material-symbols-outlined text-on-tertiary-container text-[18px]">check_circle</span>
                      Bias-mitigated ranking
                    </li>
                    <li className="flex items-center gap-xs">
                      <span className="material-symbols-outlined text-on-tertiary-container text-[18px]">check_circle</span>
                      Real-time profile updates
                    </li>
                  </ul>
                </div>
                <div className="flex-1 w-full h-64 bg-surface-container rounded-xl overflow-hidden relative flex items-center justify-center p-4">
                  <div className="bg-white/85 p-4 rounded-lg border border-outline-variant shadow-sm w-full max-w-xs space-y-xs">
                    <div className="flex justify-between items-center text-xs font-bold text-primary">
                      <span>ATS Match Validation</span>
                      <span className="bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full">Passed</span>
                    </div>
                    <p className="text-xs text-on-surface-variant">Verified Skills: TypeScript, React Router, TailwindCSS, FastAPI</p>
                    <p className="text-[10px] text-slate-400">Score: 96% match against core roles</p>
                  </div>
                </div>
              </div>

              {/* JD Matching */}
              <div className="md:col-span-4 bg-white rounded-2xl border border-outline-variant p-lg space-y-md hover:shadow-lg transition-shadow">
                <div className="w-12 h-12 rounded-xl bg-on-tertiary-container/10 flex items-center justify-center text-on-tertiary-container">
                  <span className="material-symbols-outlined">fact_check</span>
                </div>
                <h3 className="font-headline-md text-headline-md text-primary font-bold">JD Matcher</h3>
                <p className="font-body-sm text-body-sm text-on-surface-variant">
                  Instantly compare candidates against complex Job Descriptions with multi-dimensional scoring.
                </p>
                <div className="pt-sm">
                  <div className="bg-surface-container-highest p-sm rounded-lg flex items-center justify-between">
                    <span className="font-label-sm text-label-sm">Role Compatibility</span>
                    <span className="text-on-tertiary-container font-bold text-headline-md">94%</span>
                  </div>
                </div>
              </div>

              {/* Resume Chat */}
              <div className="md:col-span-4 bg-primary text-on-primary rounded-2xl p-lg space-y-md hover:shadow-xl transition-shadow">
                <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center">
                  <span className="material-symbols-outlined text-white">forum</span>
                </div>
                <h3 className="font-headline-md text-headline-md font-bold">Resume Chat</h3>
                <p className="font-body-sm text-body-sm text-on-primary-container">
                  Ask our AI anything about a candidate's history. "Does this person have experience scaling high-load AWS clusters?"
                </p>
                <div className="bg-white/10 rounded-lg p-3 border border-white/20">
                  <p className="font-label-sm text-label-sm opacity-80 text-white">AI: Yes, during their 3 years at Stripe...</p>
                </div>
              </div>

              {/* Automated Reporting */}
              <div className="md:col-span-8 bg-white rounded-2xl border border-outline-variant p-lg flex flex-col md:flex-row gap-lg items-center hover:shadow-lg transition-shadow">
                <div className="flex-1 order-2 md:order-1 w-full h-48 bg-surface-container rounded-xl overflow-hidden relative">
                  <img
                    alt="Analytics dashboard display preview"
                    className="w-full h-full object-cover"
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuBSiChahiMDc44wlSdXd7bQdIorVY_rQfxxI0p_i6vpQw9I5B8L3M-8gIVWei9ekxETrSjvxVkCle9fjty1dGB6BDz64UA6IV-35VIoiYcG1cn_B31D35Bxls4eFTNTTAJYIg0A3mvtvXvzJwVQ_nNkCIYvqXWojKdQ3ed35KXgv8f0P2Pw2RPbmP-TgHkTSxGBOG-6masNLk-KVBHFFKE-jJh3gFNF-x2_-2KEfz-BrSQ6lltWnbNeFrsZIUkPLaEr9a70ci_4JUg"
                  />
                </div>
                <div className="flex-1 order-1 md:order-2 space-y-md">
                  <div className="w-12 h-12 rounded-xl bg-secondary-container flex items-center justify-center text-on-secondary-container">
                    <span className="material-symbols-outlined">assessment</span>
                  </div>
                  <h3 className="font-headline-lg text-headline-lg text-primary font-bold">Automated Reporting</h3>
                  <p className="font-body-md text-body-md text-on-surface-variant">
                    Generate executive-ready hiring reports with a single click. Deep insights into your talent pipeline health.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <section id="pricing" className="py-xl px-gutter bg-surface">
          <div className="max-w-container-max mx-auto text-center mb-xl">
            <h2 className="font-display-lg text-display-lg text-primary mb-sm">Transparent, Enterprise-Ready Pricing</h2>
            <p className="font-body-lg text-body-lg text-on-surface-variant">Scale your recruitment with tools that grow with you.</p>
          </div>
          <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-lg text-left">
            {/* Professional Plan */}
            <div className="bg-white rounded-3xl border border-outline-variant p-xl space-y-lg flex flex-col hover:border-primary transition-colors">
              <div className="space-y-sm">
                <h3 className="font-headline-lg text-headline-lg text-primary font-bold">Professional</h3>
                <p className="font-body-md text-body-md text-on-surface-variant">Perfect for growing startups and boutique agencies.</p>
                <div className="pt-md">
                  <span className="font-display-lg text-display-lg text-primary font-bold">$499</span>
                  <span className="font-label-md text-label-md text-on-surface-variant">/mo</span>
                </div>
              </div>
              <ul className="space-y-md flex-1">
                <li className="flex items-center gap-sm font-body-md text-body-md">
                  <span className="material-symbols-outlined text-on-tertiary-container">check_circle</span>
                  Up to 500 candidate analyses/mo
                </li>
                <li className="flex items-center gap-sm font-body-md text-body-md">
                  <span className="material-symbols-outlined text-on-tertiary-container">check_circle</span>
                  AI Resume Chat
                </li>
                <li className="flex items-center gap-sm font-body-md text-body-md">
                  <span className="material-symbols-outlined text-on-tertiary-container">check_circle</span>
                  Standard Reporting
                </li>
              </ul>
              <Button variant="outline" size="md" className="w-full" onClick={handleStartTrial}>
                Get Started
              </Button>
            </div>
            {/* Enterprise Plan */}
            <div className="bg-primary-container text-on-primary rounded-3xl p-xl space-y-lg flex flex-col relative overflow-hidden shadow-2xl">
              <div className="absolute top-4 right-4 bg-on-tertiary-container text-tertiary px-3 py-1 rounded-full font-label-sm text-label-sm font-bold uppercase tracking-widest">
                Popular
              </div>
              <div className="space-y-sm">
                <h3 className="font-headline-lg text-headline-lg text-inverse-primary font-bold">Enterprise</h3>
                <p className="font-body-md text-body-md opacity-80">Full-scale talent intelligence for global organizations.</p>
                <div className="pt-md">
                  <span className="font-display-lg text-display-lg font-bold">Custom</span>
                </div>
              </div>
              <ul className="space-y-md flex-1">
                <li className="flex items-center gap-sm font-body-md text-body-md">
                  <span className="material-symbols-outlined text-on-tertiary-fixed">verified</span>
                  Unlimited candidate analyses
                </li>
                <li className="flex items-center gap-sm font-body-md text-body-md">
                  <span className="material-symbols-outlined text-on-tertiary-fixed">verified</span>
                  Custom AI Model Training
                </li>
                <li className="flex items-center gap-sm font-body-md text-body-md">
                  <span className="material-symbols-outlined text-on-tertiary-fixed">verified</span>
                  White-label Reporting
                </li>
                <li className="flex items-center gap-sm font-body-md text-body-md">
                  <span className="material-symbols-outlined text-on-tertiary-fixed">verified</span>
                  Dedicated Account Manager
                </li>
              </ul>
              <Button variant="ai" size="md" className="w-full" onClick={handleStartTrial}>
                Contact Sales
              </Button>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="py-xl px-gutter relative overflow-hidden">
          <div className="max-w-4xl mx-auto bg-white/90 backdrop-blur-xl border border-outline-variant rounded-3xl p-lg md:p-xl text-center shadow-2xl space-y-lg">
            <h2 className="font-display-lg text-display-lg text-primary font-bold">Ready to transform your hiring?</h2>
            <p className="font-body-lg text-body-lg text-on-surface-variant max-w-2xl mx-auto">
              Join the 2,000+ companies using AeroTalent AI to secure top-tier executives in record time.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-md">
              <Button variant="primary" size="lg" onClick={handleStartTrial}>
                Request Private Demo
              </Button>
              <Button variant="outline" size="lg">
                Speak to an Expert
              </Button>
            </div>
            <p className="font-label-sm text-label-sm text-on-surface-variant opacity-70">No credit card required. SOC2 Type II Compliant.</p>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-surface-bright dark:bg-background border-t border-outline-variant dark:border-outline py-lg">
        <div className="max-w-container-max mx-auto px-gutter flex flex-col md:flex-row justify-between items-center gap-md">
          <div className="flex flex-col items-center md:items-start gap-xs">
            <div className="flex items-center gap-xs">
              <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>
                rocket_launch
              </span>
              <span className="font-label-md text-label-md font-bold text-primary">AeroTalent AI</span>
            </div>
            <p className="font-body-sm text-body-sm text-on-surface-variant">© 2024 AeroTalent AI. Precision Recruiting.</p>
          </div>
          <nav className="flex flex-wrap justify-center gap-md">
            <a className="font-label-sm text-label-sm text-on-surface-variant hover:text-tertiary-container transition-opacity duration-150 hover:opacity-80 underline" href="#privacy">
              Privacy Policy
            </a>
            <a className="font-label-sm text-label-sm text-on-surface-variant hover:text-tertiary-container transition-opacity duration-150 hover:opacity-80 underline" href="#terms">
              Terms of Service
            </a>
            <a className="font-label-sm text-label-sm text-on-surface-variant hover:text-tertiary-container transition-opacity duration-150 hover:opacity-80 underline" href="#security">
              Security
            </a>
          </nav>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
