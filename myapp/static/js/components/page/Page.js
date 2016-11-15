/**
 * Created by zhangfujun on 9/22/16.
 */
var React = require('react');
var PageForm = require('./pageForm');
var PageTable = require('./pageTable');

var Page = React.createClass({
    getInitialState: function () {
        return {
            pages: []
        }
    },
    listPage: function () {
        $.ajax({
            type: 'get',
            url: '/queryPage',
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.setState({pages: resp.pages})
            }
        }.bind(this))
    },
    addPage: function (data) {
        $.ajax({
            type: 'post',
            dataType: 'json',
            url: '/addPage',
            data: data,
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.listPage();
            }
        }.bind(this))
    },
    componentDidMount: function () {
        this.listPage();
    },
    render: function () {
        return (
            <div className="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
                <PageForm addPage={this.addPage}/>
                <PageTable pages={this.state.pages}/>{/**/}
            </div>
        )
    }

});


module.exports = Page