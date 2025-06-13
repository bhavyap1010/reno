import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, Button, Alert } from 'react-native';
import * as AuthSession from 'expo-auth-session';
import { useAuthRequest, makeRedirectUri, ResponseType } from 'expo-auth-session';
//import { googleClientId } from './config';
import { useEffect } from 'react';

const discovery = {
  authorizationEndpoint: 'https://accounts.google.com/o/oauth2/v2/auth',
  tokenEndpoint: 'https://oauth2.googleapis.com/token',
  revocationEndpoint: 'https://oauth2.googleapis.com/revoke',
};


const googleClientId = '642552962636-7aiu16ona083q7tnogeibavn8j6hh9al.apps.googleusercontent.com';

export default function App() {
  const redirectUri = makeRedirectUri();

  const [request, response, promptAsync] = useAuthRequest(
    {
      clientId: googleClientId,
      redirectUri,
      responseType: ResponseType.Code,
      scopes: ['openid', 'email', 'profile'],
      extraParams: { access_type: 'offline', prompt: 'consent' },
    },
    discovery
  );

  useEffect(() => {
    if (response?.type === 'success') {
      Alert.alert('Success', 'Google sign-in successful!');
      // You can now send response.params.code to your backend for token exchange
    } else if (response?.type === 'error') {
      Alert.alert('Error', 'An error occurred during Google sign-in.');
    }
  }, [response]);

  return (
    <View style={styles.container}>
      <Text>Sign in with Google below:</Text>
      <Button title="Sign in with Google" onPress={() => promptAsync()} disabled={!request} />
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
