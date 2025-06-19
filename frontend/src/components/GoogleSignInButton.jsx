import React, { useEffect, useRef } from "react";
import api from "../api";

const GoogleSignInButton = ({ setIsAuthenticated }) => {
    const buttonRef = useRef(null);

    useEffect(() => {
        if (window.google && buttonRef.current) {
            window.google.accounts.id.initialize({
                client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
                callback: handleCredentialResponse,
            });

            window.google.accounts.id.renderButton(buttonRef.current, {
                type: "standard",
                theme: "filled_blue",
                size: "large",
                text: "continue_with",
                shape: "rectangular",
                logo_alignment: "left",
                width: "300",
            });
        }
    }, []);

    const handleCredentialResponse = async (response) => {
        try {
            const res = await api.post("accounts/social/google/", {
                credential: response.credential,
            });

            localStorage.setItem("token", res.data.token);
            setIsAuthenticated(true);
        } catch (err) {
            console.error("Google login failed", err);
            // Handle error (show message to user)
        }
    };

    return <div ref={buttonRef}></div>;
};

export default GoogleSignInButton;
