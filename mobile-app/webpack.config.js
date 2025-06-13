const createExpoWebpackConfigAsync = require('@expo/webpack-config');

module.exports = async function (env, argv) {
  const config = await createExpoWebpackConfigAsync(env, argv);

  // Required for expo-router web routing
  config.resolve.alias['expo-router'] = require.resolve('expo-router');

  return config;
};
