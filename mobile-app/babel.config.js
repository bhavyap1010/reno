module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'], // handles everything now
  };
};
