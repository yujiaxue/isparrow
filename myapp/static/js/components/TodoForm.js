/**
 * Created by zhangfujun on 9/22/16.
 */

var React = require('react')
var TodoForm = React.createClass({
    render: function () {
        return (
            <form className="input-group">
                <input ref="content" className="form-control" id="content" name="content"/>
                <span className="input-group-btn">
                    <button className="btn btn-default" type="submit">Add</button>
                </span>
            </form>
        )
    }
});
module.exports = TodoForm;