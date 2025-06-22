import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
    const token = localStorage.getItem('auth_token');
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        if (token) {
            navigate("/");
        }
    }, []);

    const loginWithGoogle = () => {
        window.location.href = import.meta.env.VITE_GOOGLE_LINK;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            const response = await fetch(import.meta.env.VITE_API_URL + "/formlogin/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });
                if (response.ok) {
                    const data = await response.json();
                    localStorage.setItem("auth_token", JSON.stringify(data));
                    navigate("/");
                } else {
                    const errData = await response.json();
                    setError(errData.detail || "Login failed");
                }
        } catch (err) {
            setError("Login failed");
        }
    };

    const goToRegister = () => {
        navigate("/register");
    };

    return (
        <>
            <form onSubmit={handleSubmit} className="auth_form">
                <div>
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <p className="error">{error}</p>}
                <button type="submit">Sign in</button>
            </form>
            <div className="auth_button">
                <button onClick={loginWithGoogle}>
                    <i className="fa fa-google" aria-hidden="true"></i>
                    Sign in with Google
                </button>
            </div>
            <div className="auth_button">
                <button onClick={goToRegister}>
                    Register
                </button>
            </div>
        </>
    );
}

export default Login;
