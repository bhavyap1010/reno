import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
} from 'react-native';


function Signup() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");
        if (password !== password2) {
            setError("Passwords do not match");
            return;
        }
        try {
            const response = await fetch(import.meta.env.VITE_API_URL + "/signup/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, email, password, password2 }),
            });
            if (response.ok) {
                setSuccess("Registration successful! You can now login.");
                setUsername("");
                setEmail("");
                setPassword("");
                setPassword2("");
            } else {
                const errData = await response.json();
                setError(errData.detail || "Registration failed");
            }
        } catch (err) {
            setError("Registration failed");
        }
    };

    const goToLogin = () => {
        navigate("/login");
    };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.label}>Username:</Text>
      <TextInput
        style={styles.input}
        value={username}
        onChangeText={setUsername}
        placeholder="Enter username"
      />

      <Text style={styles.label}>Email:</Text>
      <TextInput
        style={styles.input}
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        placeholder="Enter email"
        autoCapitalize="none"
      />

      <Text style={styles.label}>Password:</Text>
      <TextInput
        style={styles.input}
        value={password}
        onChangeText={setPassword}
        placeholder="Enter password"
        secureTextEntry
      />

      <Text style={styles.label}>Confirm Password:</Text>
      <TextInput
        style={styles.input}
        value={password2}
        onChangeText={setPassword2}
        placeholder="Confirm password"
        secureTextEntry
      />

      {error ? <Text style={styles.error}>{error}</Text> : null}
      {success ? <Text style={styles.success}>{success}</Text> : null}

      <TouchableOpacity style={styles.button} onPress={submitForm}>
        <Text style={styles.buttonText}>Register</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.secondaryButton} onPress={goToLogin}>
        <Text style={styles.secondaryButtonText}>Back to Login</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { padding: 20 },
  label: { marginTop: 10, fontWeight: 'bold' },
  input: {
    borderWidth: 1,
    borderColor: '#999',
    padding: 10,
    borderRadius: 6,
    marginBottom: 10,
  },
  error: { color: 'red', marginBottom: 10 },
  success: { color: 'green', marginBottom: 10 },
  button: {
    backgroundColor: '#007AFF',
    padding: 12,
    borderRadius: 6,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: { color: '#fff', fontWeight: 'bold' },
  secondaryButton: {
    padding: 12,
    marginTop: 10,
    alignItems: 'center',
  },
  secondaryButtonText: { color: '#007AFF' },
});

export default Signup;
