/**
 * Created by zhangfujun on 9/22/16.
 */
var React = require('react');

var PageItem = React.createClass({
    render: function () {
        var page = this.props.page;
        return (
            <tr>
                <td>{page.pagename }</td>
                <td>{page.chinese }</td>
                <td> {page.desc}</td>
                <td>{page.createtime } </td>
                <td><a href={"/element/" + page.id} target="_blank" className="btn btn-info">元素</a></td>
            </tr>
        )
    }
});

module.exports = PageItem;