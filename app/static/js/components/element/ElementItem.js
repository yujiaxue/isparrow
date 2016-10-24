/**
 * Created by zhangfujun on 10/19/16.
 */
var React = require('react');

var Eitem = React.createClass({

    render: function () {

        var item = this.props.element;
        console.info(item);
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
                <td><a className="btn btn-info">删除</a></td>
            </tr>
        )
    }
});
module.exports = Eitem;