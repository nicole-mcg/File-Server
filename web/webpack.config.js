var webpack = require("webpack");
var path = require("path");
 
var SRC = path.resolve(__dirname, "src");
var BUILD = path.resolve(__dirname, "build");

var ExtractTextPlugin = require("extract-text-webpack-plugin");
const extractLess = new ExtractTextPlugin('style.css', {
    filename: "style.css",
    allChunks: true
})
 
var config = {
  entry: SRC + "/index.jsx",
  output: {
    path: BUILD,
    filename: "webpack.js"
  },
  devServer: {
    port: 3000,
    historyApiFallback: true
  },
  module: {
    loaders: [{
        test: /\.jsx$/,
        include: SRC,
        loader: "babel-loader",
        exclude: /node_modules/
    },{
        test: /\.js$/,
        include: SRC,
        loader: "babel-loader",
        exclude: /node_modules/
    }, {
        test: /\.css$/,
        loader: "style-loader!css-loader", // translates CSS into CommonJS 
        exclude: /node_modules/
    }, {
        test: /\.less$/,
        loader: extractLess.extract({
            use: [{
                loader: "css-loader"
            }, {
                loader: "less-loader"
            }],
            // use style-loader in development
            fallback: "style-loader"
        }), // compiles Less to CSS 
        exclude: /node_modules/
    }],
  },
  plugins: [
    extractLess
  ],
  resolve: {
    extensions: ['.js', '.jsx'],
  }
};

module.exports = config;