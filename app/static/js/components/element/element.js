/**
 * Created by zhangfujun on 9/27/16.
 */

var React = require('react');
var EleForm = require('./elementForm');
var EleTable = require('./ElementTable');

var element = React.createClass({

    getInitialState: function () {
        return {
            elements: [],
        }
    },
    listElements: function () {
         var hh = window.location.href.split('/');
        var pid = hh[hh.length - 1];
        $.ajax({
            type: 'get',
            url: '/element/item/' + pid,
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.setState({elements: resp.elements});
            }else{
                console.info('resp fail list');
            }
        }.bind(this))
    },
    addElement: function (data) {
        $.ajax({
            type: 'post',
            url: '/addElement',
            dataType:'json',
            data: data
        }).done(function (resp) {
            if (resp.status == 'fail') {
                alert('fail');
            } else {
                this.listElements();
            }
        }.bind(this))
    },
    componentDidMount: function () {
        this.listElements();
    },
    render: function () {
        return (
            <div className="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
                <EleForm addElement={this.addElement}/>
                <EleTable elements={this.state.elements}/>
            </div>
        )
    }

});
module.exports = element;