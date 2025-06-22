import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';

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
    <View style={styles.form}>
      <Text style={styles.label}>Email:</Text>
      <TextInput
        style={styles.input}
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
        placeholder="Enter your email"
      />

      <Text style={styles.label}>Password:</Text>
      <TextInput
        style={styles.input}
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        placeholder="Enter your password"
      />

      {error ? <Text style={styles.error}>{error}</Text> : null}

      <TouchableOpacity style={styles.button} onPress={() => handleSubmit(email, password)}>
        <Text style={styles.buttonText}>Sign in</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={loginWithGoogle}>
        <Text style={styles.buttonText}>Sign in with Google</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={goToRegister}>
        <Text style={styles.buttonText}>Register</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  form: { padding: 20 },
  label: { marginTop: 10, marginBottom: 5, fontWeight: 'bold' },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    borderRadius: 5,
  },
  error: { color: 'red', marginVertical: 10 },
  button: {
    marginTop: 15,
    backgroundColor: '#007AFF',
    padding: 12,
    borderRadius: 5,
    alignItems: 'center',
  },
  buttonText: { color: 'white', fontWeight: 'bold' },
});


export default Login;
