import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { ErrorBoundary } from "@/components/ErrorBoundary";

// Eagerly loaded (auth-critical, tiny)
import Intro from './pages/Intro';
import Landing from './pages/Landing';
import KidLayout from './components/layout/KidLayout';
import KidProtectedRoute from './guards/KidProtectedRoute';
import ParentProtectedRoute from './guards/ParentProtectedRoute';

// Lazy-loaded Auth / Onboarding
const Splash = lazy(() => import('./pages/Splash'));
const Login = lazy(() => import('./pages/Login'));
const Signup = lazy(() => import('./pages/Signup'));
const VerifyEmail = lazy(() => import('./pages/VerifyEmail'));
const ForgotPassword = lazy(() => import('./pages/ForgotPassword'));
const SelectChild = lazy(() => import('./pages/SelectChild'));
const OnboardingSetup = lazy(() => import('./pages/onboarding/OnboardingSetup'));
const ChildInfoInput = lazy(() => import('./pages/onboarding/ChildInfoInput'));
const SubscriptionSelect = lazy(() => import('./pages/onboarding/SubscriptionSelect'));
const ModeSelection = lazy(() => import('./pages/ModeSelection'));

// Lazy-loaded Kid Pages
const KidHome = lazy(() => import('./pages/kid/KidHome'));
const Adventures = lazy(() => import('./pages/kid/Adventures'));
const AdventureDetail = lazy(() => import('./pages/kid/AdventureDetail'));
const AdventurePlay = lazy(() => import('./pages/kid/AdventurePlay'));
const AdventureResult = lazy(() => import('./pages/kid/AdventureResult'));
const Vocabulary = lazy(() => import('./pages/kid/Vocabulary'));
const VocabularyLearning = lazy(() => import('./pages/kid/VocabularyLearning'));
const VocabularyResult = lazy(() => import('./pages/kid/VocabularyResult'));
const KidShop = lazy(() => import('./pages/kid/KidShop'));
const KidProfile = lazy(() => import('./pages/kid/KidProfile'));
const KidSkills = lazy(() => import('./pages/kid/KidSkills'));

// Lazy-loaded Parent Pages
const ParentLayout = lazy(() => import('./components/layout/ParentLayout'));
const ParentHome = lazy(() => import('./pages/parent/ParentHome'));
const LearningDashboard = lazy(() => import('./pages/parent/LearningDashboard'));
const Dashboard = lazy(() => import('./pages/parent/Dashboard'));
const ReportDetail = lazy(() => import('./pages/parent/ReportDetail'));
const SkillDeepReport = lazy(() => import('./pages/parent/SkillDeepReport'));
const EditChild = lazy(() => import('./pages/parent/EditChild'));
const ConversationInsights = lazy(() => import('./pages/parent/ConversationInsights'));
const RecommendationsSettings = lazy(() => import('./pages/parent/RecommendationsSettings'));

function PageFallback() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-8 h-8 border-4 border-[var(--bt-primary)] border-t-transparent rounded-full animate-spin" />
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary scope="Global">
      <Suspense fallback={<PageFallback />}>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Intro />} />
          <Route path="/landing" element={<Landing />} />
          <Route path="/splash" element={<Splash />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/verify-email" element={<VerifyEmail />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />

          {/* Onboarding */}
          <Route path="/onboarding/setup" element={<OnboardingSetup />} />
          <Route path="/onboarding/child-info" element={<ChildInfoInput />} />
          <Route path="/onboarding/subscription" element={<SubscriptionSelect />} />

          {/* Legacy redirect */}
          <Route path="/select-child" element={<SelectChild />} />

          {/* Mode Selection (parent auth required) */}
          <Route element={<ParentProtectedRoute />}>
            <Route path="/mode-select" element={<ModeSelection />} />
          </Route>

          {/* Kids View */}
          <Route element={<KidProtectedRoute />}>
            <Route path="/kid" element={<KidLayout />}>
              <Route path="home" element={<KidHome />} />
              <Route path="adventures" element={<Adventures />} />
              <Route path="vocabulary" element={<Vocabulary />} />
              <Route path="shop" element={<KidShop />} />
              <Route path="profile" element={<KidProfile />} />
              <Route path="skills" element={<KidSkills />} />
            </Route>

            {/* Full-screen pages (no BottomNav) */}
            <Route path="/kid/adventure/:id" element={<AdventureDetail />} />
            <Route path="/kid/adventure/:id/play" element={
              <ErrorBoundary scope="AdventurePlay">
                <AdventurePlay />
              </ErrorBoundary>
            } />
            <Route path="/kid/adventure/:id/result" element={<AdventureResult />} />
            <Route path="/kid/vocabulary/:category" element={<VocabularyLearning />} />
            <Route path="/kid/vocabulary/:category/result" element={<VocabularyResult />} />
          </Route>

          {/* Parent View — with bottom tab layout */}
          <Route element={<ParentProtectedRoute />}>
            <Route path="/parent" element={<ParentLayout />}>
              <Route path="home" element={<ParentHome />} />
              <Route path="progress" element={<LearningDashboard />} />
              <Route path="insights" element={<ConversationInsights />} />
              <Route path="settings" element={<RecommendationsSettings />} />
              <Route path="dashboard" element={<Dashboard />} />
            </Route>

            {/* Full-screen parent pages (no bottom tabs) */}
            <Route path="/parent/reports/:reportId" element={<ReportDetail />} />
            <Route path="/parent/reports/:reportId/skill/:skillId" element={<SkillDeepReport />} />
            <Route path="/parent/children/:childId" element={<EditChild />} />
          </Route>
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
}

export default App;
