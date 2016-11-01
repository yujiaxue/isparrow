/**
 * Created by zhangfujun on 10/19/16.
 */

var React = require('react');
var Eitem = require('./ElementItem');

var Table = React.createClass({

    render: function () {
        var myelement = this.props.elements.map(function (item) {
            return <Eitem key={item.id} element={item} listTable={this.props.listTable} />
        }.bind(this));
        return (
            <div className="table-responsive">
                <table className="table table-striped">
                    <thead>
                    <tr>
                        <th>元素</th>
                        <th>定位器</th>
                        <th>中文</th>
                        <th>定位类型</th>
                        <th>创建时间</th>
                        <th>操作</th>
                    </tr>
                    </thead>
                    <tbody>
                    {myelement}
                    </tbody>
                </table>
            </div>
        )
    }
});
module.exports = Table;