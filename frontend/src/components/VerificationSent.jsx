import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/verification.css";

const VerificationSent = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const email = location.state?.email || "your email";
    const [isResending, setIsResending] = useState(false);
    const [resendStatus, setResendStatus] = useState(null);

    const handleResend = async () => {
        setIsResending(true);
        setResendStatus(null);

        try {
            const response = await api.post("accounts/resend-verification/", {
                email,
            });

            if (response.data.detail) {
                setResendStatus({
                    type: "success",
                    message: response.data.detail,
                });
            } else {
                setResendStatus({
                    type: "error",
                    message: "Unexpected response from server",
                });
            }
        } catch (err) {
            let errorMessage = "Failed to resend verification email";

            if (err.response) {
                // Handle specific error cases
                if (err.response.status === 404) {
                    errorMessage =
                        "No unverified user found with this email. Please register again.";
                } else if (err.response.data && err.response.data.error) {
                    errorMessage = err.response.data.error;
                } else if (err.response.status === 400) {
                    errorMessage = "Invalid request. Please try again.";
                }
            }

            setResendStatus({
                type: "error",
                message: errorMessage,
            });
        } finally {
            setIsResending(false);
        }
    };

    return (
        <div className="verification-container">
            <div className="verification-card">
                <h2>Email Verification Sent</h2>
                <div className="verification-message">
                    <p>
                        We've sent a verification email to{" "}
                        <strong>{email}</strong>.
                    </p>
                    <p>
                        Please check your inbox and click the verification link
                        to activate your account.
                    </p>
                    <p>Didn't receive the email?</p>

                    <button
                        onClick={handleResend}
                        className="resend-button"
                        disabled={isResending}
                    >
                        {isResending
                            ? "Sending..."
                            : "Resend Verification Email"}
                    </button>

                    {resendStatus && (
                        <div className={`resend-status ${resendStatus.type}`}>
                            {resendStatus.message}
                        </div>
                    )}

                    <p className="support-text">
                        If you're still having trouble, please contact support
                        at
                        <a href="mailto:support@example.com">
                            {" "}
                            support@example.com
                        </a>
                    </p>

                    <button
                        className="auth-button secondary"
                        onClick={() => navigate("/register")}
                    >
                        Register Again
                    </button>
                </div>
            </div>
        </div>
    );
};

export default VerificationSent;
