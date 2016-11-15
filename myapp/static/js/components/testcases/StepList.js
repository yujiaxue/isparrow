/**
 * Created by zhangfujun on 10/10/16.
 */
var React = require('react');

var StepList = React.createClass({
    deleteItem: function () {
        var id = this.step.id;
        $.ajax({
            type: 'post',
            url: '/deleteItem',
            data: {id: id},
            dataType: 'json'
        }).done(function (resp) {
            if (resp.status == 'success') {
                this.state.update = true;
            }
        })
    },
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
                <span className="content col-lg-1">
                    <button type="button" className="btn btn-info" onClick={this.editItem}>edit</button>
                    {/*<button type="button" className="btn btn-info" onClick={this.deleteItem}>d</button>
                     <button type="button" className="btn btn-info" onClick={this.afterItem}>a</button>*/}
                </span>
            </div>
        )
    }
});
module.exports = StepList;