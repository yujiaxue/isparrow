/**
 * Created by zhangfujun on 9/22/16.
 */

var React = require('react');
var ReactDom = require('react-dom');

var pageForm = React.createClass({

    handleSubmit: function (e) {
        e.preventDefault();
        var page = ReactDom.findDOMNode(this.refs.page).value.trim();
        var china = ReactDom.findDOMNode(this.refs.china).value.trim();
        var desc = ReactDom.findDOMNode(this.refs.desc).value.trim();
        if (!page || !china) {
            return;
        }
        // TODO: send request to the server
        this.props.addPage({page: page, china: china, desc: desc});
        ReactDom.findDOMNode(this.refs.page).value = '';
        ReactDom.findDOMNode(this.refs.china).value = '';
        ReactDom.findDOMNode(this.refs.desc).value = '';
        return;
    },
    render: function () {
        var addPage = this.props.addPage;
        return (
                <form className="form-inline" role="form" onSubmit={this.handleSubmit}>
                    <input className="form-control" style={{width:'30%'}} ref="page" id="pname" name="pname" placeholder="Page's Name 必填"/>
                    <input className="form-control" style={{width:'30%'}} ref="china" id="chinese" name="chinese" placeholder="中文名称 必填"/>
                    <input className="form-control" style={{width:'30%'}} ref="desc" id="desc" name="desc" placeholder="描述"/>
                    <button className="btn btn-default" type="submit">Add</button>
                </form>
        )


    }

});

module.exports = pageForm;