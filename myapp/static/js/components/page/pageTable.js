/**
 * Created by zhangfujun on 9/22/16.
 */
var React = require('react');
var PageItem = require('./PageItem');

var pageTable = React.createClass({
    render: function () {
        var mypages = this.props.pages.map(function (item) {
            return <PageItem key={item.id} page={item}/>
        }.bind(this));
        return (
            <div className="table-responsive">
                <table className="table table-striped">
                    <thead>
                    <tr>
                        <th>页面</th>
                        <th>中文名称</th>
                        <th>描述</th>
                        <th>创建时间</th>
                        <th>操作</th>
                    </tr>
                    </thead>
                    <tbody>
                    {/*{% for page in a.pages %}

                     <tr>
                     <td>{{page.pagename }}</td>
                     <td>{{page.chinese }}</td>
                     <td> {% if page.desc %}{{page.desc }}{% else %}{% endif %}</td>
                     <td>{{page.createtime }}</td>
                     <td><a href="/element/{{ page.id }}" target="_blank" class="btn btn-info">元素</a>
                     </tr>
                     {% endfor %}*/}
                    {mypages}

                    </tbody>
                </table>
            </div>
        )

    }
});
module.exports = pageTable;