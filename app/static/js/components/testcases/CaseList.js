/**
 * Created by zhangfujun on 10/8/16.
 */
var React = require('react');
var CaseItem = require('./CaseItem');

var CaseList = React.createClass({
    getInitialState: function () {
        return {
            pages: [],
            actions:[],
            mapelement:[],
        }
    },
    componentWillMount: function () {
        $.ajax({
            type: 'get',
            url: '/getpages',
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.state.pages = resp.pages
            } else {
                console.info('no pages')
            }
        }.bind(this));
        $.ajax({
            type: 'get',
            url: 'getactions'
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.state.actions = resp.actions
            }
        }.bind(this));
        $.ajax({
            type:'get',
            url:'/pagemapelement'
        }).done(function (resp) {
            if(resp.status=='success'){
                this.state.mapelement=resp.pageelement
            }
        }.bind(this));
    },
    render: function () {
        var tc = this.props.tcs.map(function (item) {
            return <CaseItem key={item.id}  page={item} pages={this.state.pages} actions={this.state.actions} pageelement={this.state.mapelement}/>
        }.bind(this));
        return (
            <div className="panel-default panel col-lg-12">
                <div className="panel-body">
                    {tc}
                </div>
            </div>
        )
    }
});
module.exports = CaseList;