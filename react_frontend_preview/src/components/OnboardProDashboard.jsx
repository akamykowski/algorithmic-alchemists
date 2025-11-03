import React from 'react';

// Copied and adjusted from artifacts/OnboardProDashboard_Refactored.jsx
// Fixed PaletteIcon viewBox typo ("0 ġ 24 24" -> "0 0 24 24")

const LogoIcon = () => ( <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 12.6111L8.92308 17.5L20 6.5" stroke="#2563EB" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/></svg> );
const SearchIcon = () => ( <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg> );
const MoreHorizontalIcon = () => ( <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h.01M12 12h.01M19 12h.01" /></svg> );
const ChevronUpIcon = () => ( <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" /></svg> );
const RefreshIcon = () => ( <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h5M20 20v-5h-5M4 4a8 8 0 0114.24 4.76M20 20a8 8 0 01-14.24-4.76" /></svg> );
const PlusIcon = () => ( <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg> );
const BriefcaseIcon = () => <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>;
const CogIcon = () => <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>;
const MegaphoneIcon = () => <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-2.236 9.368-5.5" /></svg>;
const PaletteIcon = () => <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" /></svg>;
const FilterIcon = () => <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h18M7 12h10m-7 8h4" /></svg>;
const SortIcon = () => <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7h12M3 12h8m-8 5h5M17 4l4 4m0 0l-4 4m4-4H7" /></svg>;
const ExternalLinkIcon = () => <svg className="w-4 h-4 text-gray-500 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>;

const Card = ({ title, actions, children, className = '' }) => (
  <div className={`bg-white p-6 rounded-2xl shadow-sm ${className}`}>
    {(title || actions) && (
      <div className="flex items-center justify-between mb-4">
        {title && <h2 className="text-lg font-semibold">{title}</h2>}
        {actions && <div className="flex items-center space-x-2">{actions}</div>}
      </div>
    )}
    {children}
  </div>
);

const ActionButton = ({ children, icon, variant = 'secondary', className = '', ...rest }) => {
  const baseClasses = 'w-full flex items-center justify-center text-sm font-semibold py-2.5 px-4 rounded-lg transition';
  const variantClasses = {
    primary: 'text-white bg-green-500 hover:bg-green-600 shadow-sm',
    secondary: 'border border-slate-300 hover:bg-slate-100',
    tertiary: 'p-1 hover:bg-slate-100 rounded-full',
  };
  return (
    <button className={`${baseClasses} ${variantClasses[variant]} ${className}`} {...rest}>
      {icon}
      {children}
    </button>
  );
};

const Header = ({ user, navItems }) => (
  <header className="bg-white/80 backdrop-blur-md sticky top-0 z-20 border-b border-slate-200">
    <div className="max-w-screen-2xl mx-auto px-6 lg:px-8">
      <div className="flex items-center justify-between h-16">
        <div className="flex items-center space-x-8">
          <a href="#" className="flex items-center space-x-2" aria-label="OnboardPro Home">
            <LogoIcon />
            <span className="font-bold text-xl text-slate-800">OnboardPro</span>
          </a>
          <nav className="hidden md:flex items-center space-x-6">
            {navItems.map(item => (
              <a key={item} href="#" className={`text-sm font-medium transition-colors duration-200 ${item === 'Dashboard' ? 'text-blue-600' : 'text-slate-600 hover:text-blue-600'}`}>
                {item}
              </a>
            ))}
          </nav>
        </div>
        <div className="flex items-center space-x-4">
          <div className="relative hidden sm:block">
            <input type="search" placeholder="Search" className="pl-10 pr-4 py-2 w-48 border border-slate-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><SearchIcon /></div>
          </div>
          <div className="flex items-center space-x-3">
            <img src={user.avatar} alt={`${user.name} profile picture`} className="w-9 h-9 rounded-full object-cover" />
            <span className="text-sm font-medium hidden lg:block">{user.name}</span>
            <button aria-label="More options"><MoreHorizontalIcon /></button>
          </div>
        </div>
      </div>
    </div>
  </header>
);

const StatsCard = ({ title, value, valueColor = 'text-slate-800', icon }) => (
  <div className="bg-white/70 p-4 rounded-xl shadow-sm flex-1">
    <p className="text-sm text-slate-500">{title}</p>
    <div className="flex items-end justify-between mt-1">
      <span className={`text-3xl font-bold ${valueColor}`}>{value}</span>
      {icon}
    </div>
  </div>
);

const WelcomeBanner = ({ userName, stats }) => (
  <div className="bg-gradient-to-r from-blue-50 to-cyan-50 p-8 rounded-2xl mb-8 flex flex-wrap md:flex-nowrap items-center justify-between shadow-sm">
    <div>
      <h1 className="text-3xl font-bold text-slate-800">Welcome back, {userName}</h1>
      <p className="text-slate-500 mt-2">Streamline your employee onboarding experience</p>
    </div>
    <div className="flex items-center space-x-4 mt-6 md:mt-0 w-full md:w-auto">
      {stats.map(stat => <StatsCard key={stat.title} {...stat} />)}
    </div>
  </div>
);

const NewHireRow = ({ hire }) => {
  const isCompleted = hire.status === 'Completed';
  const progressColor = isCompleted ? 'bg-green-500' : 'bg-blue-500';
  const progressTextColor = isCompleted ? 'text-green-600' : 'text-blue-600';

  return (
    <div className="flex items-center space-x-4">
      <img src={hire.avatar} alt={`${hire.name} avatar`} className="w-12 h-12 rounded-full" />
      <div className="flex-1">
        <p className="font-semibold text-slate-700">{hire.name}</p>
        <p className="text-xs text-slate-400">{hire.date}</p>
      </div>
      <div className="w-1/3">
        <div className="flex justify-between items-center mb-1">
          <span className={`text-xs font-medium ${progressTextColor}`}>{hire.progress}%</span>
        </div>
        <div className="w-full bg-slate-200 rounded-full h-1.5">
          <div className={`${progressColor} h-1.5 rounded-full`} style={{ width: `${hire.progress}%` }}></div>
        </div>
      </div>
      {isCompleted ? (
        <button className="text-sm bg-green-100 text-green-700 font-semibold py-1.5 px-4 rounded-full hover:bg-green-200 transition">Complete</button>
      ) : (
        <button className="text-sm text-blue-600 font-semibold py-1.5 px-4 rounded-full border border-blue-200 hover:bg-blue-50 transition">View Profile</button>
      )}
    </div>
  );
};

const RecentNewHires = ({ hires }) => (
  <Card
    title="Recent New Hires"
    actions={
      <>
        <ActionButton variant="tertiary" aria-label="Filter"><FilterIcon/></ActionButton>
        <ActionButton variant="tertiary" aria-label="Sort"><SortIcon/></ActionButton>
      </>
    }
    className="xl:col-span-2"
  >
    <div className="space-y-4">
      {hires.map(hire => <NewHireRow key={hire.name} hire={hire} />)}
    </div>
  </Card>
);

const TemplateCard = ({ template }) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-800',
    green: 'bg-green-100 text-green-800',
  };
  return (
    <div className={`flex flex-col items-center justify-center p-4 rounded-xl text-center cursor-pointer transition-transform hover:scale-105 ${colorClasses[template.color]}`}>
      {template.icon}
      <span className={`mt-2 text-sm font-medium ${colorClasses[template.color]}`}>{template.name}</span>
    </div>
  );
};

const OnboardingTemplates = ({ templates }) => (
  <Card title="Onboarding Templates">
    <div className="grid grid-cols-2 gap-4 mb-4">
      {templates.map(template => <TemplateCard key={template.name} template={template} />)}
    </div>
    <ActionButton icon={<PlusIcon />}>Create New Template</ActionButton>
  </Card>
);

const TaskItem = ({ task }) => (
  <div className="flex items-center space-x-3 p-2 rounded-lg hover:bg-slate-50">
    <input type="checkbox" className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
    <div className="flex-1">
      <p className="font-medium text-slate-700">{task.title}</p>
      <p className="text-xs text-slate-400">{task.assignee}</p>
    </div>
    <div>
      {task.tags.map(tag => (
        <span key={tag} className={`text-xs font-semibold px-2.5 py-1 rounded-full ${tag === 'Urgent' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}`}>{tag}</span>
      ))}
    </div>
  </div>
);

const UpcomingTasks = ({ tasks }) => (
  <Card
    title="Upcoming Tasks"
    actions={
      <>
        <ActionButton variant="tertiary" aria-label="Filter"><FilterIcon/></ActionButton>
        <ActionButton variant="tertiary" aria-label="View All"><ExternalLinkIcon/></ActionButton>
      </>
    }
    className="xl:col-span-2"
  >
    <div className="space-y-3">
      {tasks.map(task => <TaskItem key={task.title} task={task} />)}
    </div>
  </Card>
);

const AnalyticsOverview = () => (
  <Card title="Analytics Overview">
    <div className="flex items-center justify-between">
      <div className="w-1/2 pr-4">
        <p className="text-sm font-medium text-slate-600 mb-2">Onboarding Completion Trends</p>
        <div className="space-y-4">
          <div className="h-20 flex items-end space-x-2">
            {[20, 45, 60, 30, 80, 50].map((h, i) => <div key={i} className="bg-blue-200 w-full rounded-t-sm" style={{height: `${h}%`}}></div>)}
          </div>
          <div className="h-20 flex items-end space-x-2">
            {[30, 55, 40, 70, 60, 90].map((h, i) => <div key={i} className="bg-green-200 w-full rounded-t-sm" style={{height: `${h}%`}}></div>)}
          </div>
        </div>
      </div>
      <div className="w-1/2 flex flex-col items-center">
        <p className="text-sm font-medium text-slate-600 mb-2">Overall Completion Rate</p>
        <div className="relative w-28 h-28 flex items-center justify-center">
          <svg className="w-full h-full" viewBox="0 0 36 36">
            <path className="text-slate-200" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" />
            <path className="text-blue-500" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" strokeDasharray="94, 100" strokeDashoffset="25" strokeLinecap="round" />
          </svg>
          <span className="absolute text-2xl font-bold text-slate-800">94%</span>
        </div>
        <p className="text-xs text-slate-400 mt-2">Class Most MMB</p>
      </div>
    </div>
  </Card>
);

const QuickActions = () => (
  <div className="sticky top-24">
    <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
    <div className="space-y-3">
      <ActionButton variant="primary" icon={<PlusIcon />}>Add New Hire</ActionButton>
      <ActionButton>Create Template</ActionButton>
      <ActionButton>Generate Report</ActionButton>
    </div>
  </div>
);

const OnboardProDashboard = () => {
  const user = { name: 'Maria S.', avatar: 'https://i.pravatar.cc/150?u=marias' };
  const navItems = ['Dashboard', 'New Hires', 'Templates', 'Reports', 'Settings'];

  const stats = [
    { title: 'Active New Hires', value: '5', valueColor: 'text-blue-600', icon: <ChevronUpIcon /> },
    { title: 'Pending Tasks', value: '12' },
    { title: 'Completion Rate', value: '94%', valueColor: 'text-green-600', icon: <RefreshIcon /> },
  ];

  const newHires = [
    { name: 'David Chen', date: '08/16/2024', progress: 75, status: 'In Progress', avatar: 'https://i.pravatar.cc/150?u=davidchen' },
    { name: 'Sarah Lee', date: '08/09/2024', progress: 100, status: 'Completed', avatar: 'https://i.pravatar.cc/150?u=sarahlee' },
    { name: 'Emily Davis', date: '05/19/2024', progress: 40, status: 'In Progress', avatar: 'https://i.pravatar.cc/150?u=emilydavis' },
  ];

  const upcomingTasks = [
    { title: 'Review IT Setup Checklist', assignee: 'Alice Johnson', date: 'Today', tags: ['Urgent'] },
    { title: 'Schedule Welcome Lunch', assignee: 'Fri, Mar 22', date: 'Fri, Mar 22', tags: ['Pending'] },
    { title: 'Assign Mentor', assignee: 'Mon, Mar 25', date: 'Mon, Mar 25', tags: ['Pending'] },
  ];

  const templates = [
    { name: 'Sales Department', icon: <BriefcaseIcon />, color: 'blue' },
    { name: 'Engineering Team', icon: <CogIcon />, color: 'green' },
    { name: 'Marketing & PR', icon: <MegaphoneIcon />, color: 'blue' },
    { name: 'Creative Services', icon: <PaletteIcon />, color: 'green' },
  ];

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800">
      <Header user={user} navItems={navItems} />
      <main className="max-w-screen-2xl mx-auto px-6 lg:px-8 py-8">
        <WelcomeBanner userName={user.name} stats={stats} />
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-9 grid grid-cols-1 xl:grid-cols-3 gap-8">
            <RecentNewHires hires={newHires} />
            <OnboardingTemplates templates={templates} />
            <UpcomingTasks tasks={upcomingTasks} />
            <AnalyticsOverview />
          </div>
          <div className="lg:col-span-3">
            <QuickActions />
          </div>
        </div>
      </main>
    </div>
  );
};

export default OnboardProDashboard;
