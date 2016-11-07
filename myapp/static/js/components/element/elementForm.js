/**
 * Created by zhangfujun on 10/19/16.
 */

var React = require('react');
var ReactDom = require('react-dom');

var eleForm = React.createClass({
    handleAddElement: function (e) {
        e.preventDefault();
        var name = ReactDom.findDOMNode(this.refs.name).value.trim();
        var locator = ReactDom.findDOMNode(this.refs.locator).value.trim();
        var type = ReactDom.findDOMNode(this.refs.type).value.trim();
        var chinese = ReactDom.findDOMNode(this.refs.chinese).value.trim();
        //var pid = ReactDom.findDOMNode(this.refs.pid).value.trim();
        var hh = window.location.href.split('/');
        var pid = hh[hh.length - 1];
        if (!type) {
            type = 'xpath';
        }

        if (!name || !locator ) {
            return;
        }
        this.props.addElement({name: name, locator: locator, type: type, chinese: chinese, pid: pid});
        ReactDom.findDOMNode(this.refs.name).value = '';
        ReactDom.findDOMNode(this.refs.locator).value = '';
        ReactDom.findDOMNode(this.refs.type).value = '';
        ReactDom.findDOMNode(this.refs.chinese).value = '';
        return;
    },
    render: function () {
        return (
            <form className="form-inline" role="form" onSubmit={this.handleAddElement}>
                <input className="form-control" style={{'width':'20%'}} ref="name" id="name" name="name" placeholder="元素名称 必填"/>
                <input className="form-control" style={{width: '40%'}} ref="locator" id="locator" name="locator"
                       placeholder="定位器 必填"/>
                <input className="form-control" ref="type" id="type" name="type" placeholder="定位器类型 必填"/>
                <input className="form-control" ref="chinese" style={{width:'15%'}} id="chinese" name="chinese"
                       placeholder="中文"/>
                <input type="hidden" ref="pid" id="pid" name="pid"/>
                <button className="btn btn-default" type="submit">Add</button>
            </form>
        )
    }
});
module.exports = eleForm;