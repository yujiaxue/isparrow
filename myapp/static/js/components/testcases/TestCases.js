/**
 * Created by zhangfujun on 9/27/16.
 */

var React = require('react');
var AddCaseForm = require('./AddCaseForm');
var CaseList = require('./CaseList');


var TestCases = React.createClass({
    getInitialState: function () {
        return {
            tcs: []
        }
    },
    addCase: function (data) {
        $.ajax({
            type: 'post',
            url: '/addCase',
            data: data,
            dataType: 'json',
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.listCases();
            }
        }.bind(this))
    },
    listCases: function () {
        $.ajax({
            type: 'get',
            url: '/getCases'
        }).done(function (resp) {
            if ('success' == resp.status) {
                this.setState({tcs: resp.tc})
            }
        }.bind(this))
    },
    componentDidMount:function () {
        this.listCases();
    },
    render: function () {
        return (
            <div >
                <AddCaseForm addCase={this.addCase}/>
                <CaseList tcs={this.state.tcs}/>
            </div>
        )
    }
});
module.exports = TestCases;

