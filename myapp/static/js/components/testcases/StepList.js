/**
 * Created by zhangfujun on 10/10/16.
 */
var React = require('react');
var ReactDom = require('react-dom');

var StepList = React.createClass({
    getInitialState:function () {
      return {
          edit:false,
          update:false
      }
    },
    deleteItem: function () {
        var id = this.props.step.id;
        data = {id:id};
        this.props.deleteItem(data);

    },
    editItem:function(){
        this.setState({edit: true});
    },
    handlerStepUpdate:function (e) {
        e.preventDefault();
        var id = this.props.step.id;
        var cid = this.props.step.caseid;
        var sid = ReactDom.findDOMNode(this.refs.sortn).value;
        var page = ReactDom.findDOMNode(this.refs.page).value.trim();
        var element = ReactDom.findDOMNode(this.refs.element).value.trim();
        var action = ReactDom.findDOMNode(this.refs.action).value.trim();
        var input = ReactDom.findDOMNode(this.refs.input).value.trim();
        var attr = ReactDom.findDOMNode(this.refs.attr).value.trim();
        if (!id || !page  || !action){
            return ;
        }
        this.props.updateStep({id:id,cid:cid, sid: sid, page: page, element: element, action: action, input: input, attr: attr});
        this.setState({edit: false});
        return;
    },
    render: function () {
        console.log('ok..');
        var step = this.props.step;
        if (this.state.edit){
            return (
                <div className="subform">
                <form onSubmit={this.handlerStepUpdate}>
                    <span className="col-lg-1"><label className="label label-info">{this.props.step.sort}</label>
                    <input ref="sortn" type="hidden" defaultValue={this.props.step.sort}/> </span>
                    <span className="col-lg-2 content" style={{paddingRight: '0px', paddingLeft: '0px'}}>
                        <input ref="page" className="form-control" type="text" id="page"
                               name="page" placeholder="页面" defaultValue={this.props.step.page}/>
                    </span>
                    <span className="col-lg-2 content" style={{paddingRight: '0px', paddingLeft: '0px'}}> <input
                        ref="element" className="form-control" type="text"
                        name="selenium"
                        id="selenium" placeholder="元素" defaultValue={this.props.step.element}/></span>
                    <span className="col-lg-2 content" style={{paddingRight: '0px', paddingLeft: '0px'}}> <input
                        ref="action" className="form-control" type="text"
                        name="action"
                        id="action" placeholder="动作" defaultValue={this.props.step.action}/></span>
                    <span className="col-lg-2 content" id="sp" style={{paddingRight: '0px', paddingLeft: '0px'}}> <input
                        ref="input" className="form-control" type="text"
                        name="input"
                        placeholder="输入值" defaultValue={this.props.step.value}/></span>
                    <span className="col-lg-2 content"
                          style={{paddingRight: '0px', paddingLeft: '0px', display: 'hidden'}}> <input
                        ref="attr" className="form-control" type="text"
                        name="attr"
                        placeholder="断言属性" defaultValue={this.props.step.attr}/></span>
                    <span className="col-lg-1 content"> <button className="btn btn-info" type="submit"
                                                                id="submit">保存</button></span>
                </form>
            </div>
            )

        }else{


        return (
            <div className="subcontent " id = {step.id} >
                <span className="col-lg-1"><label className="label label-info" ref="sort">{step.sort}</label></span>
                <span className="content col-lg-2" ref="page">{step.page}</span>
                <span className="content col-lg-2" ref="element">{step.element}</span>
                <span className="content col-lg-2" ref="action">{step.action}</span>
                <span className="content col-lg-2" ref="value">{step.value}</span>
                <span className="content col-lg-1" ref="attr">{step.attr}</span>
                <span className=" col-lg-2">
                    <div className="btn-group-xs">
                    <button type="button" className="btn btn-info btn-xs" onClick={this.editItem}>edit</button>
                    <button type="button" className="btn btn-danger btn-xs" onClick={this.deleteItem}>del</button>
                </div>
                </span>
            </div>
        )
            }
    }
});
module.exports = StepList;