var ReactDOM = require('react-dom');
var React = require("react");
var Todo = require('./components/Todo');
var Page = require('./components/page/Page');
var Case = require("./components/testcases/TestCases");
var Element = require("./components/element/element");

document.getElementById("todo-container") && ReactDOM.render(<Todo />, document.getElementById("todo-container"));

document.getElementById("page") && ReactDOM.render(<Page />, document.getElementById("page"));
//document.getElementById("components-table-demo-tree") && ReactDOM.render(<Demo />, document.getElementById('components-table-demo-tree'));

document.getElementById("tcs") && ReactDOM.render(<Case />, document.getElementById("tcs"));

document.getElementById("element") && ReactDOM.render(<Element />, document.getElementById("element"));