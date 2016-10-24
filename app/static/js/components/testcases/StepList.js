/**
 * Created by zhangfujun on 10/10/16.
 */
var React = require('react');

var StepList = React.createClass({
    render: function () {
        var step = this.props.step;
        return (
            <div className="subcontent ">
                <span className="col-lg-1"><label className="label label-info">{step.sort}</label></span>
                <span className="content col-lg-2">{step.page}</span>
                <span className="content col-lg-3">{step.element}</span>
                <span className="content col-lg-2">{step.action}</span>
                <span className="content col-lg-2">{step.value}</span>
                <span className="content col-lg-1">{step.attr}</span>
                <span className="content col-lg-1"><button type="button"
                                                       className="btn btn-info">编辑</button></span>
            </div>
        )
    }
});
module.exports = StepList;