/**
 * Created by zhangfujun on 10/19/16.
 */
var React = require('react');

var Eitem = React.createClass({

    deleteHandle:function () {
        $.ajax({
            type:'post',
            url:'/deleteElement',
            dataType:'json',
            data:{id:this.props.element.id}
        }).done(function (resp) {
            if(resp.status=='success'){
                this.props.listTable();
            }
        }.bind(this))
    },
    render: function () {
        var item = this.props.element;
        return (
            /*  <tr>
             <td colspan="6" align="center">没有数据!!</td>
             </tr>*/
            <tr>
                <td>{item.name}</td>
                <td>{item.locator}</td>
                <td> {item.chinese }</td>
                <td>{item.type }</td>
                <td>{item.createtime }</td>
                <td><a className="btn btn-info" onClick={this.deleteHandle}>删除</a></td>
            </tr>
        )
    }
});
module.exports = Eitem;