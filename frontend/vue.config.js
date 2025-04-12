const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: path.resolve(__dirname, '../core/static/core/js'),
  filenameHashing: false,
  css: {
    extract: {
      filename: '../css/main.css'
    }
  },
  configureWebpack: {
    output: {
      filename: 'bundle.js'
    },
    optimization: {
      splitChunks: false // Desabilita a divisão em chunks
    }
  }
})