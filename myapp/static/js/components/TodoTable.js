/**
 * Created by zhangfujun on 9/22/16.
 */
var React = require('react')
var TodoItem = require('./TodoItem')

var TodoTable = React.createClass({
    render: function () {
        var todos = this.props.todos.map(function (item) {
            return <TodoItem key={item.id} todo={item}/>
        }.bind(this));
        return (
            <div>
                <h2>Todo List</h2>
                <table className="table">
                    <thead>
                    <tr>
                        <th>content</th>
                        <th>status</th>
                        <th>time</th>
                        <th>opreation</th>
                    </tr>
                    </thead>
                    <tbody>
                    {todos}
                    </tbody>
                </table>
            </div>
        )
    }
});


module.exports = TodoTable;