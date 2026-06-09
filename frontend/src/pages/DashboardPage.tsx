import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';

interface Candidate {
  id: string;
  name: string;
  role: string;
  targetRole: string;
  matchScore: number;
  status: string;
  avatar: string;
}

export const DashboardPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [candidates, setCandidates] = useState<Candidate[]>([
    {
      id: '1',
      name: 'Sarah Chen',
      role: 'Senior Cloud Architect',
      targetRole: 'Director of Engineering',
      matchScore: 98,
      status: 'Interviewing',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCU5Mr_gL6Bw1-etZL0mj2T9bfPk1sx8cYSb-LpyfrnnPxo1G14KbD1Qxf_GWOKpCDiB4NrxOqeVVLRsK-0UapHyy98ol3fVn_vxby3AleUKdy34ghlfgN4KxS2qnibsXmC_HVLultGXAzDkzIS9G-BT4183xl9hNrt-CBT55ac6S2mg6ge7IDNrfWA1J5DsVcP66DftJcdGnzqlI97Dp2zEGKhCsYCgZ72fbrNrR_92FFKXWggEsh9rLRtj0GxCvVIOMsJ8VvAhUw',
    },
    {
      id: '2',
      name: 'Marcus Holloway',
      role: 'Lead Product Manager',
      targetRole: 'VP of Product',
      matchScore: 94,
      status: 'Sourcing',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDHw8bAvEpls5YJ2hpjb_eFNp3FMpLfp90X74EJbLFYUoPI2L8iNc6HXOEwo0j3-_DoE7x3w-ts6b9GRG4gZ_4MOud9vOInnlAFox9QRj8exoxqSRzVoIxUFaCFf3cYJe4S_Uk-FLOHMcY9iUcCVAMza13cnNA_qoKd7K73QuWtCsDQwBw4fmPUkag7_NXwr1RlMgrwzDJbTbjGfLU5eh6VcRmRhH4cGXHsqqExovLYRzk2bRK6E5_P_kisK1SdRXIpu6OU-81o3tc',
    },
    {
      id: '3',
      name: 'David Stern',
      role: 'Data Scientist',
      targetRole: 'Head of AI Research',
      matchScore: 91,
      status: 'Offer Sent',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDmwCebx_UzjtcQkVMyF-yKo9y0HWZrTLez-roJdAYF-mWolKg6R_LRGZqXfkLHNzeRyuqDLaIdb5hI3fK11zlj1LXoawRSwSwLZHLaO-yq2aiphu87-bda1lAvIXjVLTegnVZ8M0Te8Uuv9U8QT0nC1d7P_fr1Maoj5uvf2KQL9xyKGkfoFhHBlFad4giuoSHbQRDmgmCbDq-v02IEqyc_o4Ac417t37U8qPU_uELO0CXwmrEaGTpfWgs0f8aG-NUwQMEN2o6yLyg',
    },
  ]);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newCandidate, setNewCandidate] = useState({
    name: '',
    role: '',
    targetRole: '',
    matchScore: 85,
    status: 'Sourcing',
  });

  const { data: systemInfo, request: getSystemInfo } = useApi();
  const { data: analyticsData, request: getAnalytics } = useApi();

  useEffect(() => {
    getSystemInfo('get', '/info').catch(() => {
      console.log('Backend API offline. Operating in fallback mock mode.');
    });
    getAnalytics('get', '/analytics/dashboard').catch(() => {
      console.log('Backend analytics offline. Operating in fallback mock mode.');
    });
  }, [getSystemInfo, getAnalytics]);

  const handleAddNewCandidate = (e: React.FormEvent) => {
    e.preventDefault();
    const candidateToAdd: Candidate = {
      id: String(candidates.length + 1),
      ...newCandidate,
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBkv9gfEweiEXkYV9zHlDx0xRTIUYXaPta-EnbzqoHKewk1eHu0zZSAtW_pQk1OY0erOH76b_xWbCPIfVDnQwIifB-CG9jng81h4e0hIAl-CrX0bzMxoil6DzgFv2ZvxDENtFHEoM921cYyVeHr0XOis0MI6ttv6B3n-4yAGy5tQUPsEfp5ssqZuL8hAPLWwzqFBerLnFWHUGUBKOIHKRPnitbcRFaUb_48tDodGzVZH9k5mUUVaHt3ZV97m5bqXDXKVTqL8zwwTBY',
    };
    setCandidates([candidateToAdd, ...candidates]);
    setIsModalOpen(false);
    setNewCandidate({
      name: '',
      role: '',
      targetRole: '',
      matchScore: 85,
      status: 'Sourcing',
    });
  };

  const filteredCandidates = candidates.filter(
    (c) =>
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.targetRole.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const fallbackAnalytics = {
    ats_score_history: [
      { date: '2026-06-01', score: 70 },
      { date: '2026-06-03', score: 75 },
      { date: '2026-06-05', score: 82 },
      { date: '2026-06-07', score: 80 },
      { date: '2026-06-09', score: 88 }
    ],
    jd_match_history: [
      { role: 'Frontend Architect', score: 68 },
      { role: 'Fullstack Engineer', score: 75 },
      { role: 'Lead FastAPI Dev', score: 89 },
      { role: 'Cloud DevOps Eng', score: 52 }
    ],
    skill_gaps: [
      { skill: 'Docker', frequency: 8 },
      { skill: 'AWS Solutions', frequency: 6 },
      { skill: 'Kubernetes', frequency: 5 },
      { skill: 'TypeScript', frequency: 4 },
      { skill: 'PostgreSQL', frequency: 3 }
    ],
    agent_scores: [
      { agent: 'ATS Expert', score: 85 },
      { agent: 'Recruiter', score: 90 },
      { agent: 'Resume Reviewer', score: 88 },
      { agent: 'Career Advisor', score: 82 }
    ]
  };

  const analytics = analyticsData || fallbackAnalytics;


  return (
    <div className="flex h-screen w-full bg-surface text-on-surface font-body-md overflow-hidden text-left">
      {/* SideNavBar */}
      <aside className="hidden md:flex flex-col h-full py-md px-sm gap-2 bg-surface-container-low border-r border-outline-variant w-64 sticky left-0 z-50">
        <div className="flex items-center px-4 mb-xl">
          <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center mr-3 flex-shrink-0">
            <span className="material-symbols-outlined text-white" style={{ fontVariationSettings: "'FILL' 1" }}>
              rocket_launch
            </span>
          </div>
          <div>
            <h1 className="font-headline-md text-headline-md font-extrabold text-primary leading-tight">AeroTalent</h1>
            <p className="font-label-sm text-label-sm text-on-surface-variant">Enterprise Tier</p>
          </div>
        </div>

        <Button
          variant="ai"
          size="lg"
          shimmer
          icon="add_circle"
          className="mx-2 mb-lg"
          onClick={() => setIsModalOpen(true)}
        >
          New Analysis
        </Button>

        <nav className="flex-grow flex flex-col gap-1">
          {[
            { id: 'dashboard', label: 'Dashboard', icon: 'dashboard' },
            { id: 'resumes', label: 'Resumes', icon: 'upload_file' },
            { id: 'analysis', label: 'Analysis', icon: 'analytics' },
            { id: 'matcher', label: 'JD Matcher', icon: 'fact_check' },
            { id: 'chat', label: 'AI Chat', icon: 'forum' },
            { id: 'reports', label: 'Reports', icon: 'assessment' },
          ].map((tab) => (
            <div
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`group flex items-center px-4 py-3 cursor-pointer transition-all duration-200 rounded-lg ${
                activeTab === tab.id
                  ? 'bg-secondary-container text-on-secondary-container font-bold'
                  : 'text-on-surface-variant hover:bg-surface-container-high'
              }`}
            >
              <span className="material-symbols-outlined mr-3">{tab.icon}</span>
              <span className="font-label-md text-label-md">{tab.label}</span>
            </div>
          ))}
        </nav>

        <div className="border-t border-outline-variant pt-md flex flex-col gap-1">
          <div className="group flex items-center px-4 py-3 cursor-pointer text-on-surface-variant hover:bg-surface-container-high transition-all duration-200 rounded-lg">
            <span className="material-symbols-outlined mr-3">settings</span>
            <span className="font-label-md text-label-md">Settings</span>
          </div>
          <div className="group flex items-center px-4 py-3 cursor-pointer text-on-surface-variant hover:bg-surface-container-high transition-all duration-200 rounded-lg">
            <span className="material-symbols-outlined mr-3">contact_support</span>
            <span className="font-label-md text-label-md">Support</span>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-grow overflow-y-auto bg-surface flex flex-col">
        {/* TopAppBar */}
        <header className="flex justify-between items-center w-full px-gutter h-16 sticky top-0 bg-surface/70 backdrop-blur-md border-b border-outline-variant z-40">
          <div className="flex items-center gap-base">
            <span className="md:hidden material-symbols-outlined text-primary cursor-pointer">menu</span>
            <h2 className="font-headline-md text-headline-md font-bold text-primary">AeroTalent AI</h2>
          </div>
          <div className="hidden lg:flex items-center bg-surface-container-low border border-outline-variant rounded-full px-4 py-1.5 w-96">
            <span className="material-symbols-outlined text-outline text-sm mr-2">search</span>
            <input
              className="bg-transparent border-none focus:ring-0 text-sm w-full p-0 placeholder:text-outline focus:outline-none"
              placeholder="Search candidates, roles, or insights..."
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="flex items-center gap-md">
            <button className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-high p-2 rounded-full transition-colors">
              notifications
            </button>
            <button className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-high p-2 rounded-full transition-colors">
              help
            </button>
            <button className="material-symbols-outlined text-on-surface-variant hover:bg-surface-container-high p-2 rounded-full transition-colors">
              settings
            </button>
            <div className="h-10 w-10 rounded-full overflow-hidden border-2 border-primary-fixed cursor-pointer">
              <img
                alt="User profile representation"
                className="w-full h-full object-cover"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuDG4rKLGdbi-w3bOQbErBy_o3A6PnG4rT2pyZi-krDngQMs9UeAua7zlQPzUDWs2o7dA943McI1BJIfBXC2MLdx1IYd7RNloo6gvLSBZXPBewYKPvCV61oZJlb477Xk8I3SB-7rzsYaAxjz9c0hzu-x4p7DlM3Ds2BpxmMhtQi9_QH7_KMdk9lpXz_RN4EvpPDj6iwJ76Sc9-jxUiohd_cTHNviOIRTKLpoEY_4YPLhGHFILsAHQ-jL7buwTyy6aryxzinC7s_wJSw"
              />
            </div>
          </div>
        </header>

        {/* Dashboard Panels */}
        <div className="max-w-container-max mx-auto p-gutter space-y-lg w-full flex-grow">
          {/* API Health Banner */}
          {systemInfo && (
            <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs rounded-xl flex items-center gap-2">
              <span className="material-symbols-outlined text-[16px] animate-pulse">cloud_done</span>
              <span>FastAPI Database Connection Online. Schema status active.</span>
            </div>
          )}

          {/* Welcome Section */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-md">
            <div>
              <h3 className="font-headline-lg text-headline-lg text-primary font-bold">Recruitment Overview</h3>
              <p className="text-on-surface-variant font-body-md">Precision talent sourcing powered by AI. Here's what's happening today.</p>
            </div>
            <div className="flex items-center gap-sm">
              <div className="flex -space-x-2">
                <img
                  className="w-8 h-8 rounded-full border-2 border-white object-cover"
                  alt="Recruiter 1"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuDLNRsBlnX2bgPGYV9atvDhRB4ei3mWcxh5Vn4b5qx8br91QtEsvAR1CbQBg7stDbutMmfnQW8BpzN1cFeVqtz3c_KNGQ5HWT1YeNfIvJRd_bVAgN_K2YZOV0eei1Qz6w7otVYmoqoCe4SCE5Pm2LoydsOSaf1o8VCv4BPxt0tbXMFdfQtyoQtHTBYKl8NRtKbhdzKn6MZe_ChISKLJyjdmRpEhxYnCuKLZSWNguVPo9QMXNUgjBONo96-sJzDgD-sXxrte5UI9AkY"
                />
                <img
                  className="w-8 h-8 rounded-full border-2 border-white object-cover"
                  alt="Recruiter 2"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuDc7npKj8vJallGVu7Sk5evE8SEIB9JfREK46333dhsLb6F0BXxev130dWsupE1Fn5e4ogm4xqdETtzvMhDnvV9x6grsUzhqC1CT-co2ZCBIV7ZQV4qigL2Dtfy6A_bOxhwq8zzGkyOVeCQvOUh90UnszdXCy9253HBPO0pqQ4YYlJ94HDorAgSWf-YcsoR8gynr-Cnm67nV2m2SK9ImdD0l3ChB-u13jx63iRLMXa6ERqlzpGC39QCAZQl8ljNMMZPb1HnUa6OBpQ"
                />
                <div className="w-8 h-8 rounded-full bg-secondary-container flex items-center justify-center text-[10px] font-bold border-2 border-white">
                  +12
                </div>
              </div>
              <span className="text-xs text-on-surface-variant font-label-sm">Active recruiters online</span>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-md">
            {/* Stat Card 1 */}
            <Card hoverEffect className="relative group">
              <div className="flex justify-between items-start mb-sm">
                <div className="p-2 bg-primary-container rounded-lg flex items-center justify-center">
                  <span className="material-symbols-outlined text-white" style={{ fontVariationSettings: "'FILL' 1" }}>
                    groups
                  </span>
                </div>
                <span className="text-on-tertiary-container font-label-sm flex items-center">
                  <span className="material-symbols-outlined text-xs mr-1">trending_up</span> +12%
                </span>
              </div>
              <p className="text-on-surface-variant font-label-md">Total Candidates</p>
              <h4 className="text-headline-lg font-display-lg text-primary font-bold">1,482</h4>
              <div className="w-full bg-surface-container-high h-1 mt-md rounded-full overflow-hidden">
                <div className="bg-primary h-full w-3/4"></div>
              </div>
            </Card>

            {/* Stat Card 2 */}
            <Card hoverEffect>
              <div className="flex justify-between items-start mb-sm">
                <div className="p-2 bg-secondary-container rounded-lg flex items-center justify-center">
                  <span className="material-symbols-outlined text-on-secondary-container" style={{ fontVariationSettings: "'FILL' 1" }}>
                    work
                  </span>
                </div>
                <span className="text-on-surface-variant font-label-sm">Updated 2h ago</span>
              </div>
              <p className="text-on-surface-variant font-label-md">Active Jobs</p>
              <h4 className="text-headline-lg font-display-lg text-primary font-bold">24</h4>
              <div className="flex gap-1 mt-md">
                <div className="h-2 w-full bg-on-tertiary-container rounded-full"></div>
                <div className="h-2 w-full bg-on-tertiary-container rounded-full opacity-50"></div>
                <div className="h-2 w-full bg-surface-container-high rounded-full"></div>
              </div>
            </Card>

            {/* Stat Card 3 */}
            <Card hoverEffect className="border-l-4 border-l-on-tertiary-container">
              <div className="flex justify-between items-start mb-sm">
                <div className="p-2 bg-tertiary-fixed rounded-lg flex items-center justify-center">
                  <span className="material-symbols-outlined text-on-tertiary-fixed" style={{ fontVariationSettings: "'FILL' 1" }}>
                    bolt
                  </span>
                </div>
                <div className="bg-tertiary-fixed-dim/20 text-on-tertiary-fixed-variant px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider">
                  AI Insight
                </div>
              </div>
              <p className="text-on-surface-variant font-label-md">AI Match Rate</p>
              <h4 className="text-headline-lg font-display-lg text-primary font-bold">
                87.4<span className="text-lg">%</span>
              </h4>
              <p className="text-[11px] text-on-tertiary-fixed-variant mt-md">Matched across 4 priority roles</p>
            </Card>

            {/* Stat Card 4 */}
            <Card hoverEffect>
              <div className="flex justify-between items-start mb-sm">
                <div className="p-2 bg-surface-container-highest rounded-lg flex items-center justify-center">
                  <span className="material-symbols-outlined text-on-surface-variant" style={{ fontVariationSettings: "'FILL' 1" }}>
                    calendar_month
                  </span>
                </div>
              </div>
              <p className="text-on-surface-variant font-label-md">Interviews This Week</p>
              <h4 className="text-headline-lg font-display-lg text-primary font-bold">18</h4>
              <div className="flex items-center gap-2 mt-md">
                <div className="flex -space-x-1">
                  <div className="w-5 h-5 rounded-full bg-primary-fixed-dim border border-white"></div>
                  <div className="w-5 h-5 rounded-full bg-secondary-fixed-dim border border-white"></div>
                  <div className="w-5 h-5 rounded-full bg-tertiary-fixed-dim border border-white"></div>
                </div>
                <span className="text-[11px] font-medium text-on-surface-variant">Scheduled Today: 4</span>
              </div>
            </Card>
          </div>

          {/* Analytics Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-md">
            {/* ATS Score Timeline (Area Chart) */}
            <Card className="p-md h-80 flex flex-col justify-between">
              <h5 className="font-label-md text-primary uppercase tracking-wider font-semibold mb-sm">ATS Score Trend</h5>
              <div className="w-full h-60">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={analytics.ats_score_history} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#4f46e5" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                    <XAxis dataKey="date" stroke="#94a3b8" fontSize={11} tickLine={false} />
                    <YAxis domain={[0, 100]} stroke="#94a3b8" fontSize={11} tickLine={false} axisLine={false} />
                    <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #cbd5e1' }} />
                    <Area type="monotone" dataKey="score" stroke="#4f46e5" fillOpacity={1} fill="url(#colorScore)" strokeWidth={2} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </Card>

            {/* JD Match History (Bar Chart) */}
            <Card className="p-md h-80 flex flex-col justify-between">
              <h5 className="font-label-md text-primary uppercase tracking-wider font-semibold mb-sm">Role Matching Analysis</h5>
              <div className="w-full h-60">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={analytics.jd_match_history} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                    <XAxis dataKey="role" stroke="#94a3b8" fontSize={11} tickLine={false} />
                    <YAxis domain={[0, 100]} stroke="#94a3b8" fontSize={11} tickLine={false} axisLine={false} />
                    <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #cbd5e1' }} />
                    <Bar dataKey="score" fill="#10b981" radius={[4, 4, 0, 0]} barSize={30} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>

            {/* Skill Gaps (Bar Chart) */}
            <Card className="p-md h-80 flex flex-col justify-between">
              <h5 className="font-label-md text-primary uppercase tracking-wider font-semibold mb-sm">Identified Skill Gaps</h5>
              <div className="w-full h-60">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={analytics.skill_gaps} layout="vertical" margin={{ top: 10, right: 30, left: 20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
                    <XAxis type="number" stroke="#94a3b8" fontSize={11} tickLine={false} />
                    <YAxis dataKey="skill" type="category" stroke="#94a3b8" fontSize={11} tickLine={false} axisLine={false} />
                    <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #cbd5e1' }} />
                    <Bar dataKey="frequency" fill="#f59e0b" radius={[0, 4, 4, 0]} barSize={15} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>

            {/* Agent Scores (Radar Chart) */}
            <Card className="p-md h-80 flex flex-col justify-between">
              <h5 className="font-label-md text-primary uppercase tracking-wider font-semibold mb-sm">Multi-Agent Performance</h5>
              <div className="w-full h-60">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="75%" data={analytics.agent_scores}>
                    <PolarGrid stroke="#e2e8f0" />
                    <PolarAngleAxis dataKey="agent" stroke="#94a3b8" fontSize={11} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#cbd5e1" fontSize={9} />
                    <Radar name="Agent Rating" dataKey="score" stroke="#6366f1" fill="#6366f1" fillOpacity={0.3} />
                    <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #cbd5e1' }} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </div>

          {/* Bento Grid Content */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-md items-start">
            {/* Top Candidates Table (Col 1-8) */}
            <section className="lg:col-span-8 bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden">
              <div className="px-gutter py-md border-b border-outline-variant flex justify-between items-center bg-surface-bright">
                <h5 className="font-headline-md text-primary font-bold">Top AI-Matched Candidates</h5>
                <button className="text-primary font-label-md flex items-center hover:underline">
                  View All Candidates <span className="material-symbols-outlined text-sm ml-1">arrow_forward</span>
                </button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead className="bg-surface-container-low">
                    <tr>
                      <th className="px-6 py-4 font-label-md text-on-surface-variant">Candidate</th>
                      <th className="px-6 py-4 font-label-md text-on-surface-variant">Target Role</th>
                      <th className="px-6 py-4 font-label-md text-on-surface-variant">Match Score</th>
                      <th className="px-6 py-4 font-label-md text-on-surface-variant">Status</th>
                      <th className="px-6 py-4"></th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-outline-variant">
                    {filteredCandidates.map((c) => (
                      <tr key={c.id} className="hover:bg-surface-container transition-colors group">
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-sm">
                            <img className="w-10 h-10 rounded-lg object-cover flex-shrink-0" alt={c.name} src={c.avatar} />
                            <div>
                              <p className="font-label-md text-primary font-bold">{c.name}</p>
                              <p className="text-xs text-on-surface-variant">{c.role}</p>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-on-surface">{c.targetRole}</td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2">
                            <span className="w-12 h-6 flex items-center justify-center bg-tertiary-fixed-dim/30 text-on-tertiary-fixed-variant font-bold text-xs rounded-full flex-shrink-0">
                              {c.matchScore}%
                            </span>
                            <div className="flex gap-0.5">
                              {Array.from({ length: 5 }).map((_, i) => (
                                <div
                                  key={i}
                                  className={`w-1 h-3 rounded-full ${
                                    i < Math.round(c.matchScore / 20)
                                      ? 'bg-on-tertiary-container'
                                      : 'bg-outline-variant'
                                  }`}
                                />
                              ))}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <span
                            className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${
                              c.status === 'Interviewing'
                                ? 'bg-secondary-container text-on-secondary-container'
                                : c.status === 'Offer Sent'
                                ? 'bg-on-tertiary-container text-white'
                                : 'bg-surface-container-highest text-on-surface-variant'
                            }`}
                          >
                            {c.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <button className="material-symbols-outlined text-outline hover:text-primary transition-colors">
                            more_vert
                          </button>
                        </td>
                      </tr>
                    ))}
                    {filteredCandidates.length === 0 && (
                      <tr>
                        <td colSpan={5} className="px-6 py-8 text-center text-on-surface-variant text-sm">
                          No matching candidates found.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
              <div className="p-4 bg-surface-container-low flex justify-center">
                <button className="text-sm font-label-md text-on-surface-variant hover:text-primary font-bold">
                  Load more candidates...
                </button>
              </div>
            </section>

            {/* Sidebar Widgets (Col 9-12) */}
            <div className="lg:col-span-4 space-y-md w-full">
              {/* Upcoming Interviews */}
              <div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-md text-left">
                <div className="flex justify-between items-center mb-md">
                  <h6 className="font-label-md text-primary uppercase tracking-wider font-semibold">Interviews Today</h6>
                  <span className="material-symbols-outlined text-outline cursor-pointer hover:text-primary">
                    event_note
                  </span>
                </div>
                <div className="space-y-4">
                  <div className="flex items-center gap-md border-l-4 border-primary pl-3 py-1">
                    <div className="flex-shrink-0">
                      <p className="font-bold text-primary text-base">09:30</p>
                      <p className="text-[10px] text-on-surface-variant uppercase font-semibold">AM</p>
                    </div>
                    <div className="overflow-hidden">
                      <p className="font-label-md text-on-surface truncate font-semibold">Sarah Chen - Technical Round</p>
                      <p className="text-[11px] text-on-surface-variant">Zoom Meeting • ID: 892-021</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-md border-l-4 border-tertiary pl-3 py-1">
                    <div className="flex-shrink-0">
                      <p className="font-bold text-primary text-base">11:00</p>
                      <p className="text-[10px] text-on-surface-variant uppercase font-semibold">AM</p>
                    </div>
                    <div className="overflow-hidden">
                      <p className="font-label-md text-on-surface truncate font-semibold">Marcus Holloway - Culture Fit</p>
                      <p className="text-[11px] text-on-surface-variant">Office Room 4B • In-Person</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-md border-l-4 border-outline pl-3 py-1 opacity-60">
                    <div className="flex-shrink-0">
                      <p className="font-bold text-primary text-base">02:00</p>
                      <p className="text-[10px] text-on-surface-variant uppercase font-semibold">PM</p>
                    </div>
                    <div className="overflow-hidden">
                      <p className="font-label-md text-on-surface truncate font-semibold">JD Matcher Training</p>
                      <p className="text-[11px] text-on-surface-variant">Internal Team Session</p>
                    </div>
                  </div>
                </div>
                <button className="w-full mt-md py-2 border border-outline-variant rounded-lg font-label-md text-on-surface-variant hover:bg-surface-container-high transition-all text-xs font-semibold">
                  View Full Calendar
                </button>
              </div>

              {/* Recent Activity Feed */}
              <div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-md text-left">
                <h6 className="font-label-md text-primary uppercase tracking-wider mb-md font-semibold">Recent Activity</h6>
                <div className="space-y-6 relative before:absolute before:left-2 before:top-2 before:bottom-2 before:w-px before:bg-outline-variant text-sm">
                  <div className="relative pl-7">
                    <div className="absolute left-0 top-1 w-4 h-4 rounded-full bg-on-tertiary-container border-4 border-surface shadow-sm"></div>
                    <p className="text-on-surface">
                      <span className="font-bold">AI Matched</span> Sarah Chen to VP role
                    </p>
                    <p className="text-[11px] text-on-surface-variant">2 mins ago</p>
                  </div>
                  <div className="relative pl-7">
                    <div className="absolute left-0 top-1 w-4 h-4 rounded-full bg-primary border-4 border-surface shadow-sm"></div>
                    <p className="text-on-surface">
                      <span className="font-bold">James L.</span> updated hiring pipeline
                    </p>
                    <p className="text-[11px] text-on-surface-variant">45 mins ago</p>
                  </div>
                  <div className="relative pl-7">
                    <div className="absolute left-0 top-1 w-4 h-4 rounded-full bg-secondary border-4 border-surface shadow-sm"></div>
                    <p className="text-on-surface">
                      <span className="font-bold">Resume Uploaded</span> for Data Analyst
                    </p>
                    <p className="text-[11px] text-on-surface-variant">2 hours ago</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-auto py-lg bg-surface-bright border-t border-outline-variant w-full">
          <div className="max-w-container-max mx-auto px-gutter flex flex-col md:flex-row justify-between items-center gap-md">
            <div className="flex items-center gap-sm">
              <span className="font-label-md text-label-md font-bold text-primary">AeroTalent AI</span>
              <span className="text-on-surface-variant text-xs font-body-sm">| Precision Recruiting.</span>
            </div>
            <p className="font-label-sm text-label-sm text-on-surface-variant">© 2024 AeroTalent AI. All rights reserved.</p>
          </div>
        </footer>
      </main>

      {/* Floating Action AI Assistant Button */}
      <button className="fixed bottom-8 right-8 w-14 h-14 bg-on-tertiary-container text-white rounded-full flex items-center justify-center shadow-lg hover:scale-110 transition-transform z-50 group">
        <span className="material-symbols-outlined group-hover:hidden" style={{ fontVariationSettings: "'FILL' 1" }}>
          smart_toy
        </span>
        <span className="hidden group-hover:block font-bold text-xs">AI HELP</span>
      </button>

      {/* New Analysis / Upload Resume Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl border border-outline-variant max-w-md w-full shadow-2xl overflow-hidden p-6 relative text-left">
            <button
              onClick={() => setIsModalOpen(false)}
              className="absolute top-4 right-4 text-on-surface-variant hover:text-primary material-symbols-outlined"
            >
              close
            </button>
            <h3 className="text-xl font-bold text-primary mb-4">Analyze Candidate Resume</h3>
            <form onSubmit={handleAddNewCandidate} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase text-on-surface-variant mb-1">Candidate Name</label>
                <input
                  required
                  type="text"
                  className="w-full border border-outline-variant rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-primary"
                  placeholder="e.g. Elena Rodriguez"
                  value={newCandidate.name}
                  onChange={(e) => setNewCandidate({ ...newCandidate, name: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase text-on-surface-variant mb-1">Current Role</label>
                <input
                  required
                  type="text"
                  className="w-full border border-outline-variant rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-primary"
                  placeholder="e.g. Lead ML Architect"
                  value={newCandidate.role}
                  onChange={(e) => setNewCandidate({ ...newCandidate, role: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase text-on-surface-variant mb-1">Target Position</label>
                <input
                  required
                  type="text"
                  className="w-full border border-outline-variant rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-primary"
                  placeholder="e.g. Director of Engineering"
                  value={newCandidate.targetRole}
                  onChange={(e) => setNewCandidate({ ...newCandidate, targetRole: e.target.value })}
                />
              </div>
              <div className="pt-2 flex justify-end gap-sm">
                <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>
                  Cancel
                </Button>
                <Button variant="ai" type="submit">
                  Upload & Analyze
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
