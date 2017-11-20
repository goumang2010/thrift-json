"use strict";
var PythonShell = require('python-shell');
var path = require('path');
module.exports = exports.default = function (files) {
    if (files && (typeof files === 'string')) files = [files];
    else if (!Array.isArray(files)) return Promise.reject('Please input files array');
    return new Promise(function (resolve, reject) {
        var thriftpy = new PythonShell(path.relative(process.cwd(), path.resolve(__dirname, 'thrift_to_json.py')));
        var result = [];
        var idx = 0;
        // sends a message to the Python script via stdin
        thriftpy.on('message', function (message) {
            if (message)
                result.push({ source: files[idx], value: JSON.parse(message) });
            idx++;
        });
        files.forEach(function (x) {
            thriftpy.send(path.resolve(process.cwd(), x));
        });
        thriftpy.end(function (err) {
            if (err)
                reject(err);
            resolve(result);
        });
    });
};
