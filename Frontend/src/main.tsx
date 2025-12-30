import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import "./styles/index.css";
import { AuthProvider } from "./context/AuthContext";
import { LoginPage } from "./pages/LoginPage";
import { ProfilePage } from "./pages/ProfilePage";
import { InterviewPage } from "./pages/InterviewPage";
import { ResultsPage } from "./pages/ResultsPage";
import { CodingDashboardPage } from "./pages/CodingDashboardPage";
import { CommunityDashboardPage } from "./pages/CommunityDashboardPage";

createRoot(document.getElementById("root")!).render(
  <BrowserRouter>
    <AuthProvider>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/interview" element={<InterviewPage />} />
        <Route path="/results/:interviewId" element={<ResultsPage />} />
        <Route path="/coding" element={<CodingDashboardPage />} />
        <Route path="/community" element={<CommunityDashboardPage />} />
      </Routes>
    </AuthProvider>
  </BrowserRouter>,
);