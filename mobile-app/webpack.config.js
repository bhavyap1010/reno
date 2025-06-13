const createExpoWebpackConfigAsync = require('@expo/webpack-config');

module.exports = async function (env, argv) {
  const config = await createExpoWebpackConfigAsync(env, argv);

  // Required for expo-router web routing
  config.resolve.alias['expo-router'] = require.resolve('expo-router');

  // Add browser polyfills for Node.js core modules
  config.resolve.fallback = {
    ...(config.resolve.fallback || {}),
    crypto: require.resolve('crypto-browserify'),
    stream: require.resolve('stream-browserify'),
    vm: require.resolve('vm-browserify'),
  };

  return config;
};
