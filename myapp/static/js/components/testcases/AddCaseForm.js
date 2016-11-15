/**
 * Created by zhangfujun on 10/8/16.
 */
var React = require('react');
var ReactDom = require('react-dom');

var addCaseForm = React.createClass({
    handlerSubmit: function (e) {
        e.preventDefault();
        var caseName = ReactDom.findDOMNode(this.refs.caseName).value.trim();
        if (!caseName) {
            return;
        }
        // TODO: send request to the server
        this.props.addCase({caseName: caseName});
        ReactDom.findDOMNode(this.refs.caseName).value = '';
        return;
    },

    render: function () {
        return (
            <div className="panel panel-default">
                <div className="panel-body">
                    <form className="form-inline" role="form" onSubmit={this.handlerSubmit}>
                        <div className="input-group" style={{width: '100%'}}>
                            <div className="input-group-btn">
                                <input className="form-control" style={{width: '80%', border: '3px solid #5CB85C'}}
                                       type="text" ref="caseName"
                                       id="casename" name="casename"
                                       placeholder="case Name"/>
                                <span className="input-group-btn" style={{width:'20%'}}>
                                <button type="submit" style={{border: '1px solid #5CB85C', width: '100%'}}
                                        className="btn btn-success">添加一条用例吧</button>
                           </span>
                            </div>
                        </div>
                    </form>
                </div>
            </div>);
    }
});

module.exports = addCaseForm;