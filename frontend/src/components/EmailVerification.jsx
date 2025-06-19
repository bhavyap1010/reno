import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/verification.css";

const EmailVerification = ({ setIsAuthenticated, setUserData }) => {
    const { token } = useParams();
    const navigate = useNavigate();
    const [status, setStatus] = useState("verifying");
    const [message, setMessage] = useState("");
    const [user, setUser] = useState(null);

    useEffect(() => {
        const verifyEmail = async () => {
            try {
                const response = await api.get(`accounts/verify-email/${token}/`);

                // Save token and user data
                localStorage.setItem("token", response.data.token);
                setUser(response.data.user);
                setUserData(response.data.user);
                setIsAuthenticated(true);

                setStatus("success");
                setMessage("Email verified successfully! Redirecting to home page...");

                // Redirect after delay
                setTimeout(() => navigate("/home"), 3000);
            } catch (err) {
                setStatus("error");
                let errorMessage = "Email verification failed";

                // Provide more specific error messages
                if (err.response) {
                    if (err.response.data && err.response.data.error) {
                        errorMessage = err.response.data.error;
                    } else if (err.response.status === 400) {
                        errorMessage = "Invalid or expired verification token";
                    } else if (err.response.status === 404) {
                        errorMessage = "Verification token not found";
                    }
                }

                setMessage(errorMessage);
            }
        };

        verifyEmail();
    }, [token, navigate, setIsAuthenticated, setUserData]);

    return (
        <div className="verification-container">
            <div className="verification-card">
                <h2>Email Verification</h2>

                {status === "verifying" && (
                    <div className="verification-status">
                        <div className="spinner"></div>
                        <p>Verifying your email address...</p>
                    </div>
                )}

                {status === "success" && (
                    <div className="verification-success">
                        <div className="success-icon">✓</div>
                        <p>{message}</p>
                        {user && (
                            <p>
                                Welcome, {user.first_name} {user.last_name}!
                            </p>
                        )}
                    </div>
                )}

                {status === "error" && (
                    <div className="verification-error">
                        <div className="error-icon">✗</div>
                        <p>{message}</p>

                        <div className="action-buttons">
                            <button
                                onClick={() => navigate("/register")}
                                className="auth-button"
                            >
                                Register Again
                            </button>
                            <button
                                onClick={() => navigate("/login")}
                                className="auth-button secondary"
                            >
                                Go to Login
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default EmailVerification;