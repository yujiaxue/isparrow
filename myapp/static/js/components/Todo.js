var React = require("react");
var TodoForm = require('./TodoForm');
var TodoTable = require('./TodoTable');

var Todo = React.createClass({

    getInitialState: function () {
        return {
            todos: []
        }
    },

    listTodo: function () {
        $.ajax({
            type: 'get',
            url: '/queryPage',
        }).done(function (resp) {
            if (resp.status == "success") {
                this.setState({todos: resp.pages});
            }
        }.bind(this))
    },
    addTodo: function (content) {
        $.ajax({
            type: 'post',
            url: '/addPage',
            data: {content: content}
        }).done(function (resp) {
            if (resp.status == "success") {
            }
            this.listTodo();
        }.bind(this))
    },
    componentDidMount: function () {
        this.listTodo();
    },
    render: function () {
        return (<div>
            <TodoForm addTodo={this.addTodo}/>
            <TodoTable todos={this.state.todos}/>
        </div>)

    }
});

module.exports = Todo;