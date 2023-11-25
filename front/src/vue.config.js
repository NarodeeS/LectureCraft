const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  //filenameHashing: true,
  productionSourceMap: process.env.NODE_ENV != "production",
});
