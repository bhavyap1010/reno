import React from "react";
import GoogleSignInButton from "./GoogleSignInButton";
import "../styles/social.css";

const SocialLogin = ({ setIsAuthenticated }) => {
    return (
        <div className="social-login">
            <GoogleSignInButton setIsAuthenticated={setIsAuthenticated} />
        </div>
    );
};

export default SocialLogin;
