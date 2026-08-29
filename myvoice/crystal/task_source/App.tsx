import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import Home from "@/pages/Home";
import Shop from "@/pages/Shop";
import Profile from "@/pages/Profile";
import MissionList from "@/pages/mission/MissionList";
import MissionDetail from "@/pages/mission/MissionDetail";
import MissionPlay from "@/pages/mission/MissionPlay";
import MissionResult from "@/pages/mission/MissionResult";
import VocabularyList from "@/pages/vocabulary/VocabularyList";
import VocabularyLearning from "@/pages/vocabulary/VocabularyLearning";
import VocabularyResult from "@/pages/vocabulary/VocabularyResult";
import Skills from "@/pages/Skills";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import ProtectedRoute from "./components/ProtectedRoute";
function Router() {
  // All routes require authentication
  return (
    <ProtectedRoute>
      <Switch>
      <Route path={"/"} component={Home} />
      <Route path={"/home"} component={Home} />
      <Route path={"/missions"} component={MissionList} />
      <Route path={"/mission/:id"} component={MissionDetail} />
      <Route path={"/mission/:id/play"} component={MissionPlay} />
      <Route path={"/mission/:id/result"} component={MissionResult} />
      <Route path={"/vocabulary"} component={VocabularyList} />
      <Route path={"/vocabulary/:category/result"} component={VocabularyResult} />
      <Route path={"/vocabulary/:category"} component={VocabularyLearning} />
      <Route path={"/shop"} component={Shop} />
      <Route path={"/profile"} component={Profile} />
      <Route path={"/skills"} component={Skills} />
      <Route path={"/404"} component={NotFound} />
      <Route component={NotFound} />
    </Switch>
    </ProtectedRoute>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="light">
        <TooltipProvider>
          <Toaster />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
