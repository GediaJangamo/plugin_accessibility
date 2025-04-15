// const { defineConfig } = require('@vue/cli-service')
// const path = require('path')

// module.exports = defineConfig({
//   transpileDependencies: true,
//   outputDir: path.resolve(__dirname, '../core/static/core/js'),
//   filenameHashing: false,
//   css: {
//     extract: {
//       filename: '../css/main.css'
//     }
//   },
//   configureWebpack: {
//     output: {
//       filename: 'bundle.js'
//     },
//     optimization: {
//       splitChunks: false // Desabilita a divisão em chunks
//     }
//   }
// })

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
  },
  chainWebpack: config => {
    // Configura o carregamento de imagens
    config.module
      .rule('images')
      .use('url-loader')
      .loader('url-loader')
      .tap(options => {
        options = options || {}
        options.limit = 4096 // Arquivos menores que 4kb serão convertidos para base64
        options.fallback = {
          loader: 'file-loader',
          options: {
            name: '../img/[name].[ext]', // Caminho relativo para imagens
            publicPath: '/' // Caminho público para acesso às imagens
          }
        }
        return options
      })
  }
})