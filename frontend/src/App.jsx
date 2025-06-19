import { useState, useEffect } from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Navigate,
} from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Home from "./components/Home";
import Navbar from "./components/Navbar";
import VerificationSent from "./components/VerificationSent";
import EmailVerification from "./components/EmailVerification";
import "./styles/auth.css";
import "./styles/home.css";
import "./styles/navbar.css";
import "./styles/social.css";
import "./styles/verification.css";
import api from "./api";

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Check authentication status on app load
    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem("token");
            if (!token) {
                setLoading(false);
                return;
            }

            try {
                // Verify token with backend
                const response = await api.get("accounts/user/");
                setUserData(response.data);
                setIsAuthenticated(true);
            } catch (err) {
                console.error("Authentication check failed:", err);
                if (err.response?.status === 401) {
                    // Token is invalid or expired
                    localStorage.removeItem("token");
                }
                setError("Failed to verify authentication. Please log in again.");
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, []);

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading...</p>
            </div>
        );
    }

    return (
        <Router>
            <Navbar
                isAuthenticated={isAuthenticated}
                userData={userData}
                setIsAuthenticated={setIsAuthenticated}
                setUserData={setUserData}
            />

            {error && (
                <div className="global-error">
                    {error}
                    <button onClick={() => setError(null)}>Dismiss</button>
                </div>
            )}

            <Routes>
                <Route
                    path="/login"
                    element={
                        !isAuthenticated ? (
                            <Login
                                setIsAuthenticated={setIsAuthenticated}
                                setUserData={setUserData}
                                setError={setError}
                            />
                        ) : (
                            <Navigate to="/home" />
                        )
                    }
                />
                <Route
                    path="/register"
                    element={
                        !isAuthenticated ? (
                            <Register
                                setIsAuthenticated={setIsAuthenticated}
                                setUserData={setUserData}
                            />
                        ) : (
                            <Navigate to="/home" />
                        )
                    }
                />
                <Route
                    path="/home"
                    element={
                        isAuthenticated ? (
                            <Home
                                isAuthenticated={isAuthenticated}
                                userData={userData}
                            />
                        ) : (
                            <Navigate to="/login" />
                        )
                    }
                />
                <Route
                    path="/verification-sent"
                    element={<VerificationSent />}
                />
                <Route
                    path="/verify-email/:token"
                    element={
                        <EmailVerification
                            setIsAuthenticated={setIsAuthenticated}
                            setUserData={setUserData}
                            setError={setError}
                        />
                    }
                />
                <Route
                    path="/"
                    element={
                        <Navigate to={isAuthenticated ? "/home" : "/login"} />
                    }
                />
                {/* Fallback route */}
                <Route path="*" element={<div>Page not found</div>} />
            </Routes>
        </Router>
    );
}

export default App;
