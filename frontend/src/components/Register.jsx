import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/auth.css";
import SocialLogin from "./SocialLogin";

const Register = ({ setIsAuthenticated }) => {
    const [formData, setFormData] = useState({
        username: "",
        first_name: "",
        last_name: "",
        email: "",
        account_type: "individual",
        password: "",
        password2: "",
    });
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        // Clear error for this field when user types
        if (errors[e.target.name]) {
            setErrors({ ...errors, [e.target.name]: null });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        setErrors({});

        // Client-side validation
        const newErrors = {};
        if (!formData.username.trim()) newErrors.username = 'Username is required';
        if (!formData.email.trim()) newErrors.email = 'Email is required';
        if (!formData.password) newErrors.password = 'Password is required';
        if (formData.password !== formData.password2) newErrors.password2 = "Passwords don't match";

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            setIsSubmitting(false);
            return;
        }

        try {
            // This should return a success message
            const response = await api.post("accounts/register/", formData);

            if (response.status === 201) {
                // Redirect to verification sent page with email
                navigate("/verification-sent", { state: { email: formData.email } });
            } else {
                setErrors({ non_field_errors: "Unexpected response from server. Please try again." });
            }
        } catch (err) {
            if (err.response) {
                // Handle Django validation errors
                if (err.response.data) {
                    setErrors(err.response.data);
                } else {
                    setErrors({ non_field_errors: "Registration failed. Please check your details." });
                }
            } else if (err.request) {
                setErrors({ non_field_errors: "Network error. Please check your connection." });
            } else {
                setErrors({ non_field_errors: "An unexpected error occurred." });
            }
            console.error("Registration error:", err);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <h2 className="auth-title">Register</h2>
                {errors.non_field_errors && (
                    <div className="auth-error">{Array.isArray(errors.non_field_errors)
                        ? errors.non_field_errors.join(" ")
                        : errors.non_field_errors}</div>
                )}
                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            disabled={isSubmitting}
                            required
                        />
                        {errors.username && (
                            <span className="error-text">
                                {Array.isArray(errors.username) ? errors.username.join(" ") : errors.username}
                            </span>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="first_name">First Name</label>
                        <input
                            type="text"
                            id="first_name"
                            name="first_name"
                            value={formData.first_name}
                            onChange={handleChange}
                            disabled={isSubmitting}
                            required
                        />
                        {errors.first_name && (
                            <span className="error-text">
                                {Array.isArray(errors.first_name) ? errors.first_name.join(" ") : errors.first_name}
                            </span>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="last_name">Last Name</label>
                        <input
                            type="text"
                            id="last_name"
                            name="last_name"
                            value={formData.last_name}
                            onChange={handleChange}
                            disabled={isSubmitting}
                            required
                        />
                        {errors.last_name && (
                            <span className="error-text">
                                {Array.isArray(errors.last_name) ? errors.last_name.join(" ") : errors.last_name}
                            </span>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            disabled={isSubmitting}
                            required
                        />
                        {errors.email && (
                            <span className="error-text">
                                {Array.isArray(errors.email) ? errors.email.join(" ") : errors.email}
                            </span>
                        )}
                    </div>

                    <div className="form-group">
                        <label>Account Type</label>
                        <div className="radio-group">
                            <label>
                                <input
                                    type="radio"
                                    name="account_type"
                                    value="individual"
                                    checked={
                                        formData.account_type === "individual"
                                    }
                                    onChange={handleChange}
                                    disabled={isSubmitting}
                                />
                                Individual
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    name="account_type"
                                    value="business"
                                    checked={
                                        formData.account_type === "business"
                                    }
                                    onChange={handleChange}
                                    disabled={isSubmitting}
                                />
                                Business
                            </label>
                        </div>
                        {errors.account_type && (
                            <span className="error-text">
                                {Array.isArray(errors.account_type) ? errors.account_type.join(" ") : errors.account_type}
                            </span>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            disabled={isSubmitting}
                            required
                        />
                        {errors.password && (
                            <span className="error-text">
                                {Array.isArray(errors.password) ? errors.password.join(" ") : errors.password}
                            </span>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="password2">Confirm Password</label>
                        <input
                            type="password"
                            id="password2"
                            name="password2"
                            value={formData.password2}
                            onChange={handleChange}
                            disabled={isSubmitting}
                            required
                        />
                        {errors.password2 && (
                            <span className="error-text">
                                {Array.isArray(errors.password2) ? errors.password2.join(" ") : errors.password2}
                            </span>
                        )}
                    </div>

                    <button
                        type="submit"
                        className="auth-button"
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? "Registering..." : "Register"}
                    </button>
                </form>

                {/* Add social login section */}
                <div className="social-section">
                    <div className="divider">OR</div>
                    <SocialLogin setIsAuthenticated={setIsAuthenticated} />
                </div>

                <p className="auth-footer">
                    Already have an account? <a href="/login">Login here</a>
                </p>
            </div>
        </div>
    );
};

export default Register;