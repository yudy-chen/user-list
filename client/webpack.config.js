var CopyWebpackPlugin = require("./node_modules/copy-webpack-plugin");
var ExtractTextPlugin = require("./node_modules/mini-css-extract-plugin");
var utils = require('./utils');
var path = require('path');
const { VueLoaderPlugin } = require('./node_modules/vue-loader')

module.exports = {
    devtool: "source-map",
    entry: "./src/app.js",
    mode : 'development',
    devServer: {
        static: {
          directory: path.join(__dirname, 'public'),
        },
        compress: true,
        port: 9000,
    },    
    output: {
        path: path.resolve("./public/static/js"),
        publicPath: "/js/",
        filename: '[name].chunk.js',
        chunkFilename: '[name].chunk.js',
    },
    optimization: {
        splitChunks: {
            chunks: 'all',
        },
    },
    //watch: true,
    watchOptions: {
        ignored: [path.resolve("./node_modules/")]
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: './node_modules/vue-loader',
                options: {
                  loaders: utils.cssLoaders({
                    sourceMap: true,
                    extract: true
                  })
                }
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: './node_modules/babel-loader'
            },
            {
                test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
                loader: './node_modules/url-loader',
                options: {
                  limit: 10000,
                  name: utils.assetsPath('img/[name].[hash:7].[ext]')
                }
            },
            {
                test: /\.(woff(2)?|ttf|eot)(\?v=\d+\.\d+\.\d+)?$/,
                use: [{
                    loader: './node_modules/file-loader',
                    options: {
                        name: '[name].[ext]',
                        outputPath: '../fonts/'
                    }
                }]
            },
            {
                test:/\.scss$/,
                use:[
                        {
                            loader: "./node_modules/style-loader"
                        }, 
                        {
                            loader: "./node_modules/css-loader"
                        },
                        {
                            loader: "./node_modules/sass-loader",
                        }
                    ]
            },

            { test: /(\.css$)/, 
                loaders: [
                            './node_modules/style-loader', 
                            './node_modules/css-loader'
                ] 
            }
    
        ]
    },
    resolve: {
        extensions: ['*', '.js', '.vue', '.json'],
        modules: [ "node_modules", __dirname + "/static/js" ],
    },
    plugins: [
        new VueLoaderPlugin()
    ]
}