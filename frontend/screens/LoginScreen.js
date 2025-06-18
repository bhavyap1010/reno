import React, { useState, useEffect } from 'react';
import { View, TextInput, Button, Text, TouchableOpacity } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function LoginScreen({ navigation }) {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  useEffect(() => {
    // Check if token exists, if so, redirect to Home
    const checkAuth = async () => {
      const token = await AsyncStorage.getItem('token');
      if (token) {
        navigation.replace('Home');
      }
    };
    checkAuth();
  }, []);

  const handleLogin = async () => {
    setMsg('');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: identifier, password }),
      });
      const data = await res.json();
      if (res.ok) {
        // Save token to AsyncStorage
        await AsyncStorage.setItem('token', data.token);
        setMsg('');
        navigation.replace('Home');
      } else {
        setMsg('Incorrect username / password');
      }
    } catch (e) {
      setMsg('Network error');
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput placeholder="Username or Email" value={identifier} onChangeText={setIdentifier} style={{ marginBottom: 10, borderWidth: 1, padding: 8 }} />
      <TextInput placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry style={{ marginBottom: 10, borderWidth: 1, padding: 8 }} />
      <Button title="Login" onPress={handleLogin} />
      <Text style={{ color: 'red', marginTop: 10 }}>{msg}</Text>
      <TouchableOpacity onPress={() => navigation.navigate('Register')}>
        <Text style={{ color: 'blue', marginTop: 20 }}>Don't have an account? Register</Text>
      </TouchableOpacity>
    </View>
  );
}
