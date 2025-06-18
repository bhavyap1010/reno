import React, { useState, useEffect } from 'react';
import { View, TextInput, Button, Text, TouchableOpacity } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Picker } from '@react-native-picker/picker';


export default function RegisterScreen({ navigation }) {
  const [form, setForm] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    account_type: '',
    password1: '',
    password2: ''
  });
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

  const handleChange = (name, value) => setForm({ ...form, [name]: value });

  const handleRegister = async () => {
    setMsg('');
    const res = await fetch('http://127.0.0.1:8000/api/signup/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    if (res.ok) {
      setMsg('Registration successful!');
      navigation.navigate('Login');
    } else {
      setMsg(JSON.stringify(data));
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput placeholder="Username" value={form.username} onChangeText={v => handleChange('username', v)} style={{ marginBottom: 10, borderWidth: 1, padding: 8 }} />
      <TextInput placeholder="First Name" value={form.first_name} onChangeText={v => handleChange('first_name', v)} style={{ marginBottom: 10, borderWidth: 1, padding: 8 }} />
      <TextInput placeholder="Last Name" value={form.last_name} onChangeText={v => handleChange('last_name', v)} style={{ marginBottom: 10, borderWidth: 1, padding: 8 }} />
      <TextInput placeholder="Email" value={form.email} onChangeText={v => handleChange('email', v)} style={{ marginBottom: 10, borderWidth: 1, padding: 8 }} />
      <Picker
        selectedValue={form.account_type}
        onValueChange={v => handleChange('account_type', v)}
        style={{ marginBottom: 10, borderWidth: 1 }}
      >
        <Picker.Item label="Select Account Type" value="" />
        <Picker.Item label="User" value="user" />
        <Picker.Item label="Provider" value="provider" />
      </Picker>
      <TextInput placeholder="Password" value={form.password1} onChangeText={v => handleChange('password1', v)} secureTextEntry style={{ marginBottom: 10, borderWidth: 1, padding: 8 }} />
      <TextInput placeholder="Confirm Password" value={form.password2} onChangeText={v => handleChange('password2', v)} secureTextEntry style={{ marginBottom: 10, borderWidth: 1, padding: 8 }} />
      <Button title="Register" onPress={handleRegister} />
      <Text style={{ color: 'red', marginTop: 10 }}>{msg}</Text>
      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={{ color: 'blue', marginTop: 20 }}>Already have an account? Login</Text>
      </TouchableOpacity>
    </View>
  );
}
