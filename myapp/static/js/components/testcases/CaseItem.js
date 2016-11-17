/**
 * Created by zhangfujun on 10/8/16.
 */
var React = require('react');
var ReactDom = require('react-dom');
var StepList = require('./StepList');
var CaseItem;
CaseItem = React.createClass({

    getInitialState(){
        return {
            add: false,
            steps: [],
            orderid: 0,
            value: 'test'
        }
    },
    addStep: function (e) {
        this.setState({add: true});
        this.listSteps();
        var pages = this.props.pages;
        var actions = this.props.actions;
        var pageelement = this.props.pageelement;
        setTimeout(function () {
            $('#page').autocomplete({
                source: pages
            });
            $('#action').autocomplete({
                source: actions
            });
            $('#page').blur(function () {
                var key = $(this).val();
                $('#selenium').autocomplete({
                    source: pageelement[key]
                })
            });
        }, 0)

    },
    collpase: function () {
        this.setState({add: false});
    },
    componentDidMount: function () {
        this.listSteps();
    },
    componentWillMount: function () {

    },
    listSteps: function () {
        var cid = this.props.page.id;
        $.ajax({
            type: 'get',
            url: '/getcasesteps/' + cid
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.setState({steps: resp.steps, orderid: resp.steps.length + 1});
            }
        }.bind(this))
    },

    handlerStep: function (e) {
        e.preventDefault();
        var cid = this.props.page.id;
        var sid = ReactDom.findDOMNode(this.refs.sortn).value;
        var page = ReactDom.findDOMNode(this.refs.page).value.trim();
        var element = ReactDom.findDOMNode(this.refs.element).value.trim();
        var action = ReactDom.findDOMNode(this.refs.action).value.trim();
        var input = ReactDom.findDOMNode(this.refs.input).value.trim();
        var attr = ReactDom.findDOMNode(this.refs.attr).value.trim();

        if(!page  || !action){
            return ;
        }
        $.ajax({
            type: 'post',
            url: '/addonestep',
            data: {cid: cid, sid: sid, page: page, element: element, action: action, input: input, attr: attr},
            dataType: 'json'
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.listSteps();
            }
        }.bind(this));
        ReactDom.findDOMNode(this.refs.page).value = '';
        ReactDom.findDOMNode(this.refs.element).value = '';
        ReactDom.findDOMNode(this.refs.action).value = '';
        ReactDom.findDOMNode(this.refs.input).value = '';
        ReactDom.findDOMNode(this.refs.attr).value = '';
        return;
    },
    deleteItem:function (data) {
        $.ajax({
            type: 'post',
            url: '/deleteItem',
            data: data,
            dataType: 'json'
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.listSteps();
            }
        }.bind(this));
        return;
    },

    handlerUpdateStep: function (data) {
        $.ajax({
            type: 'post',
            url: '/updateonestep',
            data: data,
            dataType: 'json'
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.listSteps();
            }
        }.bind(this));
        /*ReactDom.findDOMNode(this.refs.page).value = '';
        ReactDom.findDOMNode(this.refs.element).value = '';
        ReactDom.findDOMNode(this.refs.action).value = '';
        ReactDom.findDOMNode(this.refs.input).value = '';
        ReactDom.findDOMNode(this.refs.attr).value = '';*/
        return;
    },

    contentForm: function () {
        return this.state.add ? (
            <div className="subform">
                <form onSubmit={this.handlerStep}>
                    <span className="col-lg-1"><label className="label label-info">{this.state.orderid}</label>
                    <input ref="sortn" type="hidden" value={this.state.orderid}/> </span>
                    <span className="col-lg-2 content" style={{paddingRight: '0px', paddingLeft: '0px'}}>
                        <input ref="page" className="form-control" type="text" id="page"
                               name="page" placeholder="页面"/>
                    </span>
                    <span className="col-lg-2 content" style={{paddingRight: '0px', paddingLeft: '0px'}}> <input
                        ref="element" className="form-control" type="text"
                        name="selenium"
                        id="selenium" placeholder="元素"/></span>
                    <span className="col-lg-2 content" style={{paddingRight: '0px', paddingLeft: '0px'}}> <input
                        ref="action" className="form-control" type="text"
                        name="action"
                        id="action" placeholder="动作"/></span>
                    <span className="col-lg-2 content" id="sp" style={{paddingRight: '0px', paddingLeft: '0px'}}> <input
                        ref="input" className="form-control" type="text"
                        name="input"
                        placeholder="输入值"/></span>
                    <span className="col-lg-2 content"
                          style={{paddingRight: '0px', paddingLeft: '0px', display: 'hidden'}}> <input
                        ref="attr" className="form-control" type="text"
                        name="attr"
                        placeholder="断言属性"/></span>
                    <span className="col-lg-1 content"> <button className="btn btn-info" type="submit"
                                                                id="submit">保存</button></span>
                </form>
            </div>
        ) : ""
    },
    render: function () {
        var mySteps = this.state.steps.map(function (item) {
            return <StepList key={item.id} step={item} updateStep={this.handlerUpdateStep} deleteItem={this.deleteItem}/>
        }.bind(this));
        var orderid = 1;
        var item = this.props.page;
        return (
            <div className="col-lg-12">
                <h5><span className="col-lg-6" id={item.id}>{item.title} </span>
                    <div className="btn-group-xs">
                        <button onClickCapture={this.addStep} className="btn btn-default btn-info"
                                style={{marginRight: '3px'}} id="addcase"><i
                            className="glyphicon glyphicon-plus"></i>
                        </button>
                        <button onClick={this.collpase} className="btn btn-default btn-info" id="expanse"><i
                            className="glyphicon glyphicon-chevron-down"></i></button>
                    </div>
                </h5>
                {mySteps}
                {this.contentForm()}
            </div>
        )
    },
});
module.exports = CaseItem;

