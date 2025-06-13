import { googleCallbackUri, googleClientId } from './config';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import * as AuthSession from 'expo-auth-session';
import { useEffect } from 'react';

function App() {
  useEffect(() => {
    // Log the redirect URI for Expo AuthSession
    console.log('Expo AuthSession Redirect URI:', AuthSession.makeRedirectUri());
  }, []);

  const googleSignInUrl = `https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=${googleCallbackUri}&prompt=consent&response_type=code&client_id=${googleClientId}&scope=openid%20email%20profile&access_type=offline`;

  return (
    <View style={styles.container}>
      <Text>Open up App.tsx to start working on your app!</Text>
      <a href={googleSignInUrl}>Sign in with Google</a>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default App;
