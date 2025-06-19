import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/auth.css";

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
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (formData.password !== formData.password2) {
            setErrors({ ...errors, password2: "Passwords don't match" });
            return;
        }

        try {
            const response = await api.post("accounts/register/", formData);
            localStorage.setItem("token", response.data.token);
            setIsAuthenticated(true);
            navigate("/home");
        } catch (err) {
            if (err.response?.data) {
                setErrors(err.response.data);
            }
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <h2 className="auth-title">Register</h2>
                {errors.non_field_errors && (
                    <div className="auth-error">{errors.non_field_errors}</div>
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
                            required
                        />
                        {errors.username && (
                            <span className="error-text">
                                {errors.username}
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
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="last_name">Last Name</label>
                        <input
                            type="text"
                            id="last_name"
                            name="last_name"
                            value={formData.last_name}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                        />
                        {errors.email && (
                            <span className="error-text">{errors.email}</span>
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
                                />
                                Business
                            </label>
                        </div>
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                        />
                        {errors.password && (
                            <span className="error-text">
                                {errors.password}
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
                            required
                        />
                        {errors.password2 && (
                            <span className="error-text">
                                {errors.password2}
                            </span>
                        )}
                    </div>

                    <button type="submit" className="auth-button">
                        Register
                    </button>
                </form>
                <p className="auth-footer">
                    Already have an account? <a href="/login">Login here</a>
                </p>
            </div>
        </div>
    );
};

export default Register;
