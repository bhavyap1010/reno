import React from "react";
import "../styles/home.css";

const Home = ({ isAuthenticated }) => {
    return (
        <div className="home-container">
            <h1 className="home-title">Welcome to Your Dashboard</h1>
            <div className="home-content">
                {isAuthenticated ? (
                    <div className="welcome-message">
                        <p>You are successfully logged in!</p>
                        <p>Explore the features of your account.</p>
                    </div>
                ) : (
                    <div className="welcome-message">
                        <p>
                            Please login or register to access your dashboard.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Home;
