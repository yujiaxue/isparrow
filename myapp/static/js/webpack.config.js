/**
 * Created by zhangfujun on 9/19/16.
 */

module.exports = {
    entry: {
        index: "./index.js",
    },
    output: {
        path: "./build",
        filename: "bundle.js"
    },
    module: {
        loaders: [
            {test: /\.js$/, loader: 'jsx-loader'}
        ]
    },

}